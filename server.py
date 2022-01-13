
import socket
import ascon
# take the server name and port name
host = '10.1.100.218'
port = 5000
  
# create a socket at server side
# using TCP / IP protocol
s = socket.socket(socket.AF_INET,
                  socket.SOCK_STREAM)
  
# bind the socket with server
# and port number
s.bind(('', port))
  
# allow maximum 1 connection to
# the socket
s.listen(1)
  
# wait till a client accept
# connection
c, addr = s.accept()
  
# display client address
print("CONNECTION FROM:", str(addr))
  
# send message to the client after
# encoding into binary string
message = b'trying new string'
    
variant = 'Ascon-128'

key   = bytes(bytearray([i % 256 for i in range(16)]))
nonce = bytes(bytearray([i % 256 for i in range(16)]))
ad    = bytes(bytearray([i % 256 for i in range(32)]))

print(key)

ct = ascon.ascon_encrypt(key, nonce, ad[:32], message, variant)

msg = ct
c.send(msg)
  
# disconnect the server
c.close()