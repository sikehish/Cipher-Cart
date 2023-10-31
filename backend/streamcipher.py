def generate_keystream(secret_key, length):
    # A simple keystream generator using a pseudo-random key.
    keystream = []
    key_length = len(secret_key)
    for i in range(length):
        keystream.append(secret_key[i % key_length])
    print("Output ", keystream)
    return bytes(keystream)

def encrypt(plaintext, secret_key):
    keystream = generate_keystream(secret_key, len(plaintext))
    ciphertext = bytes(p ^ k for p, k in zip(plaintext, keystream))
    return ciphertext

def decrypt(ciphertext, secret_key):
    keystream = generate_keystream(secret_key, len(ciphertext))
    plaintext = bytes(c ^ k for c, k in zip(ciphertext, keystream))
    return plaintext

if __name__ == "__main__":
    secret_key = b'\x01\x23\x45\x67\x89\xAB\xCD\xEF'
    plaintext = b'This is a variable length plaintext.'

    # Encrypt the plaintext
    ciphertext = encrypt(plaintext, secret_key)
    print(f"Ciphertext: {ciphertext.hex()}")

    # Decrypt the ciphertext
    decrypted_plaintext = decrypt(ciphertext, secret_key)
    print(f"Decrypted Plaintext: {decrypted_plaintext.decode('utf-8')}")
