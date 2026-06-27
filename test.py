import socket
s = socket.socket()
s.connect(('localhost', 7001))
s.send(b'print("hola desde vscode")\n')
s.close()