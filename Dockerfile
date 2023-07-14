FROM python:3
COPY requirements.txt /code/
COPY .env /code/

WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt && apt-get update

COPY . /code/

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
