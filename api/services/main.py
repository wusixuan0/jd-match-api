from .extract_resume import extract_resume
from .es_query_resume import opensearch_get_jd_by_resume
from .match_and_rank import rank_result
from .semantic_search import semantic_search
from api.util.send_log import send_log
from api.util.es_query_jd_id import opensearch_get_jd_by_id
import os

TEST = 'RENDER' not in os.environ
def employer_service(pdf_url, version="version1", model_name, top_n=5):
    job_summary = extract_resume(resume_data, model_name, is_resume=False)

def resume_service(resume_data, version, model_name, is_url=True, top_n=5):
    if TEST:
        # if is_url:
        #     resume_summary = extract_resume(resume_data, model_name)
        # else:
        #     resume_summary = resume_data
        send_log("test")
        ranked_ids=["YS8jTZEBIvxPMcUySMeb", "Gi9JUpEBIvxPMcUyA8jQ", "_i9iM5EBIvxPMcUyymMPQ", "hi-EOJEBIvxPMcUyXMRA", "yC_7R5EBIvxPMcUyz8ah"]
        ranked_es_document_list=opensearch_get_jd_by_id(ranked_ids)

        return {
            "resume_summary": "resume_summary",
            "ranked_ids": ranked_ids,
            "ranked_docs": ranked_es_document_list,
        }
    if is_url:
        resume_summary = extract_resume(resume_data, model_name, is_resume=True)
    else:
        resume_summary = resume_data
    
    jd_by_id_dict, es_retrived_document_list = opensearch_get_jd_by_resume(resume_summary, return_size=300, days_ago=7)

    if version == "version2":
        filtered_jd_by_id_dict=semantic_search(jd_by_id_dict, resume_summary)
        llm_ranked_id_list = rank_result(resume_summary, filtered_jd_by_id_dict, model_name, top_n, version)
    if version == "version1":        
        llm_ranked_id_list = rank_result(resume_summary, jd_by_id_dict, model_name, top_n, version)
    
    ranked_es_document_list = [next(item for item in es_retrived_document_list if item['_id'] == jd_id) for jd_id in llm_ranked_id_list]
    return {
        "resume_summary": resume_summary,
        "ranked_ids": llm_ranked_id_list,
        "ranked_docs": ranked_es_document_list,
    }