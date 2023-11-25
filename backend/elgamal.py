import random

def mod_exp(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent = exponent // 2
    return result

def elgamal_key_generation():
    # Step 1: Key Generation
    p = 23  # Replace with a large prime number
    d = random.randint(1, p - 2)
    e1 = random.choice([i for i in range(2, p) if pow(i, p - 1, p) == 1])
    e2 = mod_exp(e1, d, p)

    # Public Key: (e1, e2, p)
    public_key = (e1, e2, p)
    # Private Key: d
    private_key = d

    return public_key, private_key

def elgamal_encryption(public_key, plaintext):
    e1, e2, p = public_key
    # Step 2: Encryption
    r = random.randint(1, p - 2)
    C1 = mod_exp(e1, r, p)
    C2 = (plaintext * mod_exp(e2, r, p)) % p

    # Ciphertext: (C1, C2)
    ciphertext = (C1, C2)
    return ciphertext

def elgamal_decryption(private_key, public_key, ciphertext):
    d, p = private_key, public_key[2]
    C1, C2 = ciphertext
    # Step 3: Decryption
    inv_C1 = mod_exp(C1, p - 1 - d, p)
    plaintext = (C2 * inv_C1) % p
    return plaintext

def main():
    # Take plaintext input
    plaintext = int(input("Enter the plaintext message: "))

    # Key Generation
    public_key, private_key = elgamal_key_generation()
    print("\nKey Generation:")
    print(f"Public Key (e1, e2, p): {public_key}")
    print(f"Private Key (d): {private_key}")

    # Encryption
    ciphertext = elgamal_encryption(public_key, plaintext)
    print("\nEncryption:")
    print(f"Ciphertext (C1, C2): {ciphertext}")

    # Decryption
    decrypted_plaintext = elgamal_decryption(private_key, public_key, ciphertext)
    print("\nDecryption:")
    print(f"Decrypted Plaintext: {decrypted_plaintext}")

if __name__ == "__main__":
    main()
