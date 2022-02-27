FROM python:3.10.2-buster

WORKDIR /app

ENV PORT=$PORT

EXPOSE $PORT

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD uvicorn main:api_local --host 0.0.0.0 --port $PORT
