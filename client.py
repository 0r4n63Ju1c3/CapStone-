import socket
import random
import string
import ascon
import time

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    message = bytes(randomword(10), 'utf-8')
    print("Sent to server: ", message.decode())

    variant = 'Ascon-128'

    key   = bytes(bytearray([i % 256 for i in range(16)]))
    nonce = bytes(bytearray([i % 256 for i in range(16)]))
    ad    = bytes(bytearray([i % 256 for i in range(32)]))

    t = time.process_time()

    ct = ascon.ascon_encrypt(key, nonce, ad[:32], message, variant)

    message = ct

    client_socket.send(message)  # send message
    data = client_socket.recv(1024)  # receive response

    ct = ascon.ascon_decrypt(key, nonce, ad[:32], message, variant)

    elapsed_time = (time.process_time()  - t) * 1000000000

    print('Received from server: ', ct.decode())  # show in terminal
    print("Time: ", elapsed_time, " nano seconds")

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
