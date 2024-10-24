import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can access your environment variables
print(os.getenv("dsn_hostname"))
