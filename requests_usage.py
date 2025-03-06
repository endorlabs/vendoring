from requests import get

response = get("https://endorlabs.com")
print(response.content)