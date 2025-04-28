import logging
from django.conf import settings
import os

# Configure logger
logger = logging.getLogger('cases')
logger.setLevel(logging.INFO)

# Create handlers
log_file = os.path.join(settings.BASE_DIR, 'logs', 'cases.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

# Create formatters
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)