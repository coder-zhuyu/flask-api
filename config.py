# -*- coding: utf-8 -*-
import os
import datetime
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '71ccb40a5a1f4266a6765fbc9cb33aeb')
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=3600)

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')

    @classmethod
    def init_app(cls, app):
        file_handler = RotatingFileHandler('./logs/demo.log',
                                           mode='w', maxBytes=1024 * 1024 * 100,
                                           backupCount=20,
                                           encoding='utf-8')

        if os.getenv('ENV') != 'production':
            logging.getLogger().setLevel(logging.DEBUG)
            # logging.basicConfig(level=logging.DEBUG)
        else:
            logging.getLogger().setLevel(logging.INFO)
            # logging.basicConfig(level=logging.INFO)

        app.logger.addHandler(file_handler)

        file_handler.setFormatter(Formatter(
            '%(asctime)s [in %(pathname)s:%(lineno)d] %(levelname)s: %(message)s '
        ))


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = "mysql://root:111111@10.0.32.34:3306/api"


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
