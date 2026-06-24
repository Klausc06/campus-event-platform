import os

IS_VERCEL = os.environ.get("VERCEL", "") == "1"
_db_path = "/tmp/app.db" if IS_VERCEL else os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.db")


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f'sqlite:///{_db_path}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = False
