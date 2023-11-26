import click
import random
from sympy import primitive_root, isprime, randprime
from termcolor import colored


def mod_exp(base, exp, mod):
    # Modular exponentiation function
    return pow(base, exp, mod)

def elgamal_key_generation():
    # Key generation
    click.secho("ElGamal Key Generation", fg="green", bold=True)
    p = click.prompt("Enter a large prime number (greater than 100)", type=int, default=randprime(10000, 1000000))
    while p < 100:
        p = int(input("Enter a large prime number (greater than 100) PLEASE!: "))

    # Ensure that p is prime
    if not isprime(p):
        click.secho(f"\n{p} is not prime.", fg="red")
        p = randprime(10000, 1000000)
        click.secho(f"{p} is the new prime number generated.", fg="yellow")

    # Choose a primitive root of p
    e1 = primitive_root(p)

    d = random.randint(1, p - 2)
    e2 = mod_exp(e1, d, p)

    public_key = (e1, e2, p)
    private_key = d

    click.secho("\nKey Generation:", fg="cyan")
    click.echo(f"Public Key (e1, e2, p): {public_key}")
    click.echo(f"Private Key (d): {private_key}\n")

    return public_key, private_key

def elgamal_encryption(public_key, plaintext):
    # Encryption
    e1, e2, p = public_key
    r = random.randint(1, p - 2)

    C1 = mod_exp(e1, r, p)
    C2 = (plaintext * pow(e2, r)) % p

    click.secho("Encryption:", fg="blue")
    click.echo(f"Ciphertext (C1, C2): ({C1}, {C2})\n")

    return C1, C2

def elgamal_decryption(private_key, public_key, ciphertext):
    # Decryption
    d = private_key
    e1, e2, p = public_key
    C1, C2 = ciphertext

    inv_C1 = pow(C1, p - 1 - d, p)
    plaintext = (C2 * inv_C1) % p

    return plaintext

# Extra utitlity/CLI enhancement functions
def separator_line():
    click.echo(colored('-' * 50, 'magenta'))

@click.command()
def main():

    banner = r'''
 _______   ___       ________  ________  _____ ______   ________  ___          
|\  ___ \ |\  \     |\   ____\|\   __  \|\   _ \  _   \|\   __  \|\  \         
\ \   __/|\ \  \    \ \  \___|\ \  \|\  \ \  \\\__\ \  \ \  \|\  \ \  \        
 \ \  \_|/_\ \  \    \ \  \  __\ \   __  \ \  \\|__| \  \ \   __  \ \  \       
  \ \  \_|\ \ \  \____\ \  \|\  \ \  \ \  \ \  \    \ \  \ \  \ \  \ \  \____  
   \ \_______\ \_______\ \_______\ \__\ \__\ \__\    \ \__\ \__\ \__\ \_______\
    \|_______|\|_______|\|_______|\|__|\|__|\|__|     \|__|\|__|\|__|\|_______|
                                                                                                                                                                                                                                                                                                   
    '''
    
    
    click.echo(colored(banner, 'cyan'))
    click.secho("CipherCart - ElGamal Encryption and Decryption", fg="white", bg="blue", bold=True)
    click.echo()
    # Key Generation
    public_key, private_key = elgamal_key_generation()

    plaintext = click.prompt('Enter plaintext message (Plaintext should be less than the previously entered prime number)', type=int, default=1)
    separator_line()
    # Encryption
    ciphertext = elgamal_encryption(public_key, plaintext)

    separator_line()

    # Decryption
    decrypted_plaintext = elgamal_decryption(private_key, public_key, ciphertext)
    click.secho("Decryption:", fg="magenta")
    click.echo(f"Decrypted Plaintext: {decrypted_plaintext}\n")

    separator_line()

if __name__ == "__main__":
    main()
