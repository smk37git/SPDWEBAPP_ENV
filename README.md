# Sigma Phi Delta Mizzou New Website
## Setup Instructions
For security purposes, the website stores the database, secret key, and the path to the admin panel in a seperate file that is *two directories above the website files*, aka, *the same directory that the git repo is stored in*.

In that folder, you need two things:

1. The `db.sqlite3` file (which will be automatically generated unless you have a previous database you want to use)
2. A file called `secret_config.py`
    - This file can be setup with the following commands
        ```bash
        python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
        ```
        Copy the output of the command and put it into the file like so:
        ```python
        SECRET_KEY = 'paste here'
        ADMIN_URL = 'admin'
        ```
        You may change the admin path to whatever you wish.
