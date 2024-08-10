from .process_resume import extract_resume
from .es_query_resume import retrieve_jd_by_resume
from .match_and_rank import rank_result
from .es_query_jd_id import retrieve_jd_by_id
from .semantic_search import semantic_search
from .send_log import send_log
from .example_data import es_example, resume_summary_example
import os
from .send_log import send_log
import pdb

    
LOCAL_TEST = 'RENDER' not in os.environ

def resume_service(resume_url, version):
    send_log("This is a test log from main.py's resume_service")
    
    # pdb.set_trace()

    if not LOCAL_TEST:
        resume_summary = extract_resume(resume_url)
        es_query_resume = {
            "target job titles": resume_summary.get('target job titles'),
            "skills": resume_summary.get('skills'),
            "location": resume_summary.get('city'),
        }
        jd_by_id_dict = retrieve_jd_by_resume(es_query_resume, return_size=300, days_ago=7)
    else:
        resume_summary = resume_summary_example()
        # es_query_resume = {
        #     "target job titles": resume_summary.get('target job titles'),
        #     "skills": resume_summary.get('skills'),
        #     "location": resume_summary.get('city'),
        # }
        # jd_by_id_dict = retrieve_jd_by_resume(es_query_resume, return_size=100, days_ago=200)
        jd_by_id_dict = es_example()
    if version == "version2":
        filtered_jd_by_id_dict=semantic_search(jd_by_id_dict, resume_summary, k_splits=1000)
        rank_id_list = rank_result(resume_summary, filtered_jd_by_id_dict)
    if version == "version1":        
        rank_id_list = rank_result(resume_summary, jd_by_id_dict)

    ranked_jds=retrieve_jd_by_id(rank_id_list)
    return ranked_jds
