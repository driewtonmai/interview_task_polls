# MPV Polls

Task for the interview (Fabrique)

## Prerequisites

* Clone the project
`git clone git@github.com:driewtonmai/interview_task_polls.git`
* Create and start a a virtual environment
`virtualenv env --no-site-packages
source env/bin/activate`
* Install the project dependencies:
`pip install -r requirements.txt`
* Create a file named ".env"
`touch .env`
* Obtain a secret from MiniWebTool key and add to .env (you must use env_template template)
* Add .env to .gitignore file
* Then run
`python manage.py makemigrations`
`python manage.py migrate`
* Create admin account
`python manage.py createsuperuser`
* Start the development server
`python manage.py runserver`

## Documentation

https://documenter.getpostman.com/view/9317614/UVC8E6oz

## Built With

Django, django rest framework

### Authors

Omurzakov Tologon
