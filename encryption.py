import ascon

def encrypt(msg, e_key):
    return ascon.ascon_encrypt(e_key.key, e_key.nonce , e_key.ad[:32], msg, e_key.variant)

def decrypt(msg, e_key):
    return ascon.ascon_decrypt(e_key.key, e_key.nonce , e_key.ad[:32], msg, e_key.variant)
