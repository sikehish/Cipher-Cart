import random
from sympy import primitive_root, isprime

def mod_exp(base, exp, mod):
    # Modular exponentiation function
    return pow(base, exp, mod)

def elgamal_key_generation():
    # Key generation
    p = 997  # Replace with a large prime in practice

    # Ensure that p is prime
    while not isprime(p):
        p = random.randint(1000, 100000)  # Adjust the range as needed

    # Choose a primitive root of p
    e1 = primitive_root(p)

    d = random.randint(1, p - 2)
    e2 = mod_exp(e1, d, p)

    public_key = (e1, e2, p)
    private_key = d

    print("Key Generation:")
    print(f"Public Key (e1, e2, p): {public_key}")
    print(f"Private Key (d): {private_key}\n")

    return public_key, private_key


def elgamal_encryption(public_key, plaintext):
    # Encryption
    e1, e2, p = public_key
    r = random.randint(1, p - 2)

    C1 = mod_exp(e1, r, p)
    C2 = (plaintext * pow(e2, r)) % p

    print("Encryption:")
    print(f"Ciphertext (C1, C2): ({C1}, {C2})\n")

    return C1, C2

def elgamal_decryption(private_key, public_key, ciphertext):
    # Decryption
    d = private_key
    e1,e2,p=public_key
    C1, C2 = ciphertext

    inv_C1 = pow(C1, p - 1 - d)
    plaintext = (C2 * inv_C1) % p

    print("Decryption:")
    print(f"Decrypted Plaintext: {plaintext}\n")

    return plaintext

def main():
    plaintext = int(input("Enter plaintext message: "))

    # Key Generation
    public_key, private_key = elgamal_key_generation()

    # Encryption
    ciphertext = elgamal_encryption(public_key, plaintext)

    # Decryption
    decrypted_plaintext = elgamal_decryption(private_key, public_key, ciphertext)

if __name__ == "__main__":
    main()
