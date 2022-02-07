import ascon
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

BLOCK_SIZE = 32 # Bytes

def encrypt(msg, e_key):
    return ascon.ascon_encrypt(e_key.key, e_key.nonce , e_key.ad[:32], msg, e_key.variant)

def decrypt(msg, e_key):
    return ascon.ascon_decrypt(e_key.key, e_key.nonce , e_key.ad[:32], msg, e_key.variant)

def aesEncrypt(message):
    key   = bytes(bytearray([i % 256 for i in range(16)]))
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(message, BLOCK_SIZE))

def aesDecrypt(message):
    key   = bytes(bytearray([i % 256 for i in range(16)]))
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(message).decode()
