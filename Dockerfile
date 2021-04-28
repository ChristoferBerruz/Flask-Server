# Pull debian buster image
FROM python:3.8-buster

# Upgrade pip
RUN pip install -U pip

# Copy requirements
COPY ./requirements.txt /tmp/

# Install requirements
RUN pip install -r /tmp/requirements.txt

# Copy application inside an /project directory
COPY . /project

# Make /app the workdir
WORKDIR /project

ENTRYPOINT ["gunicorn", "--worker-tmp-dir", "/dev/shm", "app:app"]