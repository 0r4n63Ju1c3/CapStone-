import random
import string
import encryption

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

message = randomword(10)
copy_message = message
print(message)

message = encryption.encrypt(message.encode())
print(message)

message = encryption.decrypt(message)
print(message.decode())

hash_message = encryption.asc_hash(copy_message.encode())
message = encryption.asc_hash(message)
if(message != hash_message):
    print("hashes don't match")
    print("hash_1", hash_message)
    print("hash_2", message)
else:
    print("hashes match")