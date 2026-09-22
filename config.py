import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "gaokao-essay-grader-dev-key")

    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5000))

    ESSAY_MIN_LENGTH = 200
    ESSAY_MAX_LENGTH = 2000
    ESSAY_EXPECTED_LENGTH = 800

    TOTAL_SCORE = 60
    CONTENT_MAX_SCORE = 20
    EXPRESSION_MAX_SCORE = 20
    DEVELOPMENT_MAX_SCORE = 20
