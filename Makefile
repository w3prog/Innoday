.PHONY: install
install:
	pip install -r requirements/dev.txt

.PHONY: check_and_test
check-and-test:
	mypy camunda worker tests
	black --check camunda worker tests
	flake8
	tox
	#coverage report

formatcode:
	black camunda worker tests

.PHONY: lint
lint-bpmn:
	bpmnlint workflows/*/*.bpmn

.PHONY: dockerbuild
dockerbuild:
	docker build . -f docker/Dockerfile -t camundaworker

.PHONY: local-env
local-env:
	cd local-environment && docker-compose up --build

.PHONY: deploy-workflow
deploy-workflow:
	python3 send_workflow.py http://localhost:8080/engine-rest demo demo