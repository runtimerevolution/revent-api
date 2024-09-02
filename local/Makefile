# Makefile used for local development
.DEFAULT_GOAL := help
CWD:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
MOVE_TO_ROOT = cd "$(CWD)/.."

include .env
export

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Pass arguments to the test command
ifeq (test,$(firstword $(MAKECMDGOALS)))
  TEST_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(TEST_ARGS):;@:)
endif

test: # Test all django apps OR pass testing target like "photo" or "photo.tests.test_mutations"
	$(MOVE_TO_ROOT) && poetry run python manage.py test --no-input $(TEST_ARGS)

coverage: # Get test coverage
	$(MOVE_TO_ROOT) && coverage erase && coverage run manage.py test && coverage html --skip-empty --skip-covered
	open htmlcov/index.html

populate: # Generate dummy data
	$(MOVE_TO_ROOT) && poetry run python launch.py

pre: # Run pre-commit
	$(MOVE_TO_ROOT) && pre-commit run --all-files
