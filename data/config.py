from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
DB_HOST=env.str("DB_HOST")
DB_PORT=env.str("DB_PORT")
DB_USER=env.str("DB_USER")
DB_PASS=env.str("DB_PASS")
DB_NAME=env.str("DB_NAME")
IP = env.str("ip")  # Xosting ip manzili
