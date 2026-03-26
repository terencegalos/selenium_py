DBHOST = 'localhost'
DBUSER = 'wares'
DBPASS = 'w@r3s'
DBNAME = 'wares_db'

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# --- Dropbox & Data Paths ---
DROPBOX_BASE = os.getenv('DROPBOX_BASE', r'C:/Users/USER/Dropbox/Waresitat Files/2022 Upload')
WARESITAT_UPLOAD_PATH = os.path.join(DROPBOX_BASE, 'Waresitat Upload')
BHBT_UPLOAD_PATH = os.path.join(DROPBOX_BASE, 'BuyHereBuyThere')

# Image Directory
IMG_DIR = os.getenv('IMG_DIR', r'C:/Waresitat Images')

# --- Output Paths ---
# Default to local directory if not specified
OUTPUT_BASE = os.getenv('OUTPUT_BASE', os.path.dirname(os.path.dirname(__file__)))
XLS_OUTPUT_WARESITAT = os.path.join(OUTPUT_BASE, 'src_py3', 'xls', 'output', 'waresitat')
XLS_OUTPUT_BHBT = os.path.join(OUTPUT_BASE, 'src_py3', 'xls', 'output', 'bhbt')
CSV_OUTFILE_PATH = os.path.join(OUTPUT_BASE, 'src_py3', 'helper', 'csv', 'outfile')
