.DEFAULT_GOAL := help
DIRS = docker

.PHONY: $(DIRS)

help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

# Recursive run sub makefiles
ifneq ($(filter $(firstword $(MAKECMDGOALS)),$(DIRS)),)
  ARGS := $(wordlist 1,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(ARGS):;@:)
endif

docker: # Run Makefile from docker directory
	$(MAKE) -C $(ARGS)
