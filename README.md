https://jd-match.netlify.app/  
quick start
```
source venv/bin/activate
doppler run -- python manage.py runserver
```  
add new env var to doppler: https://dashboard.doppler.com/workplace/87fa3aecaa170026448c/projects/django-api/configs/dev  
```
python manage.py makemigrations
doppler run -- python manage.py migrate
```
```
pip freeze > requirements.txt
```
```
import pdb
pdb.set_trace()
```
running with Gunicorn for render.
```
doppler run -- python -m gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
```
get started
```
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export DATABASE_URL=
export DOPPLER_TOKEN=
doppler run -- python manage.py runserver
``` 
doppler get started: https://github.com/wusixuan0/seed-supabase/blob/main/README.md  
environment variables in this project (incomplete):
echo $DATABASE_URL
echo $OPENSEARCH_USERNAME_HOST 
echo $OPENSEARCH_USERNAME 
echo $OPENSEARCH_PASSWORD 
echo $GOOGLE_API_KEY  
#### Thought Process  
steps:  
1. extract_resume function: One API call to Gemini API
2. OpenSearch (ES) query: Retrieve 60 job descriptions based on extracted resume data.
3. Rank by Gemini API, returns list of id
4. Retrieve OpenSearch full records with list of id

api structure   
```
my-project/
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── services # script for assess, match and rank jd
│   ├── utils # helper functions
│   ├── serializers.py  
│   └── urls.py      
├── manage.py
├── venv/
└── requirements.txt
```  
1. Extract the resume and save the API response to resume_summary in the model.
2. Perform the OpenSearch query and Gemini API call, saving the returned response to job_id_list in the model.
3. Retrieve OpenSearch full records with the list of IDs and send back the response.

#### api structure summary before adding match script  
model.py:    
MatchRecord model with fields resume_summary, job_id_list, created_at, updated_at

views.py:  
Import generics and define MatchRecordCreateView

serializers.py:
Define MatchRecordSerializer

urls.py (app level):  
Define urlpatterns for MatchRecordCreateView

urls.py (project level):  
Include the app's URLs