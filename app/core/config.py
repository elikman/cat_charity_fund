from typing import Optional
from pydantic import EmailStr, BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Кошачий благотворительный фонд'
    app_description: str = 'Сервис для поддержки котиков!'
    app_version: str = '1.0.0'
    database_url: str = 'sqlite+aiosqlite:///./qr_kot.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    auth_backend_name: Optional[str] = 'basic_auth'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = ''
        case_sensitive = False


settings = Settings()
