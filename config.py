# Loads environment variables and defines application settings.

import os
from dotenv import load_dotenv

# Load variables from a .env file (if one exists) into the environment
load_dotenv()


class Config:
    # Turns on detailed error pages and auto-reload during development.
    # Set FLASK_DEBUG=0 in production (e.g. on Render).
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"

    # Where the SQLite database file lives.
    # On Render this can be overridden with an environment variable
    # pointing to a persistent disk path.
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "leads.db")
    )

    # Groq API key for the chatbot (Maviron Asistan). Set this on Render as
    # an environment variable; never commit the real key to the repo.
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

    # Groq model used for chat responses. llama-3.3-70b-versatile is a good
    # free-tier default: fast and capable. Can be overridden via env var.
    GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
