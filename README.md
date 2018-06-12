# Transcendence project

Social network for scientists.

# How to install

1. Recomended use venv or virtualenv for better isolation.\
   Venv setup example: \
   `python3 -m venv myenv`\
   `source myenv/bin/activate`
2. Install requirements: \
   `pip3 install -r requirements.txt` (alternatively try add `sudo` before command).
3. Open `.env` and correct values: 
    - `DJANGO_CONFIGURATION` - set up your conf (by default used `Dev` with `DEGUG=TRUE`).
    - `SENTRY_DSN` - If you don't have sentry DSN - Register in [Sentry](https://sentry.io/),
     and create new project, then put it here. Otherwise use your sentry DSN.
4. Run `python3 manage.py migrate`
5. Create new admin `python3 manage.py createsuperuser`

# How to use

1. Run `python3 manage.py runserver`
2. Go to `127.0.0.1:8000/admin/` and create new user.
3. Go to `127.0.0.1:8000/users/<USER_ID>` to see user info.

# Tests

Run `pytest`

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
