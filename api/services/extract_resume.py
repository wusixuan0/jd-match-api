from api.util.utils import clean_text, extract_json_from_response
from langchain_community.document_loaders import PyMuPDFLoader
from api.util.send_log import send_log
from api.util.gemini_api_request import requestGeminiAPI
from api.models import GeneratedResume
import json

def extract_resume(pdf_url, model_name, is_resume=True):
    if is_resume:
        send_log(">>>Starting to extract resume data")
    else:
        send_log(">>>Starting to extract job description data")
    resume_text = load_pdf(pdf_url)
    response = summarize_and_infer(resume_text, model_name='gemini-1.5-flash', is_resume=is_resume)
    resume_summary = extract_json_from_response(response)
    return resume_summary
    
def summarize_and_infer(resume_text, model_name, is_resume=True):
    resume_title="target job titles"
    jd_title="job title"
    resume_title_instruction="list of DISTINCT target roles that align with the candidate's skills and experience. Do not include job title prefix e.g. senior."
    
    jd_requirement="Identify core responsibilities and duties of the role. Identify minimum educational requirements and preferred experience and level."
    resume_qualification="Include education, key responsibilities from past experience, and other relevant qualifications. Identify candidate's experience level."

    resume_preference = "schedule, company culture, location"
    jd_preference = "schedule, location (on-site, hybrid, remote, city/region), and company culture (values, work environment, team dynamics)"

    resume_career_goal = "- career goal: future roles, skills, and long-term vision based on job progression, skills & experience, projects & accomplishments, education & certifications"
    jd_growth_potential = "- growth potential: assess the job's growth potential and how well the role aligns with typical career path and industry fit. For junior role: Look for collaborative environments, clear career paths, and roles with varied tasks for skill development. Mid-Level: Seek opportunities for increased responsibility, specialized skill development, and high-impact projects with recognition. Senior: Focus on leadership roles, strategic impact on business goals, and autonomy to drive innovation within the organization."

    string_type = ""
    json_schema = {}
    json_schema[resume_title if is_resume else jd_title] = string_type

    for field in ["skills", "qualifications", "city", "preferences"]:
        json_schema[field] = string_type

    json_schema["career goal" if is_resume else "growth potential"] = string_type

    json_schema_string = json.dumps(json_schema, indent=4)

    prompt = f"""
    Analyze this {'resume' if is_resume else 'job description'}. 
    Return a JSON object using this schema (If information for a field is not available or cannot be inferred, do not return the field):
    {json_schema_string}
    Fields to extract/infer:
    - { resume_title if is_resume else jd_title }: { resume_title_instruction if is_resume else '' }
    - skills: {"Identify relevant technical skills." if is_resume else "Identify required and preferred skills"}
    - qualifications: { resume_qualification if is_resume else jd_requirement}
    {"- city: Include city name ONLY" if is_resume else "- location: "}
    - preferences: { resume_preference if is_resume else jd_preference }
    { resume_career_goal if is_resume else jd_growth_potential}
    {'resume' if is_resume else 'job description'} text:
    """
    request_payload = prompt + resume_text
    send_log(f"Gemini API Request Payload: \n{request_payload}")
    response_data = requestGeminiAPI(request_payload, model_name)
    return response_data

def load_pdf(url):
    loader = PyMuPDFLoader(url)
    docs = loader.load()
    full_text = " ".join(doc.page_content for doc in docs)
    return clean_text(full_text)