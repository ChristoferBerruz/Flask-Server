# Documentation for Flask Server

## Swagger documentation

The swagger documentation can be found at ```/swagger```

## Project Structure

| Folder | Description
| --- | ------------ |
| app | Main folder for the flask server |
| app/database | Database related content. Includes db instance and models |
| app/api | REST api folder. |
| app/api/resources | Resources used by the REST api. Follows structure of a flask_restful app |

## Developing locally

### Environment variables

For this to run, you need the following environment variables set up:

* ```JWT_SECRET_KEY```
* ```DB_HOST```
* ```REDIS_HOST```
* ```DB_PORT```
* ```DB_USER```
* ```DB_PASSWORD```

### Steps

1. Create a python virtual environment
2. Clone this repository
3. Set environment variables or place them in an ```.env``` file file under the ```app/config``` folder.
4. Install dependencies using ```pip install -r app/requirements.txt```
    * The Pony ORM dependency uses psycopg2 which requires some native binaries. It ***might*** require
      installing those binaries
5. Run the flask server
    * (Linux) execute ```run-flask.sh``` script
    * (Windows) execute ```run-flask.ps1``` script

## Docker support - only Linux

If you just want to try the server, without modifying anything, build a docker container.

If you are using Windows, use WSL 2 to build and run the container.

### Download from DockerHub

Pull the docker image from DockerHub using the following

```docker pull cberruz/cleanhands-flask-server```

### Building from source

To build, simply run the script ```build-docker.sh```. It should execute without any problem

### Running the container

Make sure to have all environment variables defined above. Otherwise, the container won't run properly.

If you built the container from source with an ```.env``` in it, simply run the ```run-docker.sh``` script. Otherwise, describe the environment variables while using the ```docker run``` command.

## Dependencies

Notable dependencies are:

* Flask
* Flask-restful
* Marshmallow
* Pony ORM
* Redis
* JWT-Extended
