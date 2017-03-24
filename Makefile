default: export DOCKER_ENDPOINT=tcp://192.168.122.2:4000
default:
	python dockerevent2rdf/run.py

requirements:
	pip install -r requirements.txt

consul:
	docker run -d -p 8500:8500 -h consul --name consul progrium/consul -server -bootstrap
