FROM python:3.10.2-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY . .

CMD uvicorn main:api_local
