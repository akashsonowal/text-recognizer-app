# Arcane Incantation to print all the other targets
help:
      @$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null/ | awk -v RS= -F: '/^# File/ , /^# Finished Make data base/' {if ($$1 !~ "^[#.]") {print $$1}} | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

# Install exact Python and CUDA versions
conda-update:
      conda env update --prune -f environment.yml
      echo "!!!RUN THE conda activate COMMAND ABOVE RIGHT NOW!!!"

# Compile and install exact pip packages
pip-tools:
      pip install pip-tools==6.5.1 setuptools==59.5.0
      pip-compile requirements/prod.in && pip-compile requirements/dev.in
      pip-sync requirements/prod.txt requirements/dev.txt
      
# Compile and install the requirements for local linting (optional)
pip-tools-lint:
      pip install pip-tools==6.5.1 setuptools==59.5.0

# Bump versions of transitive dependencies
pip-tools-upgrade:
      pip install pip-tools==6.5.1 setuptools==59.5.0

# Example training command
train-mnist-cnn-ddp:

# Lint
lint:

# Test notebooks in source repo
test-notebooks:



      
