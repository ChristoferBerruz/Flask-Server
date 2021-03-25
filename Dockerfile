# Pull alpine version of python
FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

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