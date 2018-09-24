#!/var/www/venv/bin/python3.5

# import pip
from subprocess import call
from pip._internal.utils.misc import get_installed_distributions

call("pip install --upgrade pip", shell=True)
call("pip install --upgrade setuptools", shell=True)

for dist in get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)
