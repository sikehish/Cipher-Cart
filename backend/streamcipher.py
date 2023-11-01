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

def print_heading(heading, color="cyan"):
    click.echo(colored('\n' + heading, color))

def print_subtitle(subtitle):
    click.echo(colored(subtitle, 'blue') + " ", nl=False)

def print_content(content, color='white'):
    click.echo(colored(content, color))

def separator_line():
    click.echo(colored('-' * 50, 'magenta'))

def heading_text(text):
    return f"== {text} ==\n"


@click.command()
def main():
    os.system('cls' if os.name == 'nt' else 'clear') #Clears the system console 

    banner = r'''
 ________  _________  ________  _______   ________  _____ ______           ________  ___  ________  ___  ___  _______   ________     
|\   ____\|\___   ___\\   __  \|\  ___ \ |\   __  \|\   _ \  _   \        |\   ____\|\  \|\   __  \|\  \|\  \|\  ___ \ |\   __  \    
\ \  \___|\|___ \  \_\ \  \|\  \ \   __/|\ \  \|\  \ \  \\\__\ \  \       \ \  \___|\ \  \ \  \|\  \ \  \\\  \ \   __/|\ \  \|\  \   
 \ \_____  \   \ \  \ \ \   _  _\ \  \_|/_\ \   __  \ \  \\|__| \  \       \ \  \    \ \  \ \   ____\ \   __  \ \  \_|/_\ \   _  _\  
  \|____|\  \   \ \  \ \ \  \\  \\ \  \_|\ \ \  \ \  \ \  \    \ \  \       \ \  \____\ \  \ \  \___|\ \  \ \  \ \  \_|\ \ \  \\  \| 
    ____\_\  \   \ \__\ \ \__\\ _\\ \_______\ \__\ \__\ \__\    \ \__\       \ \_______\ \__\ \__\    \ \__\ \__\ \_______\ \__\\ _\ 
   |\_________\   \|__|  \|__|\|__|\|_______|\|__|\|__|\|__|     \|__|        \|_______|\|__|\|__|     \|__|\|__|\|_______|\|__|\|__|
   \|_________|                                                                                                                      
                                                                                                                                                                                                                                                     
    '''
    
    click.echo(colored(banner, 'cyan'))
    print_heading('Cipher Cart - Secure Data using Stream Cipher')
    click.echo('---------------------------------------------')

    secret_key = click.prompt('Enter Secret Key', default=faded_default_text(str(random.getrandbits(64))))
    plaintext = click.prompt('Enter Plain Text', default=faded_default_text('Hello World!'))

    separator_line()
    print_heading(heading_text('Encryption Process'), color="red")
    separator_line()

    print_subtitle('Secret Key:')
    print_content(secret_key, 'blue')
    print_subtitle('Plaintext:')
    print_content(plaintext, 'white')
    print_heading('Generating Keystream...')
    keystream = generate_keystream(secret_key, len(plaintext))
    print_subtitle('Keystream:')
    print_content(keystream.hex(), 'yellow')
    
    print_heading('\nEncrypting, by performing xor on the keystream and plaintext...')
    ciphertext = encrypt(plaintext.encode('utf-8'), secret_key)

    print_subtitle('Ciphertext:')
    print_content(ciphertext.hex(), 'green')

    separator_line()
    print_heading(heading_text('Decryption Process'), color="red")
    separator_line()

    print_heading('Generating Keystream...')
    keystream = generate_keystream(secret_key, len(ciphertext))
    print_subtitle('Keystream:')
    print_content(keystream.hex(), 'yellow')
    print_subtitle('Given Ciphertext:')
    print_content(ciphertext.hex(), 'green')
    print_heading('\nDecrypting, by performing xor on the keystream and cipher text...')
    decrypted_text = decrypt(ciphertext, secret_key)
    print_subtitle('Decrypted Text:')
    print_content(decrypted_text.decode('utf-8'), 'green')

    click.echo('---------------------------------------------')

if __name__ == '__main__':
    main()