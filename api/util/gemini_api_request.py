import os
import google.generativeai as genai
from api.util.send_log import send_log
import time
from datetime import datetime

GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
retry_attempt = 0
# TODO write json schema for gemini-1.5-pro
def requestGeminiAPI(request_payload, model_name='gemini-1.5-flash'):
    global retry_attempt
    start_time = time.time()
    start_time_datetime = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
    send_log(f"Gemini API Request Start at {start_time_datetime}")

    model = genai.GenerativeModel(model_name)
    try:
        response = model.generate_content(request_payload)
        response_data = response.text
        end_time = time.time()
        duration = end_time - start_time

        send_log(f"Gemini API Response: \n{response_data}")
        send_log(f"<<<Gemini API Request Finished. Duration: {duration} seconds")
        return response_data
    except Exception as e:
        retry_attempt += 1
        send_log(f"!!!Gemini API ERROR: {e}")
        if retry_attempt > 1:
            send_log(f"<<<Stoping Gemini API request with model  {model_name} after 1 failed attempt.")
            raise e
        retry_wait = 60
        send_log(f"Retrying API request in {retry_wait} seconds...")
        time.sleep(retry_wait)
        return requestGeminiAPI(request_payload, model_name)