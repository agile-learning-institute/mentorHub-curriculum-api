# institute-curriculum-api

## Overview

The Institute Curriculum API is a Python API that facilitates CRUD operations for documents in the curriculum collection. It interacts with a MongoDB database. The API is built using the Flask web framework and the mongoengine library.

The OpenAPI specifications for the API can be found in the docs folder and served [here](mentorHub-curriculum-api/docs/index.html).

## Prerequisites

- Docker Desktop
- Python (latest version)
- Optional:
    - MongoDB Compass (for database visualization)

## Using the Database Container

For a local database setup with preloaded test data, refer to the instructions in the mentorHub repository's docker configurations.

## Install Dependencies and Run

f you've started the database separately, you can run the API locally by executing the following commands:

```
cd src
pip install -r requirements.txt
python3 main.py
```
## Build and Test the Container
```
docker-build.sh
```

## Local API Testing with CURL

GET /api/curriculum/{id}
```
curl http://localhost:8080/api/curriculum/123
```

PATCH /api/curriculum/{id}
```
curl -X PATCH http://localhost:8080/api/curriculum/123 -d '{"title":"New Title"}'
```

POST /api/curriculum/{id}/topic
```
curl -X POST http://localhost:8080/api/curriculum/123/topic -d '{"title":"New Topic"}'
```

PATCH /api/curriculum/{id}/{topic_id}
```
curl -X PATCH http://localhost:8080/api/curriculum/123/456 -d '{"title":"Updated Topic"}'
```

DELETE /api/curriculum/{id}/{topic_id}
```
curl -X DELETE http://localhost:8080/api/curriculum/123/456
```

GET /api/config/

```
curl http://localhost:8080/api/config/
```

GET /api/health/
```
curl http://localhost:8080/api/health/
```

## Postman Tests
GET /api/curriculum/{id}
- Method: GET
- Endpoint: http://localhost:8080/api/curriculum/123

PATCH /api/curriculum/{id}

- Method: PATCH
- Endpoint: http://localhost:8080/api/curriculum/123
- Body:

```
{
  "title": "New Title"
}
```

POST /api/curriculum/{id}/topic
- Method: POST
- Endpoint: http://localhost:8080/api/curriculum/123/topic
- Body:

```
{
  "title": "New Topic"
}
```

PATCH /api/curriculum/{id}/{topic_id}
- Method: PATCH
- Endpoint: http://localhost:8080/api/curriculum/123/456
- Body:

```
{
  "title": "Updated Topic"
}
```

DELETE /api/curriculum/{id}/{topic_id}
- Method: DELETE
- Endpoint: http://localhost:8080/api/curriculum/123/456

GET /api/config/
- Method: GET
- Endpoint: http://localhost:8080/api/config/

GET /api/health/
- Method: GET
- Endpoint: http://localhost:8080/api/health/
