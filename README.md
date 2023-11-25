# locust-load-starter
<!-- TOC -->
* [locust-load-starter](#locust-load-starter)
  * [Introduction](#introduction)
  * [Getting Started](#getting-started)
  * [Build and Test](#build-and-test)
  * [Contribute](#contribute)
  * [Appendix](#appendix)
    * [Open API v3 yaml example](#open-api-v3-yaml-example)
    * [Helping commands](#helping-commands)
<!-- TOC -->
## Introduction
This repository aims to ease the creation of a load testing project by mapping the api automatically from the OpenAPI v3 
`yaml` or `json file.

Depending on the tests that will be done, the mapping of multiple requests can be cumbersome, reading the API documentation 
and mapping the required endpoints and parameters to the test project. The main idea here was to reduce that step and be 
able o ramp up the test creation.

This project is developed to use the [Locust](https://locust.io/) load testing framework, and all that will be generated 
by the script will use that framework. This can be used as the base for a new load testing project by just copying the 
content of this repository to the new repository base folder, since this is not done with a product in mind.

## Getting Started
To use this project install [Python](https://www.python.org/) and [pip](https://pip.pypa.io/en/stable/installation/). 
After that install the requirements using `pip` and the `requirements.txt` file (`pip install -r requirements.txt`).

After this we are set to go.

## Build and Test
To use this as a base for a new load testing project get the *spec* file (`.yml`, `.yaml` or `json`) from the API documentation, 
if using the Swagger template the `schema` url and/or a button to access the `schema` should be available.

Then execute the Python script `scripts/generate_endpoints.py` with the `-f` argument with the full path to the downloaded 
file. The script will create in the root of the project the `endpoints` folder and in it build the sub-folder with the files 
mapping the information retrieved in the *spec* file.
- `python scripts/generate_endpoints.py -h`
- `python scripts/generate_endpoints.py -f /full/path/doc.yml`

The sub-folders created will use the same structure as the API path, this was the easy way to organize the files and not 
keep all of them in the same folder.

For each endpoint it will create a sub-folder, in it a file with the name given in the *spec*, in the file a variable 
with the endpoint and a `class`. The `class` will have methods with the all the API methods, in them the locust 
implementation and the returning response.

```commandline
ENDPOINT = "/pets"


#  This class contains a list of the functions for this endpoint with all the
#  requests that were exported from the swagger spec file. To use this you
#  need to instantiate the class and pass the locust into it and after that we
#  are able to start to build the tests.
class Pets:
    #  Initialize the class with the locust instance.
    def __init__(self, loc: locust.user.users):
        self.loc = loc

    def get_listPets(self,
              params: dict[str, any] = None,
              headers: dict[str, any] = None,
              cookies: CookieJar = None,
              auth: tuple[str, str] = None,
              json: any = None,
              data: dict[str, any] = None,
              files: dict[str, any] = None,
              redirect: bool = False,
              verify: bool = True):

        response = self.loc.client.get(
            ENDPOINT,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            json=json,
            data=data,
            files=files,
            name="get_listPets",
            allow_redirects=redirect,
            verify=verify
        )

        return response
```

In case the endpoint method has parameter the `params` argument to the python method will be added as a file listing the 
parameters for that endpoint method.

```commandline
#  List of all the parameters exposed in the swagger file, with a comment
#  referring the type, that can be used when creating the test requests. The
#  name of this file is linked with a request function in the class of
#  this folder.
limit = "limit"  # integer
```

With this set we can create the locust `tasks` in a separated file and folder, instantiating the needed class and using 
the methods, with all the necessary arguments, to do the calls and build the load test(s).

Depending on the test(s) that will be used we could create a folder in the project (like `tasks`), in it the tasks using 
the generated methods and in the root project folder the test file calling the tasks created.

- `/tasks/example_task_1.py`
```commandline
from locust import TaskSet, task

from endpoints.pets.pets import Pets


class GetPetsList(TaskSet):
    @task
    def get_pets_list(self):
        pets: Pets = Pets(self)

        pets.get_listPets()

```

- `/tasks/example_task_2.py`
```commandline
from locust import TaskSet, task

from endpoints.pets.pets import Pets


class GetPetDetail(TaskSet):
    @task
    def get_pets_list(self):
        pets: Pets = Pets(self)

        pets.get_showPetById_id(id="pet_id")

```

- `/example_test.py`
```commandline
from locust import HttpUser

from tasks.example_task_1 import GetPetsList
from tasks.example_task_2 import GetPetDetail


class LoadTest(HttpUser):

    tasks = {
        GetPetsList: 1,
        GetPetDetail: 2
    }

```

There is another script in this repository called `run_tests.py`, this was created to be able to execute unattended tests, 
and be able to have the reports with some important information to help creating a manual report after. In cases that 
there is a necessity to execute multiple tests in a row and after the execution a manual report needs to be created with 
the summary of all the tests the timestamp, the users, time,... and all the locust reports is important. With this script 
all of this information will be in the `html` and `csv` files name automatically, without any need to set that when starting 
the test. This script will create the `reports` folder in the location where the script is located.
- `python run_tests.py -h`
- `python run_tests.py -u 50 -r 5 -t 5m -H https://asd.com -f /path/example_test.py`

## Contribute
This was done taking in consideration some of the obstacles that were felt during the creation and execution of load tests 
in a given environment, it will not be a tool to rule them all. So new contributions will be gladly accepted from the 
community.

To contribute, report a bug, or propose an improvement use an `Issue` to expose it and generate a discussion. Describe 
the best the idea, link relevant information, and in case there is already a branch with the change link it in the `Issue`.

Hope this helps!!!

## Appendix
### Open API v3 yaml example
```commandline
openapi: "3.0.0"
info:
  version: 1.0.0
  title: Swagger Petstore
  license:
    name: MIT
servers:
  - url: http://petstore.swagger.io/v1
paths:
  /pets:
    get:
      summary: List all pets
      operationId: listPets
      tags:
        - pets
      parameters:
        - name: limit
          in: query
          description: How many items to return at one time (max 100)
          required: false
          schema:
            type: integer
            maximum: 100
            format: int32
      responses:
        '200':
          description: A paged array of pets
          headers:
            x-next:
              description: A link to the next page of responses
              schema:
                type: string
          content:
            application/json:    
              schema:
                $ref: "#/components/schemas/Pets"
        default:
          description: unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
    post:
      summary: Create a pet
      operationId: createPets
      tags:
        - pets
      responses:
        '201':
          description: Null response
        default:
          description: unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
  /pets/{petId}:
    get:
      summary: Info for a specific pet
      operationId: showPetById
      tags:
        - pets
      parameters:
        - name: petId
          in: path
          required: true
          description: The id of the pet to retrieve
          schema:
            type: string
      responses:
        '200':
          description: Expected response to a valid request
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Pet"
        default:
          description: unexpected error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Error"
components:
  schemas:
    Pet:
      type: object
      required:
        - id
        - name
      properties:
        id:
          type: integer
          format: int64
        name:
          type: string
        tag:
          type: string
    Pets:
      type: array
      maxItems: 100
      items:
        $ref: "#/components/schemas/Pet"
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: integer
          format: int32
        message:
          type: string
```

### Helping commands
**Python linter**
- `pycodestyle scripts/`

**Execute generator**
- `python scripts/generate_endpoints.py -f "/home/path/Downloads/petstore.yaml"`

**Execute runner**
- `python run_tests.py -u 5 -r 5 -t 5m -f example_test.py -H https://domain.com`

**Locust execution**
- `locust -t 1s -u 1 -f example_test.py --headless -H https://domain.com --loglevel DEBUG --logfile asd`