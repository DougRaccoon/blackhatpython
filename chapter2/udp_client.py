import socket

target_host = "127.0.0.1"
target_port = 9999

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

payload = "AAABBBCCC"
payload = bytes(payload, "utf-8")

client.sendto(payload,(target_host,target_port))

data, addr = client.recvfrom(4096)

print(data.decode())
client.close()
