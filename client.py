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
ascon_hash_only_t = 0
ascon_hash_encrypt_t = 0

system_check = 1

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def with_none(client_socket, message):

    client_socket.send(b'None')
    client_socket.recv(1024)

    t = time.process_time()

    #print("None Message Sent:", message)

    client_socket.send(message)  # send message

    message = client_socket.recv(1024)  # receive response

    #print("None message recv:", data)
    
    if not system_check:
        elapsed_time = (time.process_time()  - t)
        global none_t
        none_t = none_t + elapsed_time

def with_ascon(client_socket, message, key, nonce, ad, variant):

    client_socket.send(b"Ascon")
    recv = client_socket.recv(1024)

    t = time.process_time()

    #print("Ascon Message sent:", message)

    message = ascon.ascon_encrypt(key, nonce, ad[:32], message, variant)

    client_socket.send(message)  # send message

    message = client_socket.recv(1024)  # receive response

    message = ascon.ascon_decrypt(key, nonce, ad[:32], message, variant) # decrypt received

    #print("Ascon message recv:", message)
    
    if not system_check:
        elapsed_time = (time.process_time()  - t)

        global ascon_t
        ascon_t = ascon_t + elapsed_time
    
def with_ascon_hash_only(client_socket, message, key, nonce, ad, variant):
    
    client_socket.send(b"Ascon-Hash-Only")
    recv = client_socket.recv(1024)

    t = time.process_time()

    #print("Ascon Message sent:", message)
    hash_message = ascon.ascon_hash(message, variant="Ascon-Hash", hashlength=32)

    client_socket.send(hash_message)  # send message

    conf_message = client_socket.recv(1024)
    
    client_socket.send(message)

    #print("Ascon message recv:", message)
    if not system_check:
        elapsed_time = (time.process_time()  - t)

        global ascon_hash_only_t
        ascon_hash_only_t = ascon_hash_only_t + elapsed_time
    
def with_ascon_hash_encrypt(client_socket, message, key, nonce, ad, variant):
    
    client_socket.send(b"Ascon-Hash-Encryption")
    recv = client_socket.recv(1024)

    t = time.process_time()

    #print("Ascon Message sent:", message)

    message = ascon.ascon_encrypt(key, nonce, ad[:32], message, variant)
    hash_message = ascon.ascon_hash(message, variant="Ascon-Hash", hashlength=32)
    
    client_socket.send(message)  # send message

    message = client_socket.recv(1024)  # receive response
    
    client_socket.send(hash_message)
    
    message = ascon.ascon_decrypt(key, nonce, ad[:32], message, variant) # decrypt received

    #print("Ascon message recv:", message)
    if not system_check:
        elapsed_time = (time.process_time()  - t)

        global ascon_hash_encrypt_t
        ascon_hash_encrypt_t = ascon_hash_encrypt_t + elapsed_time

def with_aes(client_socket, message, cipher, decipher):

    client_socket.send(b"AES")
    recv = client_socket.recv(1024).decode()

    t = time.process_time()

    #print("AES message sent:", message)

    message = cipher.encrypt(pad(message, BLOCK_SIZE))

    client_socket.send(message)

    message = client_socket.recv(1024)  # receive response

    message = decipher.decrypt(message)

    #print("AES Message recv:", message)
    if not system_check:
        elapsed_time = (time.process_time()  - t)

        global aes_t
        aes_t = aes_t + elapsed_time

def trial(message_len, trials, client_socket, key, nonce, ad, variant, cipher, decipher):

    global none_t
    global ascon_t
    global aes_t
    global ascon_hash_t
    global ascon_hash_encrypt_t
    none_t = 0
    ascon_t = 0
    aes_t = 0
    ascon_hash_t = 0
    ascon_hash_encrypt_t = 0

    print("Message Length:", message_len)

    for i in range(trials): 
        message = bytes(randomword(message_len), 'utf-8')

        #with_none(client_socket, message)
        #with_ascon(client_socket, message, key, nonce, ad, variant)
        #with_aes(client_socket, message, cipher, decipher)
        #with_ascon_hash_only(client_socket, message, key, nonce, ad, variant)
        with_ascon_hash_encrypt(client_socket, message, key, nonce, ad, variant)
        
    if not system_check:
        print("None:", (none_t/2)/trials)
        print("Ascon:", (ascon_t/2)/trials)
        print("Ascon-Hash-Only:", (ascon_hash_only_t/2)/trials)
        print("Ascon-Hash-Encrypt:", (ascon_hash_encrypt_t/2)/trials)
        print("AES:", (aes_t/2)/trials, "\n")

    return 0

def client_program():

    trials = 20
    message_len = 10

    host = socket.gethostname()  # as both code is running on same pc
    #host = '10.1.100.218'
    port = 5000 # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    variant = 'Ascon-128'

    key   = bytes(bytearray([i % 256 for i in range(16)]))
    nonce = bytes(bytearray([i % 256 for i in range(16)]))
    ad    = bytes(bytearray([i % 256 for i in range(32)]))

    cipher = AES.new(key, AES.MODE_ECB)
    decipher = AES.new(key, AES.MODE_ECB)

    global none_t
    global ascon_t
    global aes_t
    global ascon_hash_only_t
    global ascon_hash_encrypt_t

    print("Trials: ", trials)

    trial(message_len, trials, client_socket, key, nonce, ad, variant, cipher, decipher)
    message_len = 100
    trial(message_len, trials, client_socket, key, nonce, ad, variant, cipher, decipher)
    message_len = 500
    trial(message_len, trials, client_socket, key, nonce, ad, variant, cipher, decipher)

    client_socket.send(b'disconnected') # tell the server to disconect
    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
