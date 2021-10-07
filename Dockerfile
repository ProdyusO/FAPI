FROM python:3.9

RUN apt update

#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src
WORKDIR /usr/src

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./src .

EXPOSE 8000
