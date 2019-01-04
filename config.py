import os
class Config():
    '''
    parent class config

    '''
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://pheobe:pheobe@localhost/flask'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    #  email configurations
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SECRET_KEY=os.environ.get('SECRET_KEY')
    # simple mde  configurations
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True

    @staticmethod
    def init_app(app):
        pass

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    pass

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://pheobe:pheobe@localhost/blog'
    DEBUG = True


class TestConfig(Config):
    pass

config_options = {
    'production':ProdConfig,
    'development':DevConfig,
    'test':TestConfig
}
