from environs import Env

env = Env()
env.read_env()

BOT_TOKEN: str = env.str("BOT_TOKEN")
ADMINS: list = env.list("ADMINS", cast=int)

DB_USER: str = env.str("DB_USER")
DB_PASS: str = env.str("DB_PASS")
DB_NAME: str = env.str("DB_NAME")
DB_HOST: str = env.str("DB_HOST")
