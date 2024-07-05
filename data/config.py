from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS", subcast=int)  # Assuming ADMINS should be a list of integers
WEBHOOK_HOST = env.str("WEBHOOK_HOST")
WEBHOOK_PATH_NAME = env.str("WEBHOOK_PATH_NAME")  # Ensure the key matches the .env file
WEBAPP_HOST = env.str("WEBAPP_HOST")
WEBAPP_PORT = env.int("WEBAPP_PORT")
IP = env.str("ip")
DATABASE_PATH = env.str("DATABASE_PATH")

WEBHOOK_PATH = f"/{WEBHOOK_PATH_NAME}/{BOT_TOKEN}/"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
