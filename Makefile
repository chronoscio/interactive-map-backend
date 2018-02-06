DOCKER=docker
COMPOSE=docker-compose
APP_NAME="interactivemap"

# import config.
# You can change the default config with `make cnf="config_special.env" build`
cnf ?= prod.env
include $(cnf)
export $(shell sed 's/=.*//' $(cnf))

# import deploy config
# You can change the default deploy config with `make cnf="deploy_special.env" release`
dpl ?= deploy.env
include $(dpl)
export $(shell sed 's/=.*//' $(dpl))

# grep the version from the mix file
VERSION=$(shell ./bin/version.sh)

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help



# DOCKER TASKS

# Build the container
build: ## Build the release and develoment container. The development
	$(COMPOSE) build --no-cache $(APP_NAME)
	$(COMPOSE) run $(APP_NAME) grunt build
	$(DOCKER) build -t $(APP_NAME) .

image:
	$(DOCKER) build -t $(APP_NAME) .

run: stop ## Run container on port configured in `config.env`
	$(DOCKER) run -i -t --rm --env-file=./config.env -p=$(PORT):$(PORT) --name="$(APP_NAME)" $(APP_NAME)


dev: ## Run container in development mode
	$(COMPOSE) build --no-cache $(APP_NAME) && $(COMPOSE) run $(APP_NAME)

# Build and run the container
up: ## Spin up the project with the database
	$(COMPOSE) up --build

app: ## Spin up the project
	$(COMPOSE) up --build $(APP_NAME)

stop: ## Stop running containers
	$(DOCKER) stop $(APP_NAME)

rm: stop ## Stop and remove running containers
	$(DOCKER) rm $(APP_NAME)

clean: ## Clean the generated/compiles files
	echo "nothing clean ..."

# Docker release - build, tag and push the container
release: build publish ## Make a release by building and publishing the `{version}` ans `latest` tagged containers to ECR

# Docker publish
publish: repo-login publish-latest publish-version ## publish the `{version}` ans `latest` tagged containers to ECR

publish-latest: tag-latest ## publish the `latest` taged container to ECR
	@echo 'publish latest to $(DOCKER_REPO)'
	$(DOCKER) push $(DOCKER_REPO)/$(APP_NAME):latest

publish-version: tag-version ## publish the `{version}` taged container to ECR
	@echo 'publish $(VERSION) to $(DOCKER_REPO)'
	$(DOCKER) push $(DOCKER_REPO)/$(APP_NAME):$(VERSION)

# Docker tagging
tag: tag-latest tag-version ## Generate container tags for the `{version}` ans `latest` tags

tag-latest: ## Generate container `{version}` tag
	@echo 'create tag latest'
	$(DOCKER) tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest

tag-version: ## Generate container `latest` tag
	@echo 'create tag $(VERSION)'
	$(DOCKER) tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):$(VERSION)

version: ## output to version
	@echo $(VERSION)
