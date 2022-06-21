FROM python:3

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./app /code/app
COPY ./localization /code/localization
COPY ./.env /code/.env

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN mkdir -p /code/logs/