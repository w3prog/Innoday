.PHONY: install
install:
	pip install -r requirements/dev.txt

formatcode:
	black camunda worker

.PHONY: local-env
local-env:
	cd local-environment && docker-compose up --build

.PHONY: deploy-workflow
deploy-workflow:
	python3 send_workflow.py http://localhost:8080/engine-rest demo demo