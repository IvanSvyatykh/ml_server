FROM python:3.10.12

RUN mkdir /rfa_app

WORKDIR /rfa_app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg

COPY  . .

WORKDIR app

CMD gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 