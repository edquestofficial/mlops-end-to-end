# docker_setup

## Build a Docker Image
To build docker image use command
```bash
 docker build -t salary-api .
```

## Run a Docker Container
To run a Docker Container use
```bash
 docker run -it -p 5005:5005 salary-api
```


## Testing using CURL 
using this command, you can test your model.
```bash
curl -X 'POST' \
  'http://localhost:5005/predict/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "features": [
   [2.5, 5.0, 10]
  ]
}'
```