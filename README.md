# locust-load-starter
<!-- TOC -->
* [locust-load-starter](#locust-load-starter)
  * [Introduction](#introduction)
  * [Getting Started](#getting-started)
  * [Build and Test](#build-and-test)
<!-- TOC -->
## Introduction
## Getting Started
## Build and Test
run linter
`pycodestyle scripts/`

locust -t 1s -u 1 -f test.py --headless -H https://qa.ubp.ubiwhere.com --loglevel DEBUG --logfile asd

python scripts/generate_endpoints.py -f "/home/alex/Downloads/Urban Platform API (v3.36.0).yaml"

python scripts/generate_endpoints.py -f "/home/alex/Downloads/petstore.yaml"

rm -r endpoints/

https://github.com/OAI/OpenAPI-Specification/blob/main/examples/v3.0/petstore.yaml