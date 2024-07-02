from flask import Flask, request, jsonify, render_template
import pyotp

app = Flask(__name__)

# Dictionary to store phone numbers and verification codes
verification_codes = {}

@app.route('/phone/<phone_number>', methods=['GET', 'POST'])
def phone(phone_number):
    if request.method == 'POST':
        # Handle POST request to generate code
        verification_code = request.json.get('verification_code')
        if verification_code:
            # Store the phone number and verification code in the dictionary
            verification_codes[phone_number] = verification_code
            print(f"Phone -> {phone_number} \nCode -> {verification_code}")
            return jsonify({'phone': phone_number, 'verification_code': verification_code})
        else:
            return jsonify({'message': 'Missing verification code parameter'}), 400
    elif request.method == 'GET':
        # Retrieve the verification code for the given phone number
        verification_code = verification_codes.get(phone_number)
        if verification_code:
            return render_template('phone.html', phone=phone_number, code=verification_code)
        else:
            return jsonify({'message': 'No verification code found for this phone number'}), 404
        
@app.route('/email/<email>', methods=['GET', 'POST'])
def email(email):
    if request.method == 'POST':
        # Handle POST request to generate code
        verification_code = request.json.get('verification_code')
        if verification_code:
            # Store the email number and verification code in the dictionary
            verification_codes[email] = verification_code
            print(f"Email -> {email} \nCode -> {verification_code}")
            return jsonify({'email': email, 'verification_code': verification_code})
        else:
            return jsonify({'message': 'Missing verification code parameter'}), 400
    elif request.method == 'GET':
        # Retrieve the verification code for the given email number
        verification_code = verification_codes.get(email)
        if verification_code:
            return render_template('email.html', email=email, code=verification_code)
        else:
            return jsonify({'message': 'No verification code found for this email adress'}), 404
        
@app.route('/user/<user>', methods=['GET', 'POST'])
def user(user):
    if request.method == 'GET':
        # Retrieve the verification code for the given user number
        verification_code = verification_codes.get(user)
        return render_template('totp.html', code=verification_code, username=user)
    elif request.method == 'POST':
        totp = pyotp.TOTP(user)
        verification_code = totp.now()
        verification_codes[user] = verification_code
        print(f"User -> {user} \nCode -> {verification_code}")
        return jsonify({'message': "Token Created with success"})

if __name__ == '__main__':
    app.run( host="0.0.0.0",port=8001)
