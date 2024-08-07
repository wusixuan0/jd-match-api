def clean_text(text):
    # Remove HTML tags
    import re
    text = re.sub(r'<[^>]+>', '', text)

    # Remove markdown formatting
    text = re.sub(r'\*{1,2}|\_{1,2}|`{1,2}|~{1,2}|#{1,6}|>\s?|\[.*?\]\(.*?\)|!\[.*?\]\(.*?\)', '', text)

    # Remove non-printable characters and excessive whitespace
    import string
    printable = set(string.printable)
    text = ''.join(filter(lambda x: x in printable, text))
    text = ' '.join(text.split())

    return text

from datetime import datetime, timedelta
import re

def extract_number(text):
  return re.search(r'\d+', text).group()

def date_calculator(run_time, posted_at):
    run_time_date = datetime.strptime(run_time, '%Y-%m-%d') # Convert run_time to a datetime object
    days_ago = int(re.search(r'\d+', posted_at).group()) # '21 days ago' há 2 dias

    calculated_date = run_time_date - timedelta(days=days_ago)

    return calculated_date.strftime('%Y-%m-%d')