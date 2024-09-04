from api.services import resume_service
from api.util.send_log import send_log
from api.models import UserEmail, Resume, JobRecommendation
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import os
from datetime import datetime

client = MailchimpMarketing.Client()

client.set_config({
    "api_key": os.environ.get('MAILCHIMP_API_KEY'),
    "server": os.environ.get('MAILCHIMP_REGION')
})
def subscribe_user_to_list(email):
    if not all([os.environ.get('MAILCHIMP_API_KEY'), os.environ.get('MAILCHIMP_AUDIENCE_ID'), os.environ.get('MAILCHIMP_REGION')]):
        raise ValueError("MAILCHIMP environment variable is not set")

    try:
        subscriber_hash = get_subscriber_hash(email)
        audience_id = os.environ.get('MAILCHIMP_AUDIENCE_ID')
        
        try:
            response = client.lists.get_list_member(audience_id, subscriber_hash)
            if response.get("status") == 'subscribed':
                send_log(f"Email {email} already exists and subscribed.")
            else:
                send_log(f"Email {email} exists but status is unsubscribed.")
                response = client.lists.set_list_member(os.environ.get('MAILCHIMP_AUDIENCE_ID'), subscriber_hash, {"email_address": email, "status": "subscribed"})
            return response
        except ApiClientError:
            send_log(f"Email {email} not found in list, proceeding to subscribe.")

        return subscribe(email)

    except ApiClientError as error:
        send_log(f"Failed to add email to Mailchimp list: {error}")
        raise error

def subscribe(email):    
    try:
        response = client.lists.add_list_member(os.environ.get('MAILCHIMP_AUDIENCE_ID'), {
            "email_address": email,
            "status": "subscribed",
        })

        send_log(f"Successfully added email to list. The response is: {response}")        
        return response
    except ApiClientError as error:
        send_log(f"Fail to add email to Mailchimp list: {error.text}")
        raise error

def unsubscribe(email):
    try:
        subscriber_hash = get_subscriber_hash(email)
        response = client.lists.set_list_member(os.environ.get('MAILCHIMP_AUDIENCE_ID'), subscriber_hash, {"email_address": email, "status": "unsubscribed"})
        return response
    except ApiClientError as error:
        print(f"Fail to update email in Mailchimp list: {error.text}")
        raise error

def schedule_send(frequency):
    user_emails = UserEmail.objects.filter(frequency=frequency)
    for user_email in user_emails:
        email = user_email.email
        title = f"{frequency.capitalize()} Top Job Matches Based on Your Profile"
        ranked_docs = get_ranked_job(email)
        job_matched_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        send_one(email, ranked_docs, job_matched_time, title)
    return len(user_emails)

def send_one(email, ranked_docs, job_matched_time, title="Top Job Matches Based on Your Profile"):
    try:
        campaign = client.campaigns.create({
            "type": "regular",
            "recipients": {
                "list_id": os.environ.get('MAILCHIMP_AUDIENCE_ID'),
                "segment_opts": {
                    "match": "all",
                    "conditions": [{
                        "field": "EMAIL",
                        "op":  "contains",
                        "value": email
                    }]
                }
            },
            "settings": {
                "subject_line": f"{title} at {job_matched_time}",
                "from_name": "https://jd-match.netlify.app/",
                "reply_to": os.environ.get('DEFAULT_FROM_EMAIL'),
            },
        })
        
        campaign_id = campaign['id']
        
        content = generate_email_content(ranked_docs, title, job_matched_time)
        client.campaigns.set_content(campaign_id, {"html": content})
        
        response = client.campaigns.send(campaign_id)
        
        send_datetime = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        print(f"Sent one email to {email} at {send_datetime} with ID: {campaign_id}. The response is: {response}")
        return response
        
    except Exception as e:
        print(f"An error occurred while sending to {email}: {str(e)}")

def generate_email_content(ranked_docs, title, send_datetime):
    content = f"""
    <html>
    <body>
    <h1>{title}</h1>
    """

    for index, job in enumerate(ranked_docs):
        content += f"""
        <h2>Number {index+1} Match:</h2>
        <p><strong>Title:</strong> {job.get("_source").get("title")}</p>
        <p><strong>Company:</strong> {job.get("_source").get("companyName")}</p>
        <p><strong>Location:</strong> {job.get("_source").get("location")}</p>
        <p><strong>Apply link:</strong> <a href="{job.get("_source").get("applyOptions")[0].get("link")}">Apply Here</a></p>
        <p>{job.get("_source").get("description")[:1000]}...</p>
        <p><a href="{job.get("_source").get("applyOptions")[0].get("link")}">See full description</a></p>
        <hr>
        """
    
    content += f"""
    <b>Generated at {send_datetime}</b>

    </body>
    </html>
    """
    return content

def get_ranked_job(email):
    resume_summary = get_user_resume_summary(email)
    version = "version2"
    model_name = 'gemini-1.5-flash'
    match_result = resume_service(
        resume_data=resume_summary,
        version=version,
        model_name=model_name,
        is_url=False,
        top_n=5
    )
    ranked_docs = match_result.get("ranked_docs")
    return ranked_docs

def get_user_resume_summary(email):
    user_email = UserEmail.objects.get(email=email)
    resume_summary=Resume.objects.get(user_email=user_email).resume_summary
    return resume_summary

def get_subscriber_hash(email):
    import hashlib
    return hashlib.md5(email.lower().encode()).hexdigest()

# def add_tag_to_subscriber(email, tag):   
#     try:
#         subscriber_hash = get_subscriber_hash(email)
        
#         response = client.lists.update_list_member_tags(os.environ.get('MAILCHIMP_AUDIENCE_ID'), subscriber_hash, {
#             "tags": [{"name": tag, "status": "active"}]
#         })
        
#         send_log(f"Successfully added tag to subscriber. The response is: {response}")
#         return response
#     except ApiClientError as error:
#         send_log(f"An exception occurred while adding tag: {error.text}")
#         raise error

# def get_segment_id_from_tag_name(tag_name):
#     audience_id = os.environ.get('MAILCHIMP_AUDIENCE_ID')
#     for tag in client.lists.list_segments(audience_id).get('segments'):
#         if tag.get('name') == tag_name:
#             print(f"member count: {tag.get('member_count')}")
#             return tag.get('id')
#     return None

# def send_tag(tag_name):
#     try:
#         tag_id = get_segment_id_from_tag_name(tag_name)
#         if not tag_id:
#             print(f"Tag named '{tag_name}' not found.")
#             return

#         campaign = client.campaigns.create({
#             "type": "regular",
#             "recipients": {
#                 "list_id": os.environ.get('MAILCHIMP_AUDIENCE_ID'),
#                 'segment_opts': {
#                     'match': 'all',
#                     'conditions': [
#                         {
#                             'condition_type': 'StaticSegment',
#                             'field': 'static_segment',
#                             'op': 'static_is',
#                             'value': tag_id
#                         }
#                     ]
#                 }
#             },
#             "settings": {
#                 "subject_line": "Thank You For Subscribing! Here Are Your Job Recommendations",
#                 "from_name": "https://jd-match.netlify.app/",
#                 "reply_to": os.environ.get('DEFAULT_FROM_EMAIL'),
#             },
#         })

#         campaign_id = campaign['id']
#         content = "<html><body>This is testing</body></html>"
#         client.campaigns.set_content(campaign_id, {"html": content})

#         # Send immediately
#         response = client.campaigns.send(campaign_id)

#         send_datetime = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
#         print(f"Sent to tag '{tag_name}' at {send_datetime} with ID: {campaign_id}. The response is: {response}")
#         return response

#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
