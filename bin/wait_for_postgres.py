import socket
import time
import sys

print(sys.argv)
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((sys.argv[1], port))
        s.close()
        break
    except socket.error as ex:
        time.sleep(0.1)