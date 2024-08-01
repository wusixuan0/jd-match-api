```
touch django-api
cd django-api
# Create a virtual environment to isolate our package dependencies locally
python3 -m venv venv
source venv/bin/activate
pip install django djangorestframework && pip freeze > requirements.txt
// Create the Django project in the current directory
django-admin startproject config .
python manage.py startapp api
```

Your project structure should now look like this:
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
│   └── views.py
├── manage.py
├── venv/
└── requirements.txt
```

```
touch api/urls.py

```