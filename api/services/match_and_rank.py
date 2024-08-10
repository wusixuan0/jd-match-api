import google.generativeai as genai
import os
from api.util.utils import extract_json_from_response
from api.util.gemini_api_request import requestGeminiAPI
from api.util.send_log import send_log

GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

def rank_result(resume_summary, jd_by_id_dict, model_name, top_n, version):
    send_log(f">>>Starting to assess, match and rank your resume with filtered job descriptions by Gemini API")
    rank_result_llm = match_and_rank(resume_summary, jd_by_id_dict,model_name, top_n, version)
    rank_result = extract_json_from_response(rank_result_llm)
    return rank_result

def match_and_rank(resume_summary, job_summaries, model_name, top_n=5, version='version1'):
    prompt = f"""
    Given a resume summary and dictionary of {len(job_summaries)} job description where keys are unique job IDs and values are summaries. {'The job descriptions in dictionary is pre-ranked by semantic search, but the ranking is not context aware.' if version == 'version2' else ''}
    Rank the top {top_n} matches of job summaries based on qualification and suitability to the resume.
    Output an array ONLY of job IDs (as provided in the input) in descending order of the qualitative match, in the following format: [job_id_1, job_id_2, job_id_3, ...]
    Output example: [List of job IDs (as provided in the input) in a JSON array format]
    Prioritize matching accuracy, context awareness, preference handling.
    """
    match_data = f"""
        resume summary:{resume_summary}
        job summaries:{job_summaries}
    """
    send_log(f"Gemini API Request Prompt: \n{prompt}")
    send_log(f"match data in Gemini API pay load has {len(match_data)} character.")
    pay_load = prompt + match_data
    response_data = requestGeminiAPI(pay_load, model_name)
    return response_data