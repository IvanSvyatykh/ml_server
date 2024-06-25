FROM python:3.10.12

COPY  . .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg

CMD python -m uvicorn main:app --host 0.0.0.0 --port 8000