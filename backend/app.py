from flask import Flask, request, jsonify
import random

app = Flask(__name__)


# Stream cipher methods
def stream_generate_keystream(secret_key, length):
    random.seed(secret_key)
    keystream = [random.randint(0, 255) for _ in range(length)]
    return bytes(keystream)

def stream_encrypt(plaintext, secret_key):
    keystream = stream_generate_keystream(secret_key, len(plaintext))
    ciphertext = bytes(p ^ k for p, k in zip(plaintext, keystream))
    return ciphertext

def stream_decrypt(ciphertext, secret_key):
    keystream = stream_generate_keystream(secret_key, len(ciphertext))
    plaintext = bytes(c ^ k for c, k in zip(ciphertext, keystream))
    return plaintext

# Block cipher methods
def pad(plaintext, block_size):
    padding = block_size - len(plaintext) % block_size
    return plaintext + bytes([padding] * padding)

def unpad(padded_text, block_size):
    padding = padded_text[-1]
    if padding > 0 and padding <= block_size:
        return padded_text[:-padding]
    else:
        return padded_text

def generate_key(block_size):
    return bytes([random.randint(0, 255) for _ in range(block_size)])

def encrypt_block(block, key):
    return bytes(p ^ k for p, k in zip(block, key))

def decrypt_block(ciphertext_block, key):
    return bytes(c ^ k for c, k in zip(ciphertext_block, key))

def encrypt(plaintext, key, block_size):
    plaintext = pad(plaintext)
    ciphertext = b''
    for i in range(0, len(plaintext), block_size):
        block = plaintext[i:i + block_size]
        ciphertext_block = encrypt_block(block, key)
        ciphertext += ciphertext_block

    return ciphertext

def decrypt(ciphertext, key, block_size):
    plaintext = b''

    for i in range(0, len(ciphertext), block_size):
        ciphertext_block = ciphertext[i:i + block_size]
        block = decrypt_block(ciphertext_block, key)    
        plaintext += block

    return unpad(plaintext)

# Stream cipher endpoints
@app.route('/stream-cipher/encrypt', methods=['POST'])
def stream_encrypt_endpoint():
    data = request.get_json()
    secret_key = data.get('secret_key', "")
    plaintext = data.get('plaintext', "")

    if not secret_key or not plaintext:
        return jsonify({'error': 'Both secret_key and plaintext are required.'}), 400

    ciphertext = stream_encrypt(plaintext.encode('utf-8'), secret_key)
    return jsonify({'ciphertext': ciphertext.hex()})

@app.route('/stream-cipher/decrypt', methods=['POST'])
def decrypt_endpoint():
    data = request.get_json()
    secret_key = data.get('secret_key', "")
    ciphertext = data.get('ciphertext', "")

    if not secret_key or not ciphertext:
        return jsonify({'error': 'Both secret_key and ciphertext are required.'}), 400

    try:
        ciphertext_bytes = bytes.fromhex(ciphertext)
    except ValueError:
        return jsonify({'error': 'Invalid hex-encoded ciphertext.'}), 400

    decrypted_text = stream_decrypt(ciphertext_bytes, secret_key)
    return jsonify({'decrypted_text': decrypted_text.decode('utf-8')})


# Block cipher endpoints

@app.route('/block-cipher/encrypt', methods=['POST'])
def encrypt_api():
    data = request.get_json()
    plaintext = data['plaintext']
    block_size=data['block_size']

    key = generate_key(block_size)
    ciphertext = encrypt(plaintext.encode('utf-8'), key, block_size)

    return jsonify({
        'key': key.hex(),
        'ciphertext': ciphertext.hex()
    })

@app.route('/block-cipher/decrypt', methods=['POST'])
def decrypt_api():
    data = request.get_json()
    ciphertext_hex = data['ciphertext']
    key_hex = data['key']
    block_size = data['block_size']

    key = bytes.fromhex(key_hex)
    ciphertext = bytes.fromhex(ciphertext_hex)
    decrypted_text = decrypt(ciphertext, key, block_size)

    return jsonify({
        'decrypted_text': decrypted_text.decode('utf-8')
    })


if __name__ == '__main__':
    app.run(debug=True)
