FROM python:3.8

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN pip install uvicorn 

EXPOSE 8000

CMD uvicorn --interface wsgi app:app --host 0.0.0.0