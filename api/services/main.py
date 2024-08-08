from .process_resume import extract_resume
from .es_query_resume import retrieve_jd
from .example_data import es_example, resume_summary_example, rank_example
from .match_and_rank import rank_result
from .es_query_jd_id import retrieve_jds

USE_API = True
USE_ES = True
USE_ES_FINAL = True

def resume_service(resume_url):
    if USE_API:
        resume_summary = extract_resume(resume_url)
    else:
        resume_summary=resume_summary_example()

    if USE_ES:
        es_query_data = {
            "target job titles": resume_summary.get('target job titles'),
            "skills": resume_summary.get('skills'),
            "location": resume_summary.get('city'),
        }

        jd_list = retrieve_jd(es_query_data)
        
    else:
        jd_list = es_example()

    if USE_API:
        rank_id_list=rank_result(resume_summary, jd_list)
    else:
        rank_id_list=rank_example()
    
    if USE_ES_FINAL:
        ranked_jds=retrieve_jds(rank_id_list)
    
    return ranked_jds