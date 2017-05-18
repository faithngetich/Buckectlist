import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    '''Parent configuration class general settings that we want all environments to have by default. '''
    DEBUG = False
    SECRET_KEY = "\xe6Ff\xbdNB\x0eW\xa8Dtl+l\xf1U\xf5\x15A\xa3\xe1<\x14\x8d"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
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
