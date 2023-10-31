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

def faded_default_text(text):
    return f"\033[90m{text}\033[0m"  # \033[90m sets text color to gray. It adds ANSI color codes to set the text color to gray


@click.command()
def main():
    os.system('cls' if os.name == 'nt' else 'clear') #Clears the system console 

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
    click.echo('Cipher Cart - Secure Data using Stream Cipher')
    click.echo('---------------------------------------------')

    secret_key = click.prompt('Enter Secret Key', default=faded_default_text(str(random.getrandbits(64))))
    plaintext = click.prompt('Enter Plain Text', default=faded_default_text('Hello World!'))

    ciphertext = encrypt(plaintext.encode('utf-8'), secret_key)
    decrypted_text = decrypt(ciphertext, secret_key)

    
    click.echo(f'Ciphertext: {colored(ciphertext.hex(), "green")}')
    click.echo(f'Decrypted Text: {colored(decrypted_text.decode("utf-8"), "green")}')
    click.echo('---------------------------------------------')


if __name__ == '__main__':
    main()
