from re import M
import socket
import random
import string
import ascon
import time
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

BLOCK_SIZE = 32 # Bytes

none_t = 0
ascon_t = 0
aes_t = 0

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def with_none(client_socket, message):

    client_socket.send(b'None')
    client_socket.recv(1024)

    t = time.process_time()

    client_socket.send(message)  # send message

    data = client_socket.recv(1024)  # receive response

    elapsed_time = (time.process_time()  - t)
    global none_t
    none_t = none_t + elapsed_time

def with_ascon(client_socket, message):

    client_socket.send(b"Ascon")
    recv = client_socket.recv(1024)

    variant = 'Ascon-128'
    key   = bytes(bytearray([i % 256 for i in range(16)]))
    nonce = bytes(bytearray([i % 256 for i in range(16)]))
    ad    = bytes(bytearray([i % 256 for i in range(32)]))

    t = time.process_time()

    message = ascon.ascon_encrypt(key, nonce, ad[:32], message, variant)

    client_socket.send(message)  # send message

    data = client_socket.recv(1024)  # receive response

    message = ascon.ascon_decrypt(key, nonce, ad[:32], data, variant) # decrypt received

    elapsed_time = (time.process_time()  - t)

    global ascon_t
    ascon_t = ascon_t + elapsed_time

def with_aes(client_socket, message):

    client_socket.send(b"AES")
    recv = client_socket.recv(1024).decode()

    key   = bytes(bytearray([i % 256 for i in range(16)]))
    cipher = AES.new(key, AES.MODE_ECB)
    decipher = AES.new(key, AES.MODE_ECB)

    t = time.process_time()

    message = cipher.encrypt(pad(message, BLOCK_SIZE))

    client_socket.send(message)

    data = client_socket.recv(1024)  # receive response

    data_dec = decipher.decrypt(data)

    elapsed_time = (time.process_time()  - t)

    global aes_t
    aes_t = aes_t + elapsed_time

def client_program():

    trials = 20

    #host = socket.gethostname()  # as both code is running on same pc
    host = '10.1.100.218'
    port = 5000 # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    global none_t
    global ascon_t
    global aes_t

    print("Trials: ", trials)

    for i in range(trials): 
        message = bytes(randomword(10), 'utf-8')

        with_none(client_socket, message)
        with_ascon(client_socket, message)
        with_aes(client_socket, message)

    print("None Time (10):", (none_t/2)/trials)
    print("Ascon Time (10):", (ascon_t/2)/trials)
    print("AES Time (10):", (aes_t/2)/trials)


    none_t = 0
    ascon_t = 0
    aes_t = 0
    for i in range(trials): 
        message = bytes(randomword(100), 'utf-8')

        with_none(client_socket, message)
        with_ascon(client_socket, message)
        with_aes(client_socket, message)

    print("None Time (100):", (none_t/2)/trials)
    print("Ascon Time (100):", (ascon_t/2)/trials)
    print("AES Time (100):", (aes_t/2)/trials)

    none_t = 0
    ascon_t = 0
    aes_t = 0
    for i in range(trials): 
        message = bytes(randomword(500), 'utf-8')

        with_none(client_socket, message)
        with_ascon(client_socket, message)
        with_aes(client_socket, message)

    print("None Time (500):", (none_t/2)/trials)
    print("Ascon Time (500):", (ascon_t/2)/trials)
    print("AES Time (500):", (aes_t/2)/trials)

    client_socket.send(b'disconnected') # tell the server to disconect
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
