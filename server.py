import socket
import ascon

def server_none(conn):
    while True:
        data = conn.recv(1024)
        if not data or data == b'break':
            # if data is not received break
            break
        
        conn.send(data)  # send data to the client

def server_ascon(conn, key, nonce, ad, variant):
    while True:
        data = conn.recv(1024)
        if not data or data == b'break':
            # if data is not received break
            break
        #print("from connected user: " + str(data))

        ct = ascon.ascon_decrypt(key, nonce, ad[:32], data, variant)
        #print("Message decoded: ", ct.decode())

        ct = ascon.ascon_encrypt(key, nonce, ad[:32], ct, variant)
        #print("Message enrypted: ", ct)

        #server_socket.send(ct)  # send message
        
        conn.send(ct)  # send data to the client

def server_program():

    variant = 'Ascon-128'

    key   = bytes(bytearray([i % 256 for i in range(16)]))
    nonce = bytes(bytearray([i % 256 for i in range(16)]))
    ad    = bytes(bytearray([i % 256 for i in range(32)]))

    # get the hostname
    host = socket.gethostname()
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


if __name__ == '__main__':
    server_program()
