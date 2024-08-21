# curriculum-api

## Overview

This is a simple Flask API that provides Get/Post/Patch services for docuements in the Curriculum collection. This API uses data from a [backing Mongo Database](https://github.com/agile-learning-institute/mentorHub-mongodb), and supports a [Single Page Application.](https://github.com/agile-learning-institute/mentorHub-curriculum-ui)

The OpenAPI specifications for the api can be found in the ``docs`` folder, and are served [here](https://agile-learning-institute.github.io/mentorHub-curriculum-api/)

## Prerequisits

- [Mentorhub Developer Edition](https://github.com/agile-learning-institute/mentorHub/blob/main/mentorHub-developer-edition/README.md)
- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

### Optional

- [Mongo Compass](https://www.mongodb.com/try/download/compass) - if you want a way to look into the database

## Install Flask Dependencies

```bash
pipenv install
```

## Run the API locally

```bash
pipenv run local
```
Serves up the API locally with a backing mongodb database, ctrl-c to exit

## Run Unit Testing

```bash
pipenv run test
```

## Run StepCI black box end-2-end testing

```bash
pipenv run stepci
```

## Build and run the API Container

```bash
pipenv run container
```

This will build the new container, and start the mongodb and API container ready for testing. 

## API Testing with CURL

If you want to do more manual testing, here are the curl commands to use

### Test Health Endpoint

This endpoint supports the promethius monitoring standards for a healthcheck endpoint

```bash
curl http://localhost:8088/api/health/

```

### Test Config Endpoint

```bash
curl http://localhost:8088/api/config/

```

### Test get a Curriculum

```bash
curl http://localhost:8088/api/curriculum/AAAA00000000000000000001/
```

### Test add a Resource to a Curriculum

```bash
curl -X POST http://localhost:8088/api/curriculum/AAAA00000000000000000001/ \
     -d '{"sequence":100, "roadmap":"Later"}'

```

### Test update a Resource

```bash
curl -X PATCH http://localhost:8088/api/curriculum/AAAA00000000000000000001/100 \
     -d '{"path":"Some Path"}'

```

### Test delete a Resource

```bash
curl -X DELETE http://localhost:8088/api/curriculum/AAAA00000000000000000001/100 

```

## Observability and Configuration

The ```api/config/``` endpoint will return a list of configuration values. These values are either "defaults" or loaded from an Environment Variable, or found in a singleton configuration file of the same name. Configuration files take precidence over environment variables. The variable "CONFIG_FOLDER" will change the location of configuration files from the default of ```./```

The ```api/health/``` endpoint is a Promethius Healthcheck endpoint.

The [Dockerfile](./Dockerfile) uses a 2-stage build, and supports both amd64 and arm64 architectures. See [docker-build.sh](./src/docker/docker-build.sh) for details about how to build in the local architecture for testing, and [docker-push.sh] for details about how to build and push multi-architecture images.
