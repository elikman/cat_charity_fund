import secrets

# Генерация случайного секретного ключа
secret_key = secrets.token_hex(32)

# Данные для .env
env_content = f"""
APP_TITLE=QRKot
APP_DESCRIPTION=A charity project for helping animals
APP_VERSION=1.0.0
DATABASE_URL=sqlite+aiosqlite:///./cat_fund.db
SECRET={secret_key}
FIRST_SUPERUSER_EMAIL=admin@example.com
FIRST_SUPERUSER_PASSWORD=superpassword
AUTH_BACKEND_NAME=basic_auth
"""

# Запись в файл .env
with open('.env', 'w') as f:
    f.write(env_content)

print("Файл .env был успешно создан с секретным ключом.")