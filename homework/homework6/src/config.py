import os
from dotenv import load_dotenv


def load_env(env_path):
    load_dotenv(dotenv_path=env_path)

def get_key(key_name):
    value = os.getenv(key_name)
    if value is None:
        print(f"Not an env variable.")
    return value
