import os
from typing import Union

from dotenv import load_dotenv

load_dotenv()

ZAIM_USER_ID: Union[str, None] = os.getenv("ZAIM_USER_ID")
ZAIM_PASSWORD: Union[str, None] = os.getenv("ZAIM_PASSWORD")
CHROME_DRIVER_PATH: Union[str, None] = os.getenv("CHROME_DRIVER_PATH")
DOCKER_SELENIUM_IPADDRESS: Union[str, None] = os.getenv("DOCKER_SELENIUM_IPADDRESS")
LINE_CHANNEL_ACCESS_TOKEN: Union[str, None] = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_MESSAGE_TO_ID: Union[str, None] = os.getenv("LINE_MESSAGE_TO_ID")

ZAIM_CONSUMER_ID: Union[str, None] = os.getenv("ZAIM_CONSUMER_ID")
ZAIM_CONSUMER_SECRET: Union[str, None] = os.getenv("ZAIM_CONSUMER_SECRET")
ZAIM_ACCESS_TOKEN: Union[str, None] = os.getenv("ZAIM_ACCESS_TOKEN")
ZAIM_ACCESS_TOKEN_SECRET: Union[str, None] = os.getenv("ZAIM_ACCESS_TOKEN_SECRET")
ZAIM_OAUTH_VERIFIER: Union[str, None] = os.getenv("ZAIM_OAUTH_VERIFIER")
