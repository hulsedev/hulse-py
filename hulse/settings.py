import os
import json
import copy
from pathlib import Path
import requests

from appdirs import user_config_dir
from dotenv import load_dotenv

CONFIG_PATH = Path(user_config_dir(appname="hulse", appauthor="hulse"))
if not CONFIG_PATH.is_dir():
    CONFIG_PATH.mkdir(parents=True)

load_dotenv()

# base server url
HULSE_API_URL = os.getenv("HULSE_API_URL", "https://hulse-api.herokuapp.com/")
HULSE_STREAM_URL = os.getenv("HULSE_STREAM_URL", "https://hulse-stream.herokuapp.com/")
HULSE_LOGIN_URL = os.getenv(
    "HULSE_LOGIN_URL", "https://hulse-api.herokuapp.com/login/?source=desktop"
)
CONFIG = {}

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


def load_config():
    """Load config from CONFIG user file."""
    global CONFIG

    filepath = CONFIG_PATH / ".config.json"
    if filepath.is_file():
        with open(filepath) as f:
            CONFIG.update(json.load(f))


def set_config(config: dict) -> bool:
    """Store config to CONFIG user file and set it in module.

    :param config: Candidate config to be set.
    :type config: dict
    :return: Whether the config is valid.
    :rtype: bool
    """
    global CONFIG

    # check whether the config is correct when setting it
    if not validate_config(config):
        return False

    CONFIG = copy.deepcopy(config)
    with open(CONFIG_PATH / ".config.json", "w") as f:
        json.dump(CONFIG, f)

    return True


def validate_config(config: dict) -> bool:
    """Make sure that the provided config is valid.

    :param config: Candidate config
    :type config: dict
    :return: Config validity result.
    :rtype: bool
    """
    print("checking config", config)
    if "api_key" not in config or "email" not in config:
        return False

    r = requests.get(
        HULSE_API_URL + "ping/", headers=get_auth_headers(config["api_key"])
    )
    print("status code", r.status_code, HULSE_API_URL + "ping/")
    return r.status_code == 200


def reset_config():
    """Reset config to default."""
    global CONFIG

    CONFIG = {}
    with open(CONFIG_PATH / ".config.json", "w") as f:
        json.dump(CONFIG, f)


load_config()
