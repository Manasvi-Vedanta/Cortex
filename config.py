# GenMentor Configuration
# Reads from environment variables with fallback defaults

import os
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

# Google Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDRf_5b1YQxEyr80pnq9pI8NmT_ZWuNKjs")

# Google Search API Configuration (optional)
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY", "")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "genmentor.db")
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))

# AI Model Configuration
SENTENCE_TRANSFORMER_MODEL = os.getenv("SENTENCE_TRANSFORMER_MODEL", "all-mpnet-base-v2")
EMBEDDINGS_CACHE_PATH = "occupation_embeddings.pkl"

# Resource Search Configuration
RESOURCE_CACHE_TTL = int(os.getenv("RESOURCE_CACHE_TTL", "24"))  # hours

# Performance Configuration
USE_GPU = os.getenv("USE_GPU", "false").lower() == "true"
USE_FAISS = os.getenv("USE_FAISS", "true").lower() == "true"

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "5000"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DEBUG_MODE = True

# Performance Settings
MAX_SKILLS_IN_PATH = 20  # Limit skills analyzed for performance
DEFAULT_SEARCH_LIMIT = 10
MAX_SEARCH_LIMIT = 50