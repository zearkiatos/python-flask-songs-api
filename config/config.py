import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    REDIS_BROKER_BASE_URL = os.getenv('REDIS_BROKER_BASE_URL')