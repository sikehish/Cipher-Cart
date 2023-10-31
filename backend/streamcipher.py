import click
import random
from termcolor import colored
import os

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

@click.command()
def main():
    os.system('cls' if os.name == 'nt' else 'clear')  

    banner = r'''
 ________  ___  ________  ___  ___  _______   ________          ________  ________  ________  _________   
|\   ____\|\  \|\   __  \|\  \|\  \|\  ___ \ |\   __  \        |\   ____\|\   __  \|\   __  \|\___   ___\ 
\ \  \___|\ \  \ \  \|\  \ \  \\\  \ \   __/|\ \  \|\  \       \ \  \___|\ \  \|\  \ \  \|\  \|___ \  \_| 
 \ \  \    \ \  \ \   ____\ \   __  \ \  \_|/_\ \   _  _\       \ \  \    \ \   __  \ \   _  _\   \ \  \  
  \ \  \____\ \  \ \  \___|\ \  \ \  \ \  \_|\ \ \  \\  \|       \ \  \____\ \  \ \  \ \  \\  \|   \ \  \ 
   \ \_______\ \__\ \__\    \ \__\ \__\ \_______\ \__\\ _\        \ \_______\ \__\ \__\ \__\\ _\    \ \__\
    \|_______|\|__|\|__|     \|__|\|__|\|_______|\|__|\|__|        \|_______|\|__|\|__|\|__|\|__|    \|__|
    '''
    
    click.echo(colored(banner, 'cyan'))
    click.echo('Cipher Cart - Secure Data Encryption/Decryption')
    click.echo('---------------------------------------------')

    secret_key = click.prompt('Enter Secret Key', default=str(random.getrandbits(64)), show_default=True)
    plaintext = click.prompt('Enter Plain Text', default='Hello World!', show_default=True)

    ciphertext = encrypt(plaintext.encode('utf-8'), secret_key)
    decrypted_text = decrypt(ciphertext, secret_key)

    
    click.echo(f'Ciphertext: {colored(ciphertext.hex(), "green")}')
    click.echo(f'Decrypted Text: {colored(decrypted_text.decode("utf-8"), "green")}')
    click.echo('---------------------------------------------')


if __name__ == '__main__':
    main()
