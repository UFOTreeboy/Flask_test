FROM python:3.9.6-buster

ENV ACCEPT_EULA=Y

EXPOSE 8888

WORKDIR /chatterbot-testing
ADD . /chatterbot-testing

RUN apt-get update && apt-get install -y \
    freetds-bin \
    freetds-common \
    freetds-dev

RUN pip install -U pip
RUN pip install pymssql
RUN pip install -r requirements.txt


CMD [ "python", "app.py"]