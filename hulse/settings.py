import os

from dotenv import load_dotenv

load_dotenv()

# base server url
HULSE_API_URL = os.getenv("HULSE_API_URL", "https://hulse-api.herokuapp.com/")
HULSE_STREAM_URL = os.getenv("HULSE_STREAM_URL", "https://hulse-stream.herokuapp.com/")
# current transformer task supported, refer to transformer docs
SUPPORTED_TASKS = [
    "summarization",
    "translation",
    "text-generation",
    "text-classification",
    "sentiment-analysis",
    "question-answering",
    "text2text-generation",
    "zero-shot-classification",
]


def get_auth_headers(api_key: str) -> dict:
    """Generate HTTP headers for authentication with bearer token.

    :param api_key: Hulse API key.
    :type api_key: str
    :return: Headers for authentication as a dict
    :rtype: dict
    """
    return {"Authorization": f"Token {api_key}"}
