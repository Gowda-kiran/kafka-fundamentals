from requests import get
from json import loads

def fetch_products():
    response = get("https://api.escuelajs.co/api/v1/products")
    return loads(response.text)