# Environment variables and constants will live here.
import os
from dotenv import load_dotenv

load_dotenv(".env")

CAREER_ONE_STOP_OCCUPATION_LIST_ENDPOINT = "https://api.careeronestop.org/v1/occupation/{userId}/{keyword}/{dataLevel}/{start}/{limit}"
CAREER_ONE_STOP_WEB_API_USER_ID = os.getenv("CAREER_ONE_STOP_WEB_API_USER_ID")
CAREER_ONE_STOP_WEB_API_TOKEN_KEY = os.getenv("CAREER_ONE_STOP_WEB_API_TOKEN_KEY")

ONET_API_URL = "https://api-v2.onetcenter.org/online/search"
ONET_API_KEY = os.getenv("ONET_API_KEY")
