class Config(object):
    pass


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:qiong961129@127.0.0.1:3306/flp"
    SQLALCHEMY_echo = True

