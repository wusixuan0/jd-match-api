import os
from opensearchpy import OpenSearch
import time
from datetime import datetime
from .send_log import send_log

def query_es(query):
    host = os.environ.get('OPENSEARCH_USERNAME_HOST')
    if not host:
        raise ValueError("OPENSEARCH_USERNAME_HOST environment variable is not set")

    auth = (os.environ.get('OPENSEARCH_USERNAME'), os.environ.get('OPENSEARCH_PASSWORD'))
    if not all(auth):
        raise ValueError("OPENSEARCH_USERNAME or OPENSEARCH_PASSWORD environment variables are not set")

    es_client = OpenSearch(
        hosts = [{'host': host, 'port': 443}],
        http_compress = True,
        http_auth = auth,
        use_ssl = True,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
    )

    ES_JOB_INDEX = 'swifthire_jobs_dev'
    
    start_time = time.time()
    start_time_datetime = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
    send_log(f"OpenSearch query start at {start_time_datetime}")
    send_log(f"OpenSearch query: {str(query)}")
    response = es_client.search(index=ES_JOB_INDEX, body=query)
    end_time = time.time()
    duration = end_time - start_time
    total_hits = response['hits']['total']['value']
    retrived_doc = response['hits']['hits']
    
    send_log(f"OpenSearch Request Duration: {duration} seconds")
    send_log(f"documents that match query criteria: {total_hits}")
    send_log(f"<<<number of retrived documents: {len(retrived_doc)}")
    return retrived_doc