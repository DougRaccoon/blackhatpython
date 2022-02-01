import urllib.parse
import urllib.request

url = 'https://nostarch.com'

with urllib.request.urlopen(url) as response:
    content = response.read()
    
info = {'user': 'raccoon', 'passwd': 'trash'}
data = urllib.parse.urlencode(info).encode()

req = urllib.request.Request(url, data)
with urllib.request.urlopen(req) as response:
    content = response.read()
    
print(content)
