import socket
import ascon
  
# take the server name and port name
  
host = 'local host'
port = 5000
  
# create a socket at client side
# using TCP / IP protocol
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)
  
# connect it to server and port
# number on local computer.
s.connect(('127.0.0.1', port))
  
# receive message string from
# server, at a time 1024 B
msg = s.recv(1024)
  
# repeat as long as message
# string are not empty

variant = 'Ascon-128'
key   = bytes(bytearray([i % 256 for i in range(16)]))
nonce = bytes(bytearray([i % 256 for i in range(16)]))
ad    = bytes(bytearray([i % 256 for i in range(32)]))

ct = ascon.ascon_decrypt(key, nonce, ad[:32], msg, variant)

print("decoded message:" + ct.decode())

# add aes
# disconnect the client
s.close()
