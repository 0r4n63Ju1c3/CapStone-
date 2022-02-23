import ascon
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

BLOCK_SIZE = 32 # Bytes

variant = 'Ascon-128'

key   = bytes(bytearray([i % 256 for i in range(16)]))
nonce = bytes(bytearray([i % 256 for i in range(16)]))
ad    = bytes(bytearray([i % 256 for i in range(32)]))

def encrypt(msg):
    return ascon.ascon_encrypt(key, nonce , ad[:32], msg, variant)

def decrypt(msg):
    return ascon.ascon_decrypt(key, nonce , ad[:32], msg, variant)

def hash(msg):
    return ascon.ascon_hash(msg, variant="Ascon-Hash", hashlength=32)

def aesEncrypt(message):
    key   = bytes(bytearray([i % 256 for i in range(16)]))
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(message, BLOCK_SIZE))

def aesDecrypt(message):
    key   = bytes(bytearray([i % 256 for i in range(16)]))
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(message).decode()
