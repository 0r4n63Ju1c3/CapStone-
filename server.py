import socket
import ascon
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

BLOCK_SIZE = 32 # Bytes

def server_none(conn):
    message = conn.recv(1024)
    conn.send(message)  # send data to the client

def server_ascon(conn, key, nonce, ad, variant):
    
    message = conn.recv(1024)
    #print("from connected user: " + str(data))

    message = ascon.ascon_decrypt(key, nonce, ad[:32], message, variant)
    #print("Message decoded: ", ct.decode())

    message = ascon.ascon_encrypt(key, nonce, ad[:32], message, variant)
    #print("Message enrypted: ", ct)

    #server_socket.send(ct)  # send message
    
    conn.send(message)  # send data to the client

def server_aes(conn, cipher, decipher):
    
    message = conn.recv(1024)
    #print("from connected user: " + str(data))

    message = decipher.decrypt(message)
    #print(unpad(data_dec, BLOCK_SIZE).decode())
    
    #print("Message decoded: ", ct.decode())

    message = cipher.encrypt(pad(message, BLOCK_SIZE))
    conn.send(message)
    #print(unpad(data_dec, BLOCK_SIZE).decode())
    
    #print("Message enrypted: ", ct)

    #server_socket.send(ct)  # send message
    
def server_ascon_hash_only(conn, key, nonce, ad, variant):
    
    client_hash = conn.recv(1024)
    #print("from connected user: " + str(data))
    
    # confimred received hash
    conn.send(b"received hash")
    
    message = conn.recv(1024)
    #print("Message decoded: ", ct.decode())
    
    server_hash = ascon.ascon_hash(message, variant="Ascon-Hash", hashlength=32)
    #print("Message enrypted: ", ct)
    
    if client_hash != server_hash:
        print("invalid message")
    else:
        print("valid message")
    #server_socket.send(ct)  # send message
      # send data to the client          

def server_ascon_hash_encrypt(conn, key, nonce, ad, variant):
    encrypted_message = conn.recv(1024)
    #print("from connected user: " + str(data))

    decrypted_message = ascon.ascon_decrypt(key, nonce, ad[:32], encrypted_message, variant)
    #print("Message decoded: ", ct.decode())

    reencrypt_message = ascon.ascon_encrypt(key, nonce, ad[:32], decrypted_message, variant)
    #print("Message enrypted: ", ct)
    conn.send(reencrypt_message)
    
    client_hash = conn.recv(1024)
    
    server_hash = ascon.ascon_hash(decrypted_message, variant="Ascon-Hash", hashlength=32)
    
    if client_hash != server_hash:
        print("invalid message")
    else:
        print("valid message")
    #server_socket.send(ct)  # send message

def server_program():

    variant = 'Ascon-128'

    key   = bytes(bytearray([i % 256 for i in range(16)]))
    nonce = bytes(bytearray([i % 256 for i in range(16)]))
    ad    = bytes(bytearray([i % 256 for i in range(32)]))

    cipher = AES.new(key, AES.MODE_ECB)
    decipher = AES.new(key, AES.MODE_ECB)

    # get the hostname
    host = socket.gethostname()
    #host = '10.1.100.218'
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

    while True:
        msg = conn.recv(1024).decode()
        if msg == 'disconnected':
            conn.close()
            break
        print(msg)
        conn.send(b'connected')

        if msg == 'None':
            server_none(conn)

        if msg == 'Ascon':
            server_ascon(conn, key, nonce, ad, variant)

        if msg == 'AES':
            server_aes(conn, cipher, decipher)
            
        if msg == 'Ascon-Hash-Only':
            server_ascon_hash_only(conn, key, nonce, ad, variant)
        
        if msg == 'Ascon-Hash-Encryption':
            server_ascon_hash_encrypt(conn, key, nonce, ad, variant)


if __name__ == '__main__':
    server_program()
