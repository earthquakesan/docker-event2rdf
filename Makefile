default: export DOCKER_ENDPOINT=tcp://192.168.122.2:4000
default: export TIMEZONE=Europe/Berlin
default: export VIRTUOSO_ENDPOINT=http://localhost:8890/sparql-auth
default: export DBA_USERNAME=dba
default: export DBA_PASSWORD=dba
default: export DEFAULT_GRAPH_URI=http://example.com/
default:
	python dockerevent2rdf/run.py

requirements:
	sudo apt-get install -y unixodbc-dev
	pip install -r requirements.txt

consul:
	docker run -d -p 8500:8500 -h consul --name consul progrium/consul -server -bootstrap

virtuoso:
	docker run --name my-virtuoso \
		-p 8890:8890 -p 1111:1111 \
		-e DBA_PASSWORD=dba \
		-e SPARQL_UPDATE=true \
		-e DEFAULT_GRAPH=http://ontology.aksw.org/dockevent \
		-v $(shell pwd)/virtuoso/db:/data \
		-d tenforce/virtuoso

test: export VIRTUOSO_ENDPOINT=http://localhost:8890/sparql-auth
test: export DBA_USERNAME=dba
test: export DBA_PASSWORD=dba
test: export DEFAULT_GRAPH_URI=http://example.com/
test:
	python -m unittest tests/dockerevent2rdf/virtuoso_connector_test.py
