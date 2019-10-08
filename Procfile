web: ( cd src && gunicorn --workers 2 core.wsgi:app --bind 0.0.0.0:$PORT )
release: python src/manage.py migrate
