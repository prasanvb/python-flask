# python-flask-smorest-jwt

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
  

## NOTES

### JWT SIGNING
- jwt signing we need "algorithm", "payload" and "secret"
  - Sample `HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload), secret)`
- `flask_jwt_extended.create_access_token(identity=username)`
  - Adds header `{  "alg":"HS256",  "typ":"JWT"  }`
  - Adds payload ```{"fresh": false, "iat":1721799720, "jti":"f8cdc3fa-d440-45c1-af88-70549eb6909f", "type":"access", "sub":"prasan", "nbf":1721799720, "csrf":"2a8e3e33-dc0d-4054-896c-90577fe3713f", "exp":1721800620  }```
  - *NOTE:* `jti` json token identifier

### JWT VALIDATION
- `@jwt_required()` if added to a route then need to pass authorization header `authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.NDgyNS1iYzMwLTcyY2EyNjlhYmJlNSIsImV4cCI6MTcyMTg3OTg3NX0.FDeE5T-Nk5sx6Ltwiy1mxhzKTTkoUpYR19ueW6hAYCE`
- 