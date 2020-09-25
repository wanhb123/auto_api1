class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:ast123@47.116.137.59:3306/auto_site'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    JSON_AS_ASCII = False


class Development(Config):
    ENV = 'development'


class Production(Config):
    ENV = 'production',
    DEBUG = False
    SQLALCHEMY_ECHO = False
