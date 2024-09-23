FROM python:3.12

ADD . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD python3 -m uvicorn api:app --reload
