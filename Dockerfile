FROM python:3.12.4
EXPOSE 5000
# create a folder and naivigate to path inside the docker container
WORKDIR /app 
# COPY sourcePath destPath 
# unless the requirements.txt changes COPY and RUN will not be execute, so its much faster 
COPY requirements.txt .
RUN pip install -r requirements.txt
# COPY sourcePath destPath 
# sourcePath . denotes copy everything from current folder (i.e. Dockerfile folder)
# destPath . denotes copy everything to current folder (i.e. /app folder)
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0" ]