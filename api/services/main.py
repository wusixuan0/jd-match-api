from .process_resume import extract_resume

def resume_service(resume_url):
    return extract_resume(resume_url)