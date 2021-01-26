import requests

url = 'http://localhost/test.html'
resp = requests.delete(url)
print(resp.text)