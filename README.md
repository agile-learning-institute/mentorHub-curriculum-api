# curriculum-api

## Overview

This is a simple Flask API that provides Get/Post/Patch services for documents in the Curriculum collection. This API uses data from a [backing Mongo Database](https://github.com/agile-learning-institute/mentorHub-mongodb), and supports a [Single Page Application.](https://github.com/agile-learning-institute/mentorHub-curriculum-ui)

The OpenAPI specifications for the api can be found in the ``docs`` folder, and are served [here](https://agile-learning-institute.github.io/mentorHub-curriculum-api/)

## Prerequisites

- [Mentorhub Developer Edition](https://github.com/agile-learning-institute/mentorHub/blob/main/mentorHub-developer-edition/README.md)
- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

### Optional

- [Mongo Compass](https://www.mongodb.com/try/download/compass) - if you want a way to look into the database

## Install Dependencies

```bash
pipenv install
```

## Run Unit Testing

```bash
pipenv run test
```
NOTE: This excludes the tests with a backing service i.e. testbacking_mentorhub_mongo_io.py which can be run in vscode with the mongodb backing database running. 

## {re}start the containerized database and run the API locally

```bash
pipenv run start
```

## Run the API locally (assumes database is already running)

```bash
pipenv run local
```

## Build and run the API Container

```bash
pipenv run container
```

This will build the new container, and {re}start the mongodb and API container.

## Run StepCI end-2-end testing
NOTE: Assumes the API is running at localhost:8088

```bash
pipenv run stepci
```

## Run StepCI load testing
NOTE: Assumes the API is running at localhost:8088

```bash
pipenv run load
```

# Project Layout
- ``/src`` this folder contains all source code
- ``/src/server.py`` is the main entrypoint, which initializes the configuration and registers routes with Flask
- ``/src/config/Config.py`` is the singleton config object that manages configuration values and acts as a cache for enumerators and other low volatility data values.
- ``/src/models`` contains helpers related to creating transactional data objects such as breadcrumbs or RBAC tokens
- ``/src/routes`` contains Flask http request/response handlers
- ``/src/services`` service interface that wraps database calls with RBAC, encode/decode, and other business logic
- ``/src/utils/mentorhub_mongo_io.py`` is a singleton that manages the mongodb connection, and provides database io functions to the service layer. 
- ``/test`` this folder contains unit testing, and testing artifacts. The sub-folder structure mimics the ``/src`` folder

# API Testing with CURL

If you want to do more manual testing, here are the curl commands to use

### Test Health Endpoint

This endpoint supports the Prometheus monitoring standards for a healthcheck endpoint

```bash
curl http://localhost:8088/api/health/

```

### Test Config Endpoint

```bash
curl http://localhost:8088/api/config/

```

### Test get or create a Curriculum

```bash
curl http://localhost:8088/api/curriculum/{_id value}
```

### Test update a Curriculum

```bash
curl -X PATCH http://localhost:8088/api/curriculum/{_id value} \
     -d '{"now":"[]"}'

```

### Test delete a Curriculum

```bash
curl -X DELETE http://localhost:8088/api/curriculum/{_id value} 
```

## Observability and Configuration

The ```api/config/``` endpoint will return a list of configuration values. These values are either "defaults" or loaded from a singleton configuration file, or an Environment Variable of the same name. Configuration files take precedence over environment variables. The environment variable "CONFIG_FOLDER" will change the location of configuration files from the default of ```./```

The ```api/health/``` endpoint is a [Prometheus](https://prometheus.io) Health check endpoint.

The [Dockerfile](./Dockerfile) uses a 2-stage build, and supports both amd64 and arm64 architectures. 
