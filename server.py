import socket
import ascon
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

BLOCK_SIZE = 32 # Bytes

def server_none(conn):
    data = conn.recv(1024)
    conn.send(data)  # send data to the client

def server_ascon(conn, key, nonce, ad, variant):
    
    data = conn.recv(1024)
    #print("from connected user: " + str(data))

    ct = ascon.ascon_decrypt(key, nonce, ad[:32], data, variant)
    #print("Message decoded: ", ct.decode())

    ct = ascon.ascon_encrypt(key, nonce, ad[:32], ct, variant)
    #print("Message enrypted: ", ct)

    #server_socket.send(ct)  # send message
    
    conn.send(ct)  # send data to the client

def server_aes(conn, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decipher = AES.new(key, AES.MODE_ECB)
    
    data = conn.recv(1024)
    #print("from connected user: " + str(data))

    data_dec = decipher.decrypt(data)
    #print(unpad(data_dec, BLOCK_SIZE).decode())
    
    #print("Message decoded: ", ct.decode())

    message = cipher.encrypt(pad(data_dec, BLOCK_SIZE))
    conn.send(message)
    #print(unpad(data_dec, BLOCK_SIZE).decode())
    
    #print("Message enrypted: ", ct)

    #server_socket.send(ct)  # send message

def server_program():

    variant = 'Ascon-128'

    key   = bytes(bytearray([i % 256 for i in range(16)]))
    nonce = bytes(bytearray([i % 256 for i in range(16)]))
    ad    = bytes(bytearray([i % 256 for i in range(32)]))

    # get the hostname
    host = socket.gethostname()
    #host = '10.1.100.140'
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
            server_aes(conn, key)


if __name__ == '__main__':
    server_program()
