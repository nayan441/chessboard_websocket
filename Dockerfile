# pull the official base image
FROM python:3

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN pip install --upgrade pip

WORKDIR /usr/src/app
RUN mkdir app
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt
COPY . /usr/src/app
EXPOSE 8040
# RUN rm -rf db.sqlite3
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
