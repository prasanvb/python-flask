# python-flask-smorest-ma

- flask-smorest automatically generates an OpenAPI documentation (formerly known as Swagger) for the API.
- marshmallow is an ORM/ODM/framework-agnostic library for converting complex datatypes, such as objects, to and from native Python datatypes.

## Initial Set up

1. `git clone <url>`
2. `python -m venv .venv` - initializes python virtual env for development on the current folder `.venv`
3. `pip install -r requirements.txt` - install project dependencies

**Note**: From the VS code Command Palette (cmf+shift+p) use the `Python: Select Interpreter` command to resolve any import issues

## Running the app

### Flask

- `flask run --port 3000` - to access local host *or* `flask --debug run --port 3000` - runs flask in watch mode

## Docker

- `docker images` - list all images
- `docker container ls -a`  or `docker ps -a` - list all containers and its details
- **Using Dockerfile**
    **Note**: Make sure docker is running before running these commands
  - `docker build -t python-flask-rest-api .` - create a image from the base python image
  - `docker run -d -p 3000:5000 --name rest-api-using-flask python-flask-rest-api` - spins up a container from image created
    or
  - `docker run -d -p 3000:5000 -w /app -v "$(pwd):/app" python-flask-rest-api` - runs the container in the watch mode
    - `-w /app` - creates a working directory inside the container (i.e.`WORKDIR /app`)
    - `-v "$(pwd):/app"` - creates a new volume and actively copies everything from local working directory to container working directory
    - `docker volume ls` - list volumes

- **Using Docker Compose**
**Note**: `docker compose up --build --force-recreate --no-deps [serviceNAME]` - forcefully builds new images and recreates the  container for the mentioned service
  - `docker compose up` - spins up a containers services from the `docker-compose.yml`  
  