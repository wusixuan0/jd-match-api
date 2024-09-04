from .es_query import query_es, query_simple

def opensearch_get_jd_by_id(rank_id_list):    
    query = {
        "query": {
            "ids": {
                "values": rank_id_list
            }
        }
    }
    
    es_jd_list = query_es(query)
    return es_jd_list

def get_distinct_field(field):
    query = {
      "size": 0,
      "aggs": {
        "distinct_titles": {
          "terms": {
            "field": f"{field}.keyword",
            "size": 10000
          }
        },
        "title_count": {
          "cardinality": {
            "field": f"{field}.keyword",
          }
        }
      }
    }

    response = query_simple(query)

    distinct_count = response.get('aggregations').get('title_count').get('value')
    distinct_titles = response.get('aggregations').get('distinct_titles').get('buckets')
    print(f"number of distinct {field}: {distinct_count}")
    distinct_list = []
    for distinct in distinct_titles:
        key = distinct.get('key')
        doc_count = distinct.get('doc_count')
        print(f"{key} : {doc_count} document count")
        distinct_list.append(key)
        
    return distinct_list
