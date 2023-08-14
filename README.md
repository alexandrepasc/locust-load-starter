# locust-load-starter

run linter
`pycodestyle scripts/`

locust -t 1s -u 1 -f test.py --headless -H https://qa.ubp.ubiwhere.com --loglevel DEBUG --logfile asd

python scripts/generate_endpoints.py -f "/home/alex/Downloads/Urban Platform API (v3.36.0).yaml"

rm -r endpoints/