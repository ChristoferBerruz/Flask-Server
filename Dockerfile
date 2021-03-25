# Pull python running in an alpine linux distro
FROM python:alpine3.7

# Install OS packages for psycopg2 to work
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Install native psycopg2 binaries
RUN pip install psycopg2-binary

# Copy working directory
COPY . .

# Set environment for flask to run
ENV FLASK_APP="app"

# Install python requirements using pip
RUN pip install -r app/requirements.txt

# Expose ports to other containers
EXPOSE 5000

# Define command to execute once container is up
ENTRYPOINT [ "flask", "run", "-h", "0.0.0.0", "-p", "5000"]