import os
from opensearchpy import OpenSearch
from api.services import send_log

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

    response = es_client.search(index=ES_JOB_INDEX, body=query)
    total_hits = response['hits']['total']['value']
    retried_doc = response['hits']['hits']
    # send_log(f"documents that match query criteria: {total_hits}")
    # send_log(f"number of retried documents: {len(retried_doc)}")
    return retried_doc