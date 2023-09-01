from celery import Celery
from config import Config

config = Config()

celery_app = Celery(__name__, broker=f'{config.REDIS_BROKER_BASE_URL}/0')

@celery_app.task(name='log_register')
def log_register(username, date):
     with open('logs/log_signin.txt', 'a+') as file:
         file.write('{} - Session initializated: {}\n'.format(username, date))