import random
import string
import encryption

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def e_key():
    variant = 'Ascon-128'

    key   = bytes(bytearray([i % 256 for i in range(16)]))
    nonce = bytes(bytearray([i % 256 for i in range(16)]))
    ad    = bytes(bytearray([i % 256 for i in range(32)]))

message = randomword(10)
copy_message = message
print(message)
key = e_key()

message = encryption.encrypt(message.encode())
print(message)

message = encryption.decrypt(message)
print(message.decode())

hash_message = encryption.hash(message)
message = encryption.hash(message)
if(message != hash_message):
    print("hashes don't match")
    print("hash_1", hash_message)
    print("hash_2", message)
else:
    print("hashes match")