#pull official base image
FROM python:3.10-alpine


#set work directory
WORKDIR /app


#set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# install psycopg2 dependancies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev
    # jpeg-dev zlib-dev

# install python dependancies
COPY requirements.txt /app/requirements.txt 
RUN pip install --upgrade pip 
RUN pip install -U setuptools
RUN pip install --no-cache-dir -r requirements.txt

#add app
COPY . .

    