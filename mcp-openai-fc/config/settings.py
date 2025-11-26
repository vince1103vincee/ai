"""Configuration settings for OpenAI API"""
from pathlib import Path
import configparser

# Initialize paths
PROJECT_ROOT = Path(__file__).parent.parent
SECRET_DIR = PROJECT_ROOT / ".secret"
KEY_FILE = SECRET_DIR / "openai.key"
CONFIG_FILE = PROJECT_ROOT / "local.config"

# Load configuration from local.config
if not CONFIG_FILE.exists():
    raise FileNotFoundError(
        f"Configuration file not found at {CONFIG_FILE}\n"
        f"Please create local.config with required settings"
    )

config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# Read OpenAI configuration
OPENAI_MODEL = config.get('OpenAI Settings', 'OPENAI_MODEL', fallback='gpt-3.5-turbo')
OPENAI_TEMPERATURE = config.getfloat('OpenAI Settings', 'OPENAI_TEMPERATURE', fallback=0.7)

# Read API Server configuration
API_SERVER_URL = config.get('API Server Settings', 'API_SERVER_URL', fallback='http://localhost:8000')
API_SERVER_TIMEOUT = config.getint('API Server Settings', 'API_SERVER_TIMEOUT', fallback=10)

# Read OpenAI API Key from .secret/openai.key
if not KEY_FILE.exists():
    raise FileNotFoundError(
        f"API Key file not found at {KEY_FILE}\n"
        f"Please create .secret/openai.key with your OpenAI API Key"
    )

with open(KEY_FILE, 'r') as f:
    OPENAI_API_KEY = f.read().strip()

if not OPENAI_API_KEY:
    raise ValueError("openai.key file is empty. Please add your OpenAI API Key.")
