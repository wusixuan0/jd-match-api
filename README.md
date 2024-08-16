https://jd-match.netlify.app/  
quick start
```
source venv/bin/activate
doppler run -- uvicorn config.asgi:application --workers 1
```  
add new env var to doppler: https://dashboard.doppler.com/workplace/87fa3aecaa170026448c/projects/django-api/configs/dev  
```
doppler run -- python manage.py email
python manage.py makemigrations
doppler run -- python manage.py migrate
doppler run -- python manage.py migrate api zero
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
### Thought Process  
#### version 2 addition of semantic search:  
Goal: filter more jd before final match&rank by LLM.  
Step 1: split and embed jd in vectorestore  
Split and Embed:  
- Job descriptions(JDs) are splitted into smaller, manageable pieces(jd chunks) to facilitate comparison.
- embed each jd chunk, save its OpenSearch ID in embedding's metadata for identificaton later.
- Save jd chunk embeddings to vectorstore for search
Similarity Search:  
- Two separate searches are performed within the vectorstore:
  - all qualifications info from resume summary
  - career goals from resume summary
- Each search produces a ranked list of relevant jd chunks based on similarity in vector space.

Ranking & Combining Search Results:
- Goal: I need to combine two ranked list of jd chunks, produce a overall ranked jd (not chunks).
- group jd chunks back together based on their job IDs (stored in metadata).
- scoring formula explain:
  - RRF combines rankings from multiple sources into a single, unified ranking. In my case it's two queries for qualification and career goal.
  - why use RRF: similarity score from different libaries are not normalized. instead of producing a final rank list by combining similarity scores from jd chunks, RRF makes it simplier.
  - RRF score = sum(1 / (k + rank_i))  
  - rank_i is the position of the chunk in the list for query i
  - since qualification and career goal have different importance in resume jd match, I added weights to this formula: RRF score = weight_for_the_query * sum(1 / (k + rank_i)) 
  - k is 60 because experimentally observed to perform best


#### Benefit of addition of semantic search:  
- Open Search can’t match paragraph
- even though semantic/similarity search of embedding is not context aware, it solves LLM’s context window limitation  

#### parameter decisions:  
In similarity search, I need to decide on how many top similar jd chunks to retrieve for each field.  
factor:  
- Estimate the average number of chunks per jd from: Raw jd lengths and `chunk_size` `chunk_overlap`

One JD example: 1,199 words 7,794 characters
1. `chunk_size`: 800 characters
    - This is roughly half the length of average JD summary.
    - It's large enough to capture significant portions of each JD without splitting them into too many pieces.
    - With 800 characters, example JD (7,794 characters) would result in about 10 chunks.
2. `chunk_overlap`: 100 characters

#### version 1 LLM only steps:  
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
│   ├── routing.py
│   ├── consumers.py
│   ├── views.py
│   ├── services # script for assess, match and rank jd
│       ├── main.py
│       ├── match_and_rank.py
│       ├── more
│       ├── more
│   ├── utils # helper functions
│       ├── utils.py
│       ├── es_query.py
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