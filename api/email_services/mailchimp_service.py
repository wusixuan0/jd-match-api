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

def subscribe_user_to_list(email, frequency):
    if not all([os.environ.get('MAILCHIMP_API_KEY'), os.environ.get('MAILCHIMP_AUDIENCE_ID'), os.environ.get('MAILCHIMP_REGION')]):
        raise ValueError("MAILCHIMP environment variable is not set")
    
    try:
        response = client.lists.add_list_member(os.environ.get('MAILCHIMP_AUDIENCE_ID'), {
            "email_address": email,
            "status": "subscribed",
        })
        send_log(f"Successfully added email to list. The response is: {response}")
        
        add_tag_to_subscriber(email, frequency)
        return response
    except ApiClientError as error:
        send_log(f"An exception occurred: {error.text}")
        raise error 

def add_tag_to_subscriber(email, tag):
    import hashlib
    try:
        subscriber_hash = hashlib.md5(email.lower().encode()).hexdigest()
        
        response = client.lists.update_list_member_tags(os.environ.get('MAILCHIMP_AUDIENCE_ID'), subscriber_hash, {
            "tags": [{"name": tag, "status": "active"}]
        })
        
        send_log(f"Successfully added tag to subscriber. The response is: {response}")
        return response
    except ApiClientError as error:
        send_log(f"An exception occurred while adding tag: {error.text}")
        raise error

def generate_scheduled_email_content(email, frequency):
    content = f"""
    <html>
    <body>
    <h1>Here Are Your {frequency.upper()} Job Recommendations</h1>
    """
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
    
    content += """
    </body>
    </html>
    """
    return content

def get_user_resume_summary(email):
    user_email = UserEmail.objects.get(email=email)
    resume_summary=Resume.objects.get(user_email=user_email).resume_summary
    return resume_summary

def send_test(email):
    try:
        campaign = client.campaigns.create({
            "type": "regular",
            "recipients": {"list_id": os.environ.get('MAILCHIMP_AUDIENCE_ID')},
            "settings": {
                "subject_line": "Thank You For Subscribing! Here Are Your Job Recommendations",
                "from_name": "https://jd-match.netlify.app/",
                "reply_to": os.environ.get('DEFAULT_FROM_EMAIL'),
            },
        })

        campaign_id = campaign['id']
        content = "<html><body>This is testing</body></html>"
        client.campaigns.set_content(campaign_id, {"html": content})

        # Send immediately
        response = client.campaigns.send(campaign_id)

        send_datetime = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        print(f"Sent campaign to {email} at {send_datetime} with ID: {campaign_id}. The response is: {response}")
        return response
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")