import requests 
url = "https://oda.com/tienda-web-api/v1/search/mixed/"
params = {
    "q": "*",
    "type": "product",
    "page": 3 
}

r = requests.get(url, params=params)
r.raise_for_status()
response = r.json()
print(response)
