FROM python:3.10-alpine
ENV PYTHONBUFFERED=1

WORKDIR /app/bot
COPY requirements.txt requirements.txt
RUN pip install -U pip && pip install -r requirements.txt
COPY . .

CMD ["python", "main.py"]