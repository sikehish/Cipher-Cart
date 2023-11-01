import click
import random
from termcolor import colored
import os

def pad(plaintext):
    padding = BLOCK_SIZE - len(plaintext) % BLOCK_SIZE
    return plaintext + bytes([padding] * padding)

def unpad(padded_text):
    padding = padded_text[-1]
    if padding > 0 and padding <= BLOCK_SIZE:
        return padded_text[:-padding]
    else:
        return padded_text

def generate_key(key_size):
    return bytes([random.randint(0, 255) for _ in range(key_size)])

def encrypt_block(block, key):
    return bytes(p ^ k for p, k in zip(block, key))

def decrypt_block(ciphertext_block, key):
    return bytes(c ^ k for c, k in zip(ciphertext_block, key))

def encrypt(plaintext, key):
    plaintext = pad(plaintext)
    ciphertext = b''

    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i + BLOCK_SIZE]
        click.echo(f'Encrypting Block {i // BLOCK_SIZE + 1} (Size {len(block)} bytes):')
        click.echo(f'Block {i // BLOCK_SIZE + 1} (Plain Text): {block.hex()}')
        ciphertext_block = encrypt_block(block, key)
        click.echo(f'Block {i // BLOCK_SIZE + 1} (Encrypted): {ciphertext_block.hex()}')
        ciphertext += ciphertext_block

    return ciphertext

def decrypt(ciphertext, key):
    plaintext = b''

    for i in range(0, len(ciphertext), BLOCK_SIZE):
        ciphertext_block = ciphertext[i:i + BLOCK_SIZE]
        click.echo(f'Decrypting Block {i // BLOCK_SIZE + 1} (Size {len(ciphertext_block)} bytes):')
        click.echo(f'Block {i // BLOCK_SIZE + 1} (Encrypted): {ciphertext_block.hex()}')
        block = decrypt_block(ciphertext_block, key)
        click.echo(f'Block {i // BLOCK_SIZE + 1} (Decrypted): {block.hex()}')
        plaintext += block

    return unpad(plaintext)

def faded_default_text(text):
    return f"\033[90m{text}\033[0m"

def separator_line():
    click.echo('-' * 60)

def heading_text(text):
    return f"\n== {text} ==\n"

@click.command()
def main():
    os.system('cls' if os.name == 'nt' else 'clear')  

    banner = r'''
 ________  ___  ________  ___  ___  _______   ________          ________  ________  ________  _________   
|\   ____\|\  \|\   __  \|\  \|\  \|\  ___ \ |\   __  \        |\   ____\|\   __  \|\   __  \|\___   ___\ 
\ \  \___|\ \  \ \  \|\  \ \  \\\  \ \   __/|\ \  \|\  \       \ \  \___|\ \  \|\  \ \  \|\  \|___ \  \_| 
 \ \  \    \ \  \ \   ____\ \   __  \ \ _|/_\ \   _  _\       \ \  \    \ \   __  \ \   _  _\   \ \  \  
  \ \  \____\ \  \ \  \___|\ \  \ \  \ \  \|\ \ \  \\  \|       \ \  \____\ \  \|\  \ \  \\  \|   \ \  \ 
   \ \_______\ \__\ \__\    \ \__\ \__\ \_______\ \__\\ _\        \ \_______\ \__\ \__\ \__\\ _\    \ \__\
    \|_______|\|__|\|__|     \|__|\|__|\|_______|\|__|\|__|        \|_______|\|__|\|__|\|__|\|__|    \|__|
    '''
    
    click.echo(colored(banner, 'cyan'))
    click.echo('Cipher Cart - Secure Data using Block Cipher')
    click.echo('---------------------------------------------')

    global BLOCK_SIZE
    BLOCK_SIZE = click.prompt('Enter Block Size', type=int, default=16)

    key = generate_key(BLOCK_SIZE)
    plaintext = click.prompt('Enter Plain Text', default=faded_default_text('Hello World!'))

    click.echo(f'Secret Key: {key.hex()}')
    
    separator_line()
    click.echo(heading_text('Encryption Process'))
    separator_line()
    ciphertext = encrypt(plaintext.encode('utf-8'), key)
    click.echo(f'Ciphertext: {colored(ciphertext.hex(), "green")}')

    separator_line()
    click.echo(heading_text('Decryption Process'))
    separator_line()
    decrypted_text = decrypt(ciphertext, key)
    click.echo(f'Decrypted Text: {colored(decrypted_text.decode("utf-8"), "green")}')

if __name__ == '__main__':
    main()
