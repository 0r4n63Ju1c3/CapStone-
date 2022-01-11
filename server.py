import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ('127.0.0.1', 1000)
print('starting server')

sock.bind(address)

sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    i = 0;

    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            print('received {!r}'.format(data))
            if data:
                i = i + 1
                print('sending ack to client')
                connection.sendall(('received frame:' + str(i)).encode())
            else:
                print('no data from', client_address)
                break
    finally:
        # Clean up the connection
        connection.close()
