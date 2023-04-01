# Arcane Incantation to print all the other targets
help:
      @$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null/ | awk -v RS= -F: '/^# File/ , /^# Finished Make data base/' {if ($$1 !~ "^[#.]") {print $$1}} | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

# Install exact Python and CUDA versions
conda-update:

# Compile and install exact pip packages
pip-tools:


# Compile and install the requirements for local linting (optional)
pip-tools-lint:

# Bump versions of transitive dependencies
pip-tools-upgrade:

# Example training command
train-mnist-cnn-ddp:

# Lint
lint:

# Test notebooks in source repo
test-notebooks:



      
