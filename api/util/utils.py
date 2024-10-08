import re

def html_to_plain_text(html_content):
    import html
    # Decode HTML entities
    text = html.unescape(html_content)
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', text)
    # Remove extra whitespace and newlines
    text = ' '.join(text.split())
    return text

def load_pdf(url):
    from langchain_community.document_loaders import PyMuPDFLoader
    loader = PyMuPDFLoader(url)
    docs = loader.load()
    full_text = " ".join(doc.page_content for doc in docs)
    return clean_text(full_text)

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove markdown formatting
    text = re.sub(r'\*{1,2}|\_{1,2}|`{1,2}|~{1,2}|#{1,6}|>\s?|\[.*?\]\(.*?\)|!\[.*?\]\(.*?\)', '', text)

    # Remove non-printable characters and excessive whitespace
    import string
    printable = set(string.printable)
    text = ''.join(filter(lambda x: x in printable, text))
    text = ' '.join(text.split())

    return text

def extract_json_from_response(response_text):
    import json
    json_pattern_with_json = re.compile(r'`json(.*?)`', re.DOTALL)  # Match content between ```json markers
    json_pattern_backticks_only = re.compile(r'`(.*?)`', re.DOTALL)  # Match content between ``` markers

    # Try to match with json prefix
    match = json_pattern_with_json.search(response_text)
    if match:
        json_obj = json.loads(match.group(1))
        return json_obj

    # If not found, try to match with only backticks
    match = json_pattern_backticks_only.search(response_text)
    if match:
        json_obj = json.loads(match.group(1))
        return json_obj

def extract_number(text):
  return re.search(r'\d+', text).group()

def date_calculator(run_time, posted_at):
    from datetime import datetime, timedelta

    run_time_date = datetime.strptime(run_time, '%Y-%m-%d') # Convert run_time to a datetime object
    days_ago = int(re.search(r'\d+', posted_at).group()) # '21 days ago' há 2 dias

    calculated_date = run_time_date - timedelta(days=days_ago)

    return calculated_date.strftime('%Y-%m-%d')