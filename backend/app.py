from flask import Flask, request, jsonify
import random

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
