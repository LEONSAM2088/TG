from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()
ADMINS = env.list("ADMINS")
BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str

IP = env.str("ip")  # Тоже str, но для айпи адреса хоста
