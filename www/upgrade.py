#!/var/www/venv/bin/python3.5

import pip
from subprocess import call

call("pip install --upgrade pip", shell=True)
call("pip install --upgrade setuptools", shell=True)

for dist in pip.get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)
