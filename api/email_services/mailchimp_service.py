from api.services import resume_service
from api.util.send_log import send_log
from api.models import UserEmail, Resume, JobRecommendation, UserFeedback
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import os
from datetime import datetime, timedelta

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

def send_job_recommendation():
    try:
        campaign = client.campaigns.create({
            "type": "regular",
            "recipients": {"list_id": os.environ.get('MAILCHIMP_AUDIENCE_ID')},
            "settings": {
                "subject_line": "Your Job Recommendations",
                "from_name": "https://jd-match.netlify.app/",
                "reply_to": os.environ.get('DEFAULT_FROM_EMAIL') or 'pewpewpewpikachu@gmail.com',
            },
        })

        campaign_id = campaign['id']
        content = generate_campaign_content('immediate')
        client.campaigns.set_content(campaign_id, {"html": content})

        # Send immediately
        response = client.campaigns.send(campaign_id)

        print(f"Sent immediate campaign with ID: {campaign_id}. The response is: {response}")
        return response
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_next_schedule_time(frequency):
    now = datetime.now()
    if frequency == 'daily':
        return now + timedelta(days=1)
    elif frequency == 'weekly':
        return now + timedelta(weeks=1)
    elif frequency == 'bi-weekly':
        return now + timedelta(weeks=2)

def generate_campaign_content(frequency):
    user_emails = UserEmail.objects.filter(frequency=frequency)
    content = f"Job Recommendations for {frequency.capitalize()} Subscribers\n\n"

    for user_email in user_emails:
        content += f"Recommendations for {user_email.email}:\n"
        resume_summary = get_user_resume(user_email)
        version = "version2"
        model_name = 'gemini-1.5-flash'
        match_result = resume_service(resume_summary, version, model_name, is_url=False, top_n=5)
        ranked_docs=match_result.get("ranked_docs")
        for index, job in enumerate(ranked_docs):
            content += f"Number {index+1} Match:\n"
            content += job.get("_source").get("title")
            content += "\nCompany: "
            content += job.get("_source").get("companyName")
            content += "\n"
            content += job.get("_source").get("location")
            content += "\nlink: "
            content += job.get("_source").get("applyOptions")[0].get("link")
            content += "\n"
            content += job.get("_source").get("description")[:1000]
            content += "\n"

    return content

def get_user_resume(user_email):
    resume_summary=Resume.objects.get(user_email=user_email).resume_url
    return resume_summary
