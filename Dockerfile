FROM python:alpine3.7
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install psycopg2-binary
COPY . .
ENV FLASK_APP="app"
RUN pip install -r app/requirements.txt
EXPOSE 5000
ENTRYPOINT [ "flask", "run", "-h", "0.0.0.0", "-p", "5000"]