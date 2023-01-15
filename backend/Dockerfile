FROM python:3.10-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -U pip && pip install -r requirements.txt
COPY . .
#CMD ["python", "manage.py", "runserver"]