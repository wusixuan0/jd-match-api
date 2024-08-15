import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
import os
from api.util.send_log import send_log

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
