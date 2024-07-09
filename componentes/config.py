class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
