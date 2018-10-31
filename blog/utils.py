import os
import secrets


def get_or_create_secret_key(base_dir):
    filepath = os.path.join(base_dir, 'secret_key.txt')
    try:
        with open(filepath) as f:
            secret_key = f.read().strip()
    except FileNotFoundError as e:
        secret_key = secrets.token_urlsafe(50)
        with open(filepath, 'w') as f:
            f.write(secret_key)
    return secret_key
