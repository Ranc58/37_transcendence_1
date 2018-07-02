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
    - `DJANGO_CONFIGURATION` - set up your conf (by default used `Dev`).
    - `SECRET_KEY_DJANGO` - Put here your secret key for django project if you setup conf for `Prod`
    - `SENTRY_DSN` - If you don't have sentry DSN - Register in [Sentry](https://sentry.io/),
     and create new project, then put it here. Otherwise use your sentry DSN.
    - `DB_PASSWORD` - password for database
    - `ADMIN_PASS` - password for admin user(work only with fabric)
    - `SSH_HOST` - args for SSH connect to server(only for fabric). Must be like `user@ip`
4. Add new environment parameters to Your system: `source .env`
5. Run `python3 manage.py migrate`
6. Create new admin `python3 manage.py createsuperuser`

# How to use locally

1. Run `python3 manage.py runserver`
2. Go to `127.0.0.1:8000/admin/` and create new user.
3. Go to `127.0.0.1:8000/users/<USER_ID>` to see user info.

# Tests locally

Run `pytest`

# How to use with fabric:
Project will be by path `/var/www/sci_blog/` and starts by `systemd`. 
1. Run `fab bootstrap` for quick deploy and go to `<HOST>`.
2. Use command `fab create_superuser` for create user with nickname `admin` and password from `.env` file `ADMIN_PASS`.
3. Go to `host` in browser.
Another fabric commands:
 - `fab drop_db` - drop database 
 - `fab status_service` - get service status.
 - `fab stop_service` - stop service.
 - `fab restart_service` - restart service.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
