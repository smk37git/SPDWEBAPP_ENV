# Sigma Phi Delta Mizzou New Website
## Setup Instructions
For security purposes, the website stores the database, secret key, development environment, and the path to the admin panel in a seperate file that is *two directories above the website files*, aka, *the same directory that the git repo is stored in*.

In that folder, you need two things:

1. The `db.sqlite3` file (which will be automatically generated unless you have a previous database you want to use)
2. A file called `secret_config.py`

Create the secret_config.py file to match this template
```python
SECRET_KEY = 'paste here'
ADMIN_URL = 'admin'
ENVIRONMENT = 'local'
```
Then paste the output of this command into the file
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
You may change the admin path to whatever you wish. The environment should be set to either 'local' or 'development'
