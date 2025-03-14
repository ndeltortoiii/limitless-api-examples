import os
from dotenv import load_dotenv


def load_env(root_dir):
  # Try loading .env.local first, then fall back to .env if needed
  env_local_path = os.path.join(root_dir, '.env.local')
  env_path = os.path.join(root_dir, '.env')

  # load_dotenv returns True if it found and loaded the file
  if not load_dotenv(env_local_path):
        load_dotenv(env_path)
