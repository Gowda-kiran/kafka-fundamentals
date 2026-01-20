from requests import get
from json import loads

def fetch_users():
    response = get("https://api.escuelajs.co/api/v1/users")
    return loads(response.text)