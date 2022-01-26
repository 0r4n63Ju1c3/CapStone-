import random
import string
import encryption

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

message = randomword(10)
print(message)

message = encryption.encrypt(message.encode())
print(message)

message = encryption.decrypt(message)
print(message.decode())