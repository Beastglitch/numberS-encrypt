import os
from flask import Flask, render_template, request, jsonify
from encryption import encrypt_text, decrypt_text

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "fallback-secret-key-for-dev")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    text = request.form.get('text', '')
    use_commas = request.form.get('use_commas') == 'true'
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    encrypted_text = encrypt_text(text, use_commas)
    return jsonify({'encrypted': encrypted_text})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    text = request.form.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    decrypted_text = decrypt_text(text)
    return jsonify({'decrypted': decrypted_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
