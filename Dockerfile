FROM python:3.10.2-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["uvicorn hola:api_local --host 0.0.0.0 --port $PORT"]
