from requests import get
from json import loads

def fetch_categories():
    response = get("https://api.escuelajs.co/api/v1/categories")
    return loads(response.text)