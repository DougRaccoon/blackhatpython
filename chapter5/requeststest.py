import requests

url = 'https://google.com'
response = requests.get(url)

data = {'user': 'raccoon','passwd': 'trash'}
response = requests.post(url, data=data)
print(response.text)
