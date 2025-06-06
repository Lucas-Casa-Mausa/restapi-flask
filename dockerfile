FROM python:3.13.3-alpine3.21

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY application/ application/
COPY wsgi.py config.py ./

CMD ["python3", "wsgi.py"]

