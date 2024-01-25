from flask import Flask, render_template, request, jsonify
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

app = Flask(__name__)

# Generate RSA key pair
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

@app.route('/')
def index():
    return render_template('index.html', public_key=public_key.decode())

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_data = bytes.fromhex(request.form.get('encrypted_data'))
    cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return jsonify({'decrypted_data': decrypted_data})


if __name__ == '__main__':
    app.run(debug=True)
