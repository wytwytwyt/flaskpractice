class Config(object):
    SECRET_KEY = 'e3f40293dd2c06088dc7c27400573967'


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:qiong961129@127.0.0.1:3306/flp"
    SQLALCHEMY_echo = True

