import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = 'no key'
    SQLACHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    '''
        开发环境配置
    '''
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data/data-dev.sqlite')

class TestingConfig(Config):
    '''
        测试环境配置
    '''
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data/data-test.sqlite')

class ProductionConfig(Config):
    '''
        正式环境配置
    '''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data/data.sqlite')

config = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}
