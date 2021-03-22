# Documentation for Flask Server

## Project Structure

| Folder | Description
| --- | ------------ |
| app | Main folder for the flask server |
| app/database | Database related content. Includes db instance and models |
| app/api | REST api folder. |
| app/api/resources | Resources used by the REST api. Follows structure of a flask_restful app |

## Developing locally

1. Create a python virtual environment
2. Clone this repository
3. **Contact me so I can give you an ```.env``` file**. Place this file under the ```app/config``` folder.
4. Install dependencies using ```pip install -r app/requirements.txt```
    * The Pony ORM dependency uses psycopg2 which requires some native binaries. It ***might*** require
      installing those binaries
5. Run the flask server
    * (Linux) execute ```run-flask.sh``` script
    * (Windows) execute ```run-flask.ps1``` script

## Docker support - only Linux

If you just want to try the server, without modifying anything, build a docker container.

If you are using Windows, use WSL 2 to build and run the container.

### Building from source

**You need an ```.env``` file for the container to work.** Contact me and I will give you the credentials.

To build, simply run the script ```build-docker.sh```. It should execute without any problem

### Running the container

Simply run the ```run-docker.sh``` script.

## Dependencies

Notable dependencies are Flask, Flask Restful, and Pony ORM.
