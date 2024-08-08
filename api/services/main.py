from .process_resume import extract_resume
from .es_query_resume import retrieve_jd
from .match_and_rank import rank_result
from .es_query_jd_id import retrieve_jds

USE_API = False

def resume_service(resume_url):
    if USE_API:
        resume_summary = extract_resume(resume_url)

        es_query_data = {
            "target job titles": resume_summary.get('target job titles'),
            "skills": resume_summary.get('skills'),
            "location": resume_summary.get('city'),
        }

        jd_list = retrieve_jd(es_query_data)
        rank_id_list=rank_result(resume_summary, jd_list)
    else:
        rank_example = [
            "QC85LpEBIvxPMcUyAMOd",
            "Qy85LpEBIvxPMcUyAMOd",
            "RC85LpEBIvxPMcUyAMOd",
            "Ri85LpEBIvxPMcUyAMOd",
            "SC85LpEBIvxPMcUyAMOd"
        ]
        rank_id_list=rank_example
    
    ranked_jds=retrieve_jds(rank_id_list)
    
    return ranked_jds