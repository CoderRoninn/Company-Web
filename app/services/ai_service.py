# Sends user messages to the AI provider (Groq) and returns responses.

import requests
from config import Config

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"

# System prompt that tells the model who it is and how to behave as the
# "Maviron Asistan" chatbot on the Maviron website.
SYSTEM_PROMPT = (
    "You are 'Maviron Asistan', the chatbot on the Maviron software "
    "company website. Maviron builds SaaS products, web apps, mobile "
    "apps, custom software, cloud infrastructure and UI/UX design for "
    "businesses and startups. Answer visitor questions about services, "
    "process and general pricing in Turkish, in 2-4 short sentences, in "
    "a warm and professional tone. Never promise an exact price, "
    "deadline or contract term - say the team will follow up on those. "
    "If asked something unrelated to Maviron, politely steer back."
)


class AIServiceError(Exception):
    """Raised when the AI provider can't be reached or returns an error."""
    pass


def get_chat_response(message):
    """Send a user message to Groq and return the assistant's reply text."""
    if not Config.GROQ_API_KEY:
        raise AIServiceError("GROQ_API_KEY is not configured on the server")

    try:
        response = requests.post(
            GROQ_CHAT_URL,
            headers={
                "Authorization": f"Bearer {Config.GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": Config.GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
                "temperature": 0.6,
                "max_tokens": 400,
            },
            timeout=20,
        )
    except requests.RequestException as e:
        raise AIServiceError(f"Could not reach Groq: {e}")

    if response.status_code != 200:
        raise AIServiceError(
            f"Groq returned {response.status_code}: {response.text[:300]}"
        )

    data = response.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        raise AIServiceError("Unexpected response shape from Groq")
