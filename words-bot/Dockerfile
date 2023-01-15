FROM python:3.10-alpine

WORKDIR /app/bot
COPY requirements.txt requirements.txt
RUN pip install -U pip && pip install -r requirements.txt --no-cache-dir
COPY . .

CMD ["python", "main.py"]