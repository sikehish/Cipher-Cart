import random

def generate_keystream(secret_key, length):
    random.seed(secret_key) 
    keystream = [random.randint(0, 255) for _ in range(length)]  
    return bytes(keystream)

def encrypt(plaintext, secret_key):
    keystream = generate_keystream(secret_key, len(plaintext))
    ciphertext = bytes(p ^ k for p, k in zip(plaintext, keystream))
    return ciphertext

def decrypt(ciphertext, secret_key):
    keystream = generate_keystream(secret_key, len(ciphertext))
    plaintext = bytes(c ^ k for c, k in zip(ciphertext, keystream))
    return plaintext

if __name__ == '__main__':
    secret_key = input("Enter secret key: ") 
    plaintext = input("Enter plaintext: ").encode('utf-8')
    # OR plaintext = bytes(input("Enter plaintext: "),encoding='utf-8')
    
    ciphertext = encrypt(plaintext, secret_key)
    decrypted_text = decrypt(ciphertext, secret_key)
    
    print(f'Plaintext: {plaintext.decode("utf-8")}')
    print(f'Ciphertext: {ciphertext.hex()}')
    print(f'Decrypted Text: {decrypted_text.decode("utf-8")}')
