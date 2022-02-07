import ascon

variant = 'Ascon-128'

key   = bytes(bytearray([i % 256 for i in range(16)]))
nonce = bytes(bytearray([i % 256 for i in range(16)]))
ad    = bytes(bytearray([i % 256 for i in range(32)]))

def encrypt(msg):
    return ascon.ascon_encrypt(key, nonce , ad[:32], msg, variant)

def decrypt(msg):
    return ascon.ascon_decrypt(key, nonce , ad[:32], msg, variant)

def asc_hash(msg):
    return ascon.ascon_hash(msg, variant="Ascon-Hash", hashlength=32)