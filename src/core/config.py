import os

from dotenv import load_dotenv
from pydantic import BaseSettings, PostgresDsn

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET = os.getenv('SECRET')


class AppSettings(BaseSettings):
    app_title: str = "Cocloud"
    database_dsn: PostgresDsn

    class Config:
        env_file = '.env'


app_settings = AppSettings()
