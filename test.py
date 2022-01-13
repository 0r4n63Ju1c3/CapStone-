import encryption

class key():
    variant = 'Ascon-128'
    key   = bytes(bytearray([i % 256 for i in range(16)]))
    nonce = bytes(bytearray([i % 256 for i in range(16)]))
    ad    = bytes(bytearray([i % 256 for i in range(32)]))

e_key = key()
message = encryption.encrypt(b'Test', e_key)
print(message)
message = encryption.decrypt(message, e_key)
print(message.decode())