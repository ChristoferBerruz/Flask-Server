# Pull alpine version of python + nginx and uswgi
FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

# Define the minimum number of workers
ENV UWSGI_CHEAPER 1

# Define the maximum number of workers
ENV UWSGI_PROCESSES 2

# Dowload binaries for psycopg2 to work
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Upgrade pip
RUN pip install -U pip

# Install psycopg2 binaries
RUN pip install psycopg2-binary

# Copy requirements
COPY app/requirements.txt /tmp/


# Install requirements
RUN pip install -r /tmp/requirements.txt

# Copy application inside an /app directory
COPY . /app