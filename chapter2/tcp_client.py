import socket

target_host = "127.0.0.1"
target_port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host,target_port))

payload = "random text"
payload = bytes(payload,'utf-8')

client.send(payload)

response = client.recv(4096)

print(response)



