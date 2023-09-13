from environs import Env

env = Env()
env.read_env()

URL = "https://znanium.com/catalog/books/theme?all=1"

HEADERS = {
    "Accept": "*/*",
    "User-Agent":  env.str("USER_AGENT")
}
