import os

# prevent cross-site request forgery
CSRF_ENABLED = True
# create cryptographic token for form validation
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com'}
]

basedir = os.path.abspath(os.path.dirname(__file__))
# path of the database file
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# folder to store the SQLAlchemy-migrate data files
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


# mail server settings
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'xxxxxxxxxx'
MAIL_PASSWORD = 'xxxxxxxxxx'

# administrator list
ADMINS = ['xxxxxxxxxx@gmail.com']

# pagination
POSTS_PER_PAGE = 2

# full text search database
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 30
