from api.util.es_query import query_es

def retrieve_jd_by_id(rank_id_list):    
    query = {
        "query": {
            "ids": {
                "values": rank_id_list
            }
        }
    }
    
    es_jd_list = query_es(query)
    return es_jd_list