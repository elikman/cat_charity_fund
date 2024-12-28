# core/config.py
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    app_title: str = 'Qr_Kot'
    app_description: str = 'Tests'
    app_author: str = 'Вячеслав Любченко'
    database_url: str = 'sqlite+aiosqlite:///./cat_fund.db'
    path: str
    secret: str = 'secret'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
