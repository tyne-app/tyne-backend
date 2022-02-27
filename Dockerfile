FROM python:3.10.2-buster

ENV PORT=$PORT

EXPOSE $PORT

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["uvicorn main:api_local --host 0.0.0.0 --port 8000"]
