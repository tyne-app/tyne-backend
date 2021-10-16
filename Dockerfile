FROM python:3.9.6-buster

ENV CREATE_ACCOUNT_INTEGRATION = https://ms-integration-apis.herokuapp.com/v1/login
ENV VALIDATE_ACCOUNT_INTEGRATION = https://ms-integration-apis.herokuapp.com/v1/login/validate
ENV DELETE_ACCOUNT_INTEGRATION = https://ms-integration-apis.herokuapp.com/v1/login
ENV CREATE_ACCOUNT_LOCAL = https://backbone-locals.herokuapp.com/v1/local/register
ENV DELETE_ACCOUNT_LOCAL = https://backbone-locals.herokuapp.com/v1/local
ENV MAPBOX_URL = https://ms-integration-apis.herokuapp.com/v1/mapbox/getLatitudeLongitude

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE $PORT

COPY . .

CMD ["uvicorn main:api --host 0.0.0.0 --port $PORT"]
