FROM python:3.10-alpine

WORKDIR /app/backend
COPY requirements.txt requirements.txt
RUN pip install -U pip && pip install -r requirements.txt --no-cache-dir
COPY . .

CMD ["python", "manage.py", "runserver"]