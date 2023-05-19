# Musicians world

Little social network (like Twitter) for musicians. 

#### What's inside?
 - New musician registration;
 - Post albums;
 - Follow users.

### Technologies

- Flask
- MySQL
- Elasticsearch
- Python 3.9

#### Roadmap
- Add feed to see musicians updates;
- Add ability to add specific song.

## Installation

You need to create a virtual environment and after install necessary requirements.

Linux-based os example:

```
$ python3 vevn venv

$ source venv/bin/activate

$ pip install -r requirements.txt
```

## Flask Configuration

#### Example

```
app = Flask(__name__)
app.config['DEBUG'] = True
```
### Configuring From Files

#### Example Usage

```
app = Flask(__name__ )
app.config.from_pyfile('config.Development.cfg')
```

#### cfg example

```
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'example'

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')

    ALBUMS_PER_PAGE = 9

    CURRENT_YEAR = 2023

    LANGUAGES = ['en', 'ru']

    ELASTICSEARCH_URL = os.environ.get('ES_ENDPOINT')
```

### Configuration

All necessary configuration variables you need to set up as env variables before launch the application.

There is a list of all env variables:
- ADMINS (Pass here your email where you will get all system messages)
- ELASTICSEARCH_URL
- ES_ENDPOINT
- FLASK_APP (start point of you app. Pass here a file with 'app' variable)
- FLASK_DEBUG
- MAIL_PASSWORD
- MAIL_PORT
- MAIL_SERVER
- MAIL_USERNAME
- MAIL_USE_TLS
- SECRET_KEY
- SQLALCHEMY_DATABASE_URI
- SQLALCHEMY_TRACK_MODIFICATIONS (you can pass '0' here)

 
## Run Flask
```
$ flask run
```
In flask, Default port is `5000`

## Flask Application Structure 
```
.
├── app
│   ├── auth
│   │   ├── email.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── cli.py
│   ├── email.py
│   ├── errors
│   │   ├── handlers.py
│   │   ├── __init__.py
│   ├── __init__.py
│   ├── main
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models.py
│   ├── search.py
│   ├── templates
│   │   ├── add_album.html
│   │   ├── _album.html
│   │   ├── auth
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   ├── reset_password.html
│   │   │   └── reset_password_request.html
│   │   ├── base.html
│   │   ├── edit_album.html
│   │   ├── edit_profile.html
│   │   ├── email
│   │   │   ├── reset_password.html
│   │   │   └── reset_password.txt
│   │   ├── errors
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   ├── index.html
│   │   ├── search.html
│   │   ├── _song.html
│   │   └── user.html
│   └── translations
│       ├── es
│       │   └── LC_MESSAGES
│       │       ├── messages.mo
│       │       └── messages.po
│       └── ru
│           └── LC_MESSAGES
│               ├── messages.mo
│               └── messages.po
├── app.db
├── babel.cfg
├── config.py
├── logs
│   └── ...
├── main.py
├── messages.pot
├── microblog.py
├── migrations
│   └── ...
├── README.md
├── requirements.txt
├── sandbox.py
└── tests.py


```

## Reference

Official Website

- [Flask](http://flask.pocoo.org/)
- [Flask Extension](http://flask.pocoo.org/extensions/)
- [Flask-SQLalchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
- [elasticsearch-dsl](http://elasticsearch-dsl.readthedocs.io/en/latest/index.html)

Tutorial

- [Flask with Miguel Grinberg (article translation)](https://habr.com/ru/articles/346306/) 

## Changelog
- Version 1.0 : basic flask app (musicians registration, albums posting, following users).