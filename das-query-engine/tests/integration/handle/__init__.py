import os
from dotenv import load_dotenv

env_path = ".env.testing"
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
