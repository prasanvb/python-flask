# python-flask project

## Initial Set up

1. `git clone <url>`
2. `python -m venv .venv` - initializes python virtual env for development on the current folder `.venv`
3. `pip install -r requirements.txt` - install project dependencies
4. `flask run` - to access local host *or* `flask --debug run` - runs flask in watch mode 


**Note**: From the VS code Command Palette (cmf+shift+p) use the `Python: Select Interpreter` command to resolve any import issues

## Docker set up

**Note**: Make sure docker is running before running these commands

1. `docker build -t python-flask-rest-api .` - create a image from the base python image
2. `docker run -d -p 3000:5000 --name rest-api-using-flask python-flask-rest-api` - spins up a container from image created
3. `docker container ls  or docker ps`  - list of running containers and its details
4. `docker compose up` - spins up a containers services from the `docker-compose.yml`

**Note**: `docker compose up --build --force-recreate --no-deps [serviceNAME]` - forcefully builds new images and recreates the  container for the mentioned service
