import socket
import random
import string
import ascon
import time

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def with_none(trials, message_len, client_socket):

    total_t = time.process_time()
    client_socket.send(b'None')
    recv = client_socket.recv(1024).decode()
    if(recv == 'connected'):
        print("Connected to server")

    for i in range(trials): 
        message = bytes(randomword(message_len), 'utf-8')

        t = time.process_time()

        client_socket.send(message)  # send message

        data = client_socket.recv(1024)  # receive response

        elapsed_time = (time.process_time()  - t)

        total_t =+ elapsed_time

    print("Total Time (without Encryption) ", trials ," trials: ", total_t/trials, " in seconds")
    client_socket.send(b'disconnect')

def with_ascon(trials, message_len, client_socket):

    total_t = time.process_time()
    client_socket.send(b"Ascon")
    recv = client_socket.recv(1024).decode()
    if(recv == 'connected'):
        print("Connected to server")

    for i in range(trials): 
        message = bytes(randomword(message_len), 'utf-8')
        #print("Sent to server: ", message.decode())

        variant = 'Ascon-128'

        key   = bytes(bytearray([i % 256 for i in range(16)]))
        nonce = bytes(bytearray([i % 256 for i in range(16)]))
        ad    = bytes(bytearray([i % 256 for i in range(32)]))

        t = time.process_time()

        ct = ascon.ascon_encrypt(key, nonce, ad[:32], message, variant)

        message = ct

        client_socket.send(message)  # send message

        data = client_socket.recv(1024)  # receive response

        ct = ascon.ascon_decrypt(key, nonce, ad[:32], data, variant) # decrypt received

        elapsed_time = (time.process_time()  - t)

        total_t =+ elapsed_time

    print("Total Time (with Ascon) ", trials ," trials: ", total_t/trials, " in seconds")
    client_socket.send(b'disconnect')

def client_program():

    trials = 20
    message_len = 10

    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    with_none(trials, message_len, client_socket)
    client_socket.send(b'break')
    with_ascon(trials, message_len, client_socket)
    

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
