import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    CSRF_SESSION_KEY = "scorpionkingblues"
    SECRET_KEY = 'mimblybimblypimblypoo'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    BASE_DIR = basedir
    UPLOAD_FOLDER = basedir + '/static/uploads/'

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
