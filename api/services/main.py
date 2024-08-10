from .extract_resume import extract_resume
from .es_query_resume import opensearch_get_jd_by_resume
from .match_and_rank import rank_result
from .semantic_search import semantic_search
from api.util.send_log import send_log
import pdb

def resume_service(resume_url, version, model_name, top_n=5):
    resume_summary = extract_resume(resume_url, model_name)
    jd_by_id_dict, es_retrived_document_list = opensearch_get_jd_by_resume(resume_summary, return_size=300, days_ago=7)

    if version == "version2":
        filtered_jd_by_id_dict=semantic_search(jd_by_id_dict, resume_summary)
        llm_ranked_id_list = rank_result(resume_summary, filtered_jd_by_id_dict, model_name, top_n, version)
    if version == "version1":        
        llm_ranked_id_list = rank_result(resume_summary, jd_by_id_dict, model_name, top_n, version)
    
    ranked_es_document_list = [item for item in es_retrived_document_list if item['_id'] in llm_ranked_id_list]
    return ranked_es_document_list