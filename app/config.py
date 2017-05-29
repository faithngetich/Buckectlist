import os
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    '''Parent configuration class general settings that we want all environments to have by default. '''
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    print(SECRET_KEY)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_AUTH_URL_RULE = "/api/login"
    JWT_DEFAULT_REALM = 'Login Required'
    JWT_EXPIRATION_DELTA = timedelta(minutes=3600)
    
class DevelopmentConfig(Config):
    """Configurations for Development."""
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.db')
    DEBUG = True

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    DEBUG = True
    TESTING = True

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.db')


config_by_name = dict(
    dev = DevelopmentConfig,
    test = TestingConfig,
    prod = ProductionConfig
)

config = {
    'SECRET': os.getenv('SECRET') or "ManySecrets@#456%%to^&!@protect"
}
