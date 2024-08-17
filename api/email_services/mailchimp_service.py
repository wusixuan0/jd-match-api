from api.services import resume_service
from api.util.send_log import send_log
from api.models import UserEmail, Resume, JobRecommendation, UserFeedback
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import os
from datetime import datetime, timedelta
from datetime import datetime
import pdb
client = MailchimpMarketing.Client()

client.set_config({
    "api_key": os.environ.get('MAILCHIMP_API_KEY'),
    "server": os.environ.get('MAILCHIMP_REGION')
})

def subscribe_user_to_list(email):
    try:
        response = client.lists.add_list_member(os.environ.get('MAILCHIMP_AUDIENCE_ID'), {
            "email_address": email,
            "status": "subscribed",
        })
        send_log(f"Successfully added email to list. The response is: {response}")

    except ApiClientError as error:
        send_log(f"An exception occurred: {error.text}")
        raise error

def send_single_client(email):
    try:
        # Create a new segment for the single recipient
        segment_response = client.lists.create_segment(
            os.environ.get('MAILCHIMP_AUDIENCE_ID'),
            {"name": f"Single Recipient - {email}", "static_segment": [email]}
        )
        segment_id = segment_response['id']

        # Create the campaign
        campaign = client.campaigns.create({
            "type": "regular",
            "recipients": {
                "list_id": os.environ.get('MAILCHIMP_AUDIENCE_ID'),
                "segment_opts": {"saved_segment_id": segment_id}
            },
            "settings": {
                "subject_line": "Thank You For Subscribing! Here Are Your Job Recommendations",
                "from_name": "https://jd-match.netlify.app/",
                "reply_to": os.environ.get('DEFAULT_FROM_EMAIL'),
            },
        })

        campaign_id = campaign['id']
        content = generate_email_content(email)
        client.campaigns.set_content(campaign_id, {"html": content})

        # Send the campaign
        response = client.campaigns.send(campaign_id)

        send_datetime = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        print(f"Sent campaign to {email} at {send_datetime} with ID: {campaign_id}. The response is: {response}")
        # Clean up: delete the segment after sending
        client.lists.delete_segment(os.environ.get('MAILCHIMP_AUDIENCE_ID'), segment_id)

        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def send_all_subscriber(frequency):
    user_emails = UserEmail.objects.filter(frequency=frequency)
    for user_email in user_emails:
        email=user_email.email
    try:
        response = send_single_client(email)
        return response
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise e

def get_next_schedule_time(frequency):
    now = datetime.now()
    if frequency == 'daily':
        return now + timedelta(days=1)
    elif frequency == 'weekly':
        return now + timedelta(weeks=1)
    elif frequency == 'bi-weekly':
        return now + timedelta(weeks=2)

def generate_email_content(email):
    content = f"Job Recommendations for {email}\n"
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
    ranked_docs=match_result.get("ranked_docs")
    
    for index, job in enumerate(ranked_docs):
        content += f"Number {index+1} Match:\nTitle: "
        content += job.get("_source").get("title")
        content += "\nCompany: "
        content += job.get("_source").get("companyName")
        content += "\nLocation: "
        content += job.get("_source").get("location")
        content += "\napply link: "
        content += job.get("_source").get("applyOptions")[0].get("link")
        content += "\n"
        content += job.get("_source").get("description")[:1000]
        content += "\n...See full description: "
        content += job.get("_source").get("applyOptions")[0].get("link")
        content += "\n\n\n"

    return content

def get_user_resume_summary(email):
    user_email = UserEmail.objects.get(email=email)
    resume_summary=Resume.objects.get(user_email=user_email).resume_summary
    return resume_summary
