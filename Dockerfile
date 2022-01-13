FROM python:3.9.6-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE $PORT

COPY . .

CMD ["uvicorn src/main:api_local --host 0.0.0.0 --port $PORT"]
