import random
import string
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
BLOCK_SIZE = 32 # Bytes

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

key   = bytes(bytearray([i % 256 for i in range(16)]))
cipher = AES.new(key, AES.MODE_ECB)
message = bytes(randomword(10), 'utf-8')
data = cipher.encrypt(pad(message, BLOCK_SIZE))
print(data)
decipher = AES.new(key, AES.MODE_ECB)
data_dec = decipher.decrypt(data)
print(unpad(data_dec, BLOCK_SIZE).decode())