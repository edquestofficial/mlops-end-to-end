# docker_setup

## Build a Docker Image
To build docker image use command
```bash
 docker build -t salary-api .
```

## Run a Docker Container
To run a Docker Container use
```bash
 docker run -it --salary_prediction -p 5005:5005 salary-api
```