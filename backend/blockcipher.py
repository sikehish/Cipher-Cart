import click
import random
from termcolor import colored
import os

BLOCK_SIZE = 16  # block size in bytes

def pad(plaintext):
    # Pad the plaintext to be a multiple of BLOCK_SIZE
    padding = BLOCK_SIZE - len(plaintext) % BLOCK_SIZE
    return plaintext + bytes([padding] * padding)

def unpad(padded_text):
    # Remove the padding from the plaintext
    padding = padded_text[-1]
    if padding > 0 and padding <= BLOCK_SIZE:
        return padded_text[:-padding]
    else:
        return padded_text

def encrypt_block(block, key):
    return bytes(p ^ k for p, k in zip(block, key))

def decrypt_block(ciphertext_block, key):
    return bytes(c ^ k for c, k in zip(ciphertext_block, key))

def encrypt(plaintext, key):
    plaintext = pad(plaintext)
    ciphertext = b''

    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i + BLOCK_SIZE]
        ciphertext_block = encrypt_block(block, key)
        ciphertext += ciphertext_block

    return ciphertext

def decrypt(ciphertext, key):
    plaintext = b''

    for i in range(0, len(ciphertext), BLOCK_SIZE):
        ciphertext_block = ciphertext[i:i + BLOCK_SIZE]
        block = decrypt_block(ciphertext_block, key)
        plaintext += block

    return unpad(plaintext)

def faded_default_text(text):
    return f"\033[90m{text}\033[0m" 
@click.command()
def main():
    os.system('cls' if os.name == 'nt' else 'clear')  

    banner = r'''
 ________  ___  ________  ___  ___  _______   ________          ________  ________  ________  _________   
|\   ____\|\  \|\   __  \|\  \|\  \|\  ___ \ |\   __  \        |\   ____\|\   __  \|\   __  \|\___   ___\ 
\ \  \___|\ \  \ \  \|\  \ \  \\\  \ \   __/|\ \  \|\  \       \ \  \___|\ \  \|\  \ \  \|\  \|___ \  \_| 
 \ \  \    \ \  \ \   ____\ \   __  \ \  \_|/_\ \   _  _\       \ \  \    \ \   __  \ \   _  _\   \ \  \  
  \ \  \____\ \  \ \  \___|\ \  \ \  \ \  \_|\ \ \  \\  \|       \ \  \____\ \  \|\  \ \  \\  \|   \ \  \ 
   \ \_______\ \__\ \__\    \ \__\ \__\ \_______\ \__\\ _\        \ \_______\ \__\ \__\ \__\\ _\    \ \__\
    \|_______|\|__|\|__|     \|__|\|__|\|_______|\|__|\|__|        \|_______|\|__|\|__|\|__|\|__|    \|__|
    '''
    
    click.echo(colored(banner, 'cyan'))
    click.echo('Cipher Cart - Secure Data using Block Cipher')
    click.echo('---------------------------------------------')

    key = click.prompt('Enter Secret Key', default=faded_default_text('RandomKey' + str(random.getrandbits(64))))
    plaintext = click.prompt('Enter Plain Text', default=faded_default_text('Hello World!'))

    ciphertext = encrypt(plaintext.encode('utf-8'), key)
    decrypted_text = decrypt(ciphertext, key)

    
    click.echo(f'Ciphertext: {colored(ciphertext.hex(), "green")}')
    click.echo(f'Decrypted Text: {colored(decrypted_text.decode("utf-8"), "green")}')
    click.echo('---------------------------------------------')

if __name__ == '__main__':
    main()
