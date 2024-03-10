import os
from dotenv import dotenv_values

# Load variables from .env file
env_vars = dotenv_values()

# Retrieve KEY and IV from environment variables
KEY = env_vars.get("KEY")
IV = env_vars.get("IV")

# Remove escape sequences from KEY and IV
KEY_bytes = bytes(KEY.encode().decode('unicode-escape'), 'utf-8')
IV_bytes = bytes(IV.encode().decode('unicode-escape'), 'utf-8')

# Print the byte values
print("KEY_bytes:", KEY_bytes)
print("IV_bytes:", IV_bytes)
