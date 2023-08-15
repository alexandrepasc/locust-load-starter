# locust-load-starter
<!-- TOC -->
* [locust-load-starter](#locust-load-starter)
  * [Introduction](#introduction)
  * [Getting Started](#getting-started)
  * [Build and Test](#build-and-test)
<!-- TOC -->
## Introduction
This repository aims to ease the creation of a load testing project by mapping the api automatically from the OpenAPI v3 `yaml` file.

Depending on the tests that will be done, the mapping of multiple requests can be cumbersome, reading the API documentation and mapping 
the required endpoints and parameters to the test project. The main idea here was to reduce that step and be able o ramp 
up the test creation.

This project is developed to use the [Locust](https://locust.io/) load testing framework, and all that will be generated 
by the script will use that framework. This can be used as the base for a new load testing project by just copying the 
content of this repository to the new repository base folder, since this is not done with a product in mind.
## Getting Started
## Build and Test
run linter
`pycodestyle scripts/`

locust -t 1s -u 1 -f test.py --headless -H https://qa.ubp.ubiwhere.com --loglevel DEBUG --logfile asd

python scripts/generate_endpoints.py -f "/home/alex/Downloads/Urban Platform API (v3.36.0).yaml"

python scripts/generate_endpoints.py -f "/home/alex/Downloads/petstore.yaml"

rm -r endpoints/

https://github.com/OAI/OpenAPI-Specification/blob/main/examples/v3.0/petstore.yaml