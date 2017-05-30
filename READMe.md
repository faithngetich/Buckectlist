# Buckectlist
API for an online Bucket List (a list of things that one has not done before but wants to do before dying.)service using Flask.



| Url EndPoint                               | HTTP Methods     | Functionality                                    | Requires Token |
|--------------------------------------------|------------------|--------------------------------------------------|----------------|
| `/auth/login`                              | POST             | Logs a user in                                   | No             |
| `api/v1/auth/register`                     | POST             | Register a user                                  | No             |
| `/api/v1/bucketlists`                      | POST, GET        | Create a retrieve all bucket lists               | Yes            |
| `/api/v1/bucketlists/<id>`                 | GET, PUT, DELETE | Retrieve, update and delete a single bucket list | Yes            |
| `/api/v1/bucketlists/<id>/items`           | POST             | Create a new item in bucket list                 | Yes            |
| `/api/v1/bucketlists/<id>/items/<item_id>` | PUT, DELETE      | Delete an item in a bucket list                  | Yes            |



setting up

Prepare your virtual env

To install virtualenvwrapper, we will first install virtualenv

  $ pip install virtualenv
  $ pip install virtualenvwrapper


  To create a virtual environment

  $ mkvirtualenv --python=python3_path <environment_name>


  To activate a virtual environment

  $ workon <environment_name>

  To deactivate it, just type:

  $ deactivate

  cloning the repo
  $ git clone
  
  Create the .env file in the root folder

  $ touch .env

  Add the following to the file

  export SECRET_KEY="Your secret key"

  Export the settings

  $ source .env

  To run the application

Create the db

  $ python manage.py db init
  $ python manage.py db migrate
  $ python manage.py db upgrade

  Create an Admin user

  $ python manage.py createuser

  Install postman, a Google Chrome extension:


  $ python manage.py runserver

  Then run this command on  postman:

  $ python manage.py runserver

Change into the app directory by running `cd BucketList`.

After successfully doing this, call `git checkout develop` .

Install the requirements using `pip install -r requirements.txt`.


Deploying to Heroku

Create a Heroku account online

Install the Heroku CLI. If using Mac OS X, run

  $ brew install heroku
Log in using the email address and password you used when creating your Heroku account

  $ heroku login
Create an app on Heroku, which prepares Heroku to receive your source code

  $ heroku apps:create <app_name>
Create a Procfile in the root folder

  $ touch Procfile

Add the following to the procfile
  $ web: gunicorn manage:app

Create a runtime.txt file

  $ touch runtime.txt

Add the following to the runtime.txt
  python-3.6.0
