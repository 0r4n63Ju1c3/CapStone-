import socket
import sys
import ascon

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server
# given by the caller
server_address = ('127.0.0.1' acdsa, 1000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

    message = b'hello world'
    
    variant = 'Ascon-128'
    
    key   = bytes(bytearray([i % 256 for i in range(16)]))
    nonce = bytes(bytearray([i % 256 for i in range(16)]))
    ad    = bytes(bytearray([i % 256 for i in range(32)]))
    
    ct = ascon.ascon_encrypt(key, nonce, ad[:32], message, variant)

    
    print(ct)
    sock.sendall(ct)

    amount_received = 0
    amount_expected = len(ct)
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print('received {!r}'.format(data))

finally:
    sock.close()
    

    
    


