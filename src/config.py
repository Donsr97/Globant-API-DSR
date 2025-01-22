""" loads all configurations"""

import os
from dotenv import load_dotenv

load_dotenv()
### This is normally the file I would use to load al env variables and be able to make use of them anywhere, wherever i load them from .env or from the container.