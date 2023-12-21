#!/usr/bin/python
import os
import sys
import logging
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/opt/python/app/fuspay/")

from app import app as application
application.secret_key = os.getenv('SECRET_KEY')