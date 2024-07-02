from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
import random
from datetime import datetime, timedelta
import jwt
import requests
import json
import re
import pyotp
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create Table for user database
c.execute('''CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               uname TEXT NOT NULL,
               email TEXT NOT NULL,
               password TEXT NOT NULL,
               phone TEXT NOT NULL,
               role TEXT NOT NULL,
               points TEXT NOT NULL,
               location_whitelist TEXT NOT NULL,
               ip_whitelist TEXT NOT NULL,
               device_whitelist TEXT NOT NULL,
               refresh_code TEXT NOT NULL,
               auth_code TEXT NOT NULL,
               refresh_time TEXT NOT NULL,
               auth_time TEXT NOT NULL
             )''')
c.execute("DELETE FROM users")

# Create Default Users
users = [
    ("Private", "Private@military.pt", "12345"),
    ("Corporal", "Corporal@military.pt", "12346"),
    ("Sergeant", "Sergeant@military.pt", "12347"),
    ("Major", "Major@military.pt", "12348"),

    ("Believer", "Believer@religious.pt", "23456"),
    ("Priest", "Priest@religious.pt", "23457"),
    ("Bishop", "Bishop@religious.pt", "23458"),
    ("Pope", "Pope@religious.pt", "23459"),

    ("Looker", "Looker@cooking.pt", "34567"),
    ("Eater", "Eater@cooking.pt", "34568"),
    ("Cook", "Cook@cooking.pt", "34569"),
    ("Admin", "Admin@cooking.pt", "34570")
]
for role, email, phone in users:
    c.execute('''INSERT INTO users (uname, email, password, phone, role, points, location_whitelist, ip_whitelist, device_whitelist, refresh_code, auth_code, refresh_time, auth_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (role, email, role, phone, role, '{}', '', '', '', '', '', '', ''))

# Create Table for bruteforce database
c.execute('''CREATE TABLE IF NOT EXISTS bruteforce (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               ip TEXT NOT NULL,
               failed_tries TEXT NOT NULL
             )''')

c.execute("DELETE FROM bruteforce")

conn.commit()
conn.close()

# Transform the role into a clearance level
role_to_clearance = {"Private": "Unclassified", "Corporal": "Restricted", "Sergeant": "Confidential", "Major": "Top-Secret",
                     "Believer": "Comment", "Priest": "Recomendation", "Bishop": "Teaching", "Pope": "ReligiousLaw",
                     "Looker": "Comment", "Eater": "Evaluation", "Cook": "Recepy", "Admin": "Rule"
                     }

# Roles for each service
military_roles = ["Private", "Corporal", "Sergeant", "Major"]
religious_roles = ["Believer", "Priest", "Bishop", "Pope"]
cooking_roles = ["Looker", "Eater", "Cook", "Admin"]


@app.route('/login' , methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    # Get fields
    username = request.form['username']
    session['username'] = username
    password = request.form['password']

    # Debug
    device = request.form['device']
    session['device'] = device
    location = request.form['location']
    session['location'] = location
    ip_address = request.form['ip']
    if not validate_ip_address(ip_address):
      return redirect(url_for('login'))
    session['ip_address'] = ip_address

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    query = '''SELECT * FROM users WHERE uname = ?'''
    c.execute(query, (username,))
    user = c.fetchone()
    conn.commit()
    conn.close()

    # User not Found
    if not user:
      return redirect(url_for('login'))
    
    session['user_role'] = user[5]
    
    get_mfa_num(device, location, ip_address, user)

    # Validate Password
    password_on_db = user[3]
    if not password_on_db == password:
      # add points to session
      brute_force_attempt()
      return redirect(url_for('login'))
    
    elif(session.get('mfa') > 1):
      generate_email_otp()
      return redirect(url_for('verify_email_code'))
    
    user_passed_authentication()
    
    # If user came from /change password
    if session.get('changing_password'):
      return redirect(url_for('change_pass'))
    
    user_role = session.get('user_role')
    if user_role in military_roles:
      return redirect(f'http://localhost:8010/login?uname={username}&location={location}&ip_address={ip_address}&device={device}')
    elif user_role in religious_roles:
      return redirect(f'http://localhost:8011/login?uname={username}&location={location}&ip_address={ip_address}&device={device}')
    elif user_role in cooking_roles:
      return redirect(f'http://localhost:8012/login?uname={username}&location={location}&ip_address={ip_address}&device={device}')
  
  if 'location' in request.args:
    return render_template('login.html', default_device=request.args.get('device'), default_location=request.args.get('location'), default_ip=request.args.get('ip_address'))
  
  return render_template('login.html', default_ip="1.1.1.1")

@app.route('/register' , methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    phone = request.form['phone']
    role = request.form['role']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''INSERT INTO users (uname, email, password, phone, role, points, location_whitelist, ip_whitelist, device_whitelist,refresh_code,auth_code, refresh_time,auth_time ) VALUES (?, ?, ?, ?, ?, '{}',  '', '', '', '', '', '', '')''', (username, email, password, phone, role))
    conn.commit()
    conn.close()

    return redirect(url_for('login'))

  return render_template('register.html')


@app.route('/change_pass' , methods=['GET', 'POST'])
def change_pass():
  if request.method == 'POST':
    session['changing_password'] = False

    password = request.form['password']
    newpassword = request.form['newpassword']

    username = session.get('username')
    device = session.get('device')
    location = session.get('location')
    ip_address = session.get('ip_address')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT password FROM users WHERE uname = ?''', (username,))
    db_password = c.fetchone()[0]
    conn.commit()
    conn.close()

    # Validate Password
    if not db_password == password:
      return redirect(f'http://localhost:8080/change_pass?location={location}&ip_address={ip_address}&device={device}')
      
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''UPDATE users SET password = ? WHERE uname = ?''', (newpassword , username))
    conn.commit()
    conn.close()
    
    user_role = session.get('user_role')
    if user_role in military_roles:
      return redirect(f'http://localhost:8010/login?uname={username}&location={location}&ip_address={ip_address}&device={device}')
    elif user_role in religious_roles:
      return redirect(f'http://localhost:8011/login?uname={username}&location={location}&ip_address={ip_address}&device={device}')
    elif user_role in cooking_roles:
      return redirect(f'http://localhost:8012/login?uname={username}&location={location}&ip_address={ip_address}&device={device}')
  
  
  # redirect to make trigger number of mfa necessary before changing password
  if not session.get('changing_password', False):
    session['changing_password'] = True
    return redirect(f'http://localhost:8080/login?location={request.args.get("location")}&ip_address={request.args.get("ip_address")}&device={request.args.get("device")}')
  return render_template('change_pass.html')

# Get bruteforce_attempts of a user from app to verify if user needs to re-authenticate
@app.route('/recalculate_points' , methods=['GET'])
def recalculate_points():
  device = request.json['device']
  ip_address = request.json['ip']
  location = request.json['location']
  username = request.json['username']

  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute("SELECT * FROM users WHERE uname = ?", (username,))
  user = c.fetchone()
  conn.commit()
  conn.close()

  get_mfa_num(device, location, ip_address, user)

  return jsonify({'message': session['mfa']})

def get_mfa_num(device, location, ip_address, user):

  user_session = f"{device}:{location}:{ip_address}"
  username = user[1]
  sessions = json.loads(user[6])

  # If the session doesn't exist create one and get points
  if user_session not in sessions:
    # Get points for the current session
    sessions[user_session] = calculate_points(user, device, location, ip_address)

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    sessions_string = json.dumps(sessions)
    c.execute('''UPDATE users SET points = ? WHERE uname = ?''', (sessions_string, username))
    conn.commit()
    conn.close()

  session['current_user_session'] = user_session

  # Get session and spraying points
  total_points = sessions[user_session] + get_password_spraying_points()

  # Add additional points for user who is changing password
  if session.get('changing_password'):
    total_points += 200
  
  # Calculation of the number of mfa for the respective Services
  if user[5] in military_roles:
    if total_points > 100:
      session['mfa'] = 4
    elif total_points > 80:
      session['mfa'] = 3
    elif total_points > 20:
      session['mfa'] = 2
    else:
      session['mfa'] = 1
  elif user[5] in religious_roles:
    if total_points > 100:
      session['mfa'] = 3
    elif total_points > 60:
      session['mfa'] = 2
    elif total_points > 30:
      session['mfa'] = 1
    else:
      session['mfa'] = 0
  elif user[5] in cooking_roles:
    if total_points > 200:
      session['mfa'] = 2
    elif total_points > 100:
      session['mfa'] = 1
    else:
      session['mfa'] = 0
    
def calculate_points(values, device, location, ip_address):
  location_whitelist = values[7].split(",")
  ip_whitelist = values[8].split(",")
  device_whitelist = values[9].split(",")
  points = 0
  if location not in location_whitelist:
    points += 60
  if ip_address not in ip_whitelist:
    points += 20
  if device not in device_whitelist:
    points += 200
  
  return points

@app.route ('/authorization' ,methods=['GET'])
def authorization():
  
  username = request.json

  # Create Authorization Code
  auth_code = random.randint(10000, 99999)

  # Get expiration date
  current_time = datetime.now()
  current_time = current_time.replace(microsecond=0)
  expiration_time = current_time + timedelta(seconds=20)

  # Add token and expiration date to db
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute('''UPDATE users SET auth_code = ?, auth_time = ? WHERE uname = ?''', (auth_code, expiration_time, username))
  conn.commit()
  conn.close()

  return jsonify({'auth_code': auth_code})

@app.route('/refresh' , methods=['GET'])
def refresh():

  # Get user for auth_code
  auth_code = request.json
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute('''SELECT * FROM users WHERE auth_code = ?''', (auth_code,))
  user = c.fetchone()
  conn.commit()
  conn.close()
  
  if not user:
    return jsonify({'message': 'No user found'}), 401
  
  username = user[1]

  # Validate Expiration
  current_time = datetime.now()
  if current_time <= datetime.strptime(user[13], "%Y-%m-%d %H:%M:%S"):

    # Create Refresh Code
    refresh_token = random.randint(10000, 99999)

    # Get expiration date
    current_time = datetime.now()
    current_time = current_time.replace(microsecond=0)
    if user[5] in military_roles:
      expiration_time = current_time + timedelta(hours=2)
    if user[5] in religious_roles:
      expiration_time = current_time + timedelta(hours=24)
    if user[5] in cooking_roles:
      expiration_time = current_time + timedelta(hours=48)

    # Add token to db
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''UPDATE users SET refresh_code = ?, refresh_time = ? WHERE uname = ?''', (refresh_token, expiration_time, username))
    conn.commit()
    conn.close()

    return jsonify({'refresh_token': refresh_token})
  return jsonify({'message': 'Refresh Token Expired'}), 401

@app.route('/access' , methods=['GET'])
def access():

  refresh_code = request.json

  # Get user for refresh_code
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute('''SELECT * FROM users WHERE refresh_code = ?''', (refresh_code,))
  user = c.fetchone()
  conn.commit()
  conn.close()

  if not user:
    return jsonify({'message': 'No user found'}), 401

  # Validate Expiration
  current_time = datetime.now()
  if current_time <= datetime.strptime(user[12], "%Y-%m-%d %H:%M:%S"):
    # Replace with private key of idp server
    secret_key = "secret_key"

    # Get expiration date
    current_time = datetime.now()
    current_time = current_time.replace(microsecond=0)
    expiration_time = current_time + timedelta(seconds=10)
    payload = {
      "exp": expiration_time,
      "user_id": user[0],
      "username": user[1],
      "clearance": role_to_clearance[user[5]]
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return jsonify({'access_token': token})

  return jsonify({'message': 'Refresh Token Expired'}), 401

def generate_email_otp():
    
    uname = session.get('username')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT email FROM users WHERE uname = ?''', (uname,))
    email = c.fetchone()[0]
    conn.commit()
    conn.close()

    #generate code
    verification_code = str(random.randint(100000, 999999))
    
    #send code to mfa webpage 
    response = requests.post(f'http://mfa:8001/email/{email}', json={'verification_code': verification_code})
    
    #store code for corresponding email
    session[email] = verification_code
    return jsonify({'code_sent': 1})

@app.route('/verify_email_code' , methods=['GET', 'POST'])
def verify_email_code():
  if request.method == 'POST':
    code = request.form['code']
    username = session.get('username')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT email FROM users WHERE uname = ?''', (username,))
    email = c.fetchone()[0]
    conn.commit()
    conn.close()

    # Get code stored on session
    sent_code = session.get(email)
    del session[email]

    if code != sent_code:
      return redirect(url_for('login'))
    
    if(session.get('mfa') > 2):
      generate_sms_otp()
      return redirect(url_for('verify_sms_code'))
    
    user_passed_authentication()

    if session.get('changing_password'):
      return redirect(url_for('change_pass'))
    
    user_role = session.get('user_role')
    if user_role in military_roles:
      return redirect(f'http://localhost:8010/login?uname={username}&location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')
    elif user_role in religious_roles:
      return redirect(f'http://localhost:8011/login?uname={username}&location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')
    elif user_role in cooking_roles:
      return redirect(f'http://localhost:8012/login?uname={username}&location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')
  
  return render_template('email_otp.html')

def generate_sms_otp():
    uname = session.get('username')
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT phone FROM users WHERE uname = ?''', (uname,))
    phone_number = c.fetchone()[0]
    conn.commit()
    conn.close()

    # Generate code
    verification_code = str(random.randint(100000, 999999))
    
    # Sendo code to mfa webpage
    response = requests.post(f'http://mfa:8001/phone/{phone_number}', json={'verification_code': verification_code})
    
    #store code on session
    session[phone_number] = verification_code
    return jsonify({'code_sent': 1})

@app.route('/verify_sms_code' , methods=['GET', 'POST'])
def verify_sms_code():
  if request.method == 'POST':
    code = request.form['code']
    username = session.get('username')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT phone FROM users WHERE uname = ?''', (username,))
    phone = c.fetchone()[0]
    conn.commit()
    conn.close()

    # Get code from session
    sent_code = session.get(phone)
    del session[phone]

    if code != sent_code:
      return redirect(url_for('login'))

    if(session.get('mfa') > 3):
      generate_totp()
      return redirect(url_for('verify_totp'))
    
    user_passed_authentication()

    if session.get('changing_password'):
      return redirect(url_for('change_pass'))
    
    user_role = session.get('user_role')
    if user_role in military_roles:
      return redirect(f'http://localhost:8010/login?uname={username}&location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')
    elif user_role in religious_roles:
      return redirect(f'http://localhost:8011/login?uname={username}&location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')
    elif user_role in cooking_roles:
      return redirect(f'http://localhost:8012/login?uname={username}&location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')
    
  return render_template('sms_otp.html')

def generate_totp():
    uname = session.get('username')

    # send post so code is generated 
    response = requests.post(f'http://mfa:8001/user/{uname}')
    return jsonify({'code_sent': 1})

@app.route('/verify_totp' , methods=['GET', 'POST'])
def verify_totp():
  if request.method == 'POST':
    code = request.form['code']
    username = session.get('username')

    #Validate code base on secret key
    totp = pyotp.TOTP(username)
    valid = totp.verify(code)

    if not valid:
      return redirect(f'http://localhost:8080/login?location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')
    
    user_passed_authentication()

    if session.get('changing_password'):
      return redirect(url_for('change_pass'))
    
    user_role = session.get('user_role')
    if user_role in military_roles:
      return redirect(f'http://localhost:8010/login?uname={username}&location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')
    elif user_role in religious_roles:
      return redirect(f'http://localhost:8011/login?uname={username}&location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')
    elif user_role in cooking_roles:
      return redirect(f'http://localhost:8012/login?uname={username}&location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')
    
  return render_template('totp_verify.html')


def user_passed_authentication():

  username = session.get('username')
  user_session = session.get('current_user_session')

  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute('''SELECT * FROM users WHERE uname = ?''', (username,))
  user = c.fetchone()
  conn.commit()
  conn.close()

  # Delete Session
  sessions = json.loads(user[6])
  del sessions[user_session]

  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  sessions_string = json.dumps(sessions)
  c.execute('''UPDATE users SET points = ? WHERE uname = ?''', (sessions_string, username))
  conn.commit()
  conn.close()

  location_whitelist = user[7] + "," + session.get('location')
  ip_whitelist = user[8] + "," + session.get('ip_address')
  device_whitelist = user[9] + "," + session.get('device')

  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute('''UPDATE users SET location_whitelist = ?, ip_whitelist = ?,  device_whitelist = ? WHERE uname = ?''', (location_whitelist, ip_whitelist, device_whitelist, username))
  conn.commit()
  conn.close()
  

def brute_force_attempt():

  username = session.get('username')
  user_session = session.get('current_user_session')
  ip = session.get('ip_address')

  # Password Spraying attempt
  # Add ip 
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute('''SELECT * FROM bruteforce WHERE ip = ?''', (ip,))
  ip_bruteforce_data = c.fetchone()
  conn.commit()
  conn.close()
  
  if ip_bruteforce_data:
    bruteforce_attempts = json.loads(ip_bruteforce_data[2])

  current_time = datetime.now().replace(microsecond=0).isoformat()
  # ip not in table
  if not ip_bruteforce_data:
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Get day of attempt
    failed_tries = {'1': current_time}
    c.execute('''INSERT INTO bruteforce (ip, failed_tries) VALUES (?,?)''', (ip,json.dumps(failed_tries)))
    conn.commit()
    conn.close()
  # Max of 10 failed tries
  elif len(bruteforce_attempts) +1 <= 10:
    new_tries = len(bruteforce_attempts) +1
    bruteforce_attempts[new_tries] = current_time
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''UPDATE bruteforce SET failed_tries = ? WHERE ip = ?''', (json.dumps(bruteforce_attempts),ip,))
    conn.commit()
    conn.close()
  else:
    # Remove the oldest attempt and add the new one
    sorted_keys = sorted(bruteforce_attempts.keys(), key=lambda k: bruteforce_attempts[k])
    oldest_key = sorted_keys[0]
    del bruteforce_attempts[oldest_key]
    bruteforce_attempts[oldest_key] = current_time

  
  # Add 20 Points after brute force
  # Get session
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute('''SELECT * FROM users WHERE uname = ?''', (username,))
  user = c.fetchone()
  conn.commit()
  conn.close()
  
  # Add points to session
  sessions = json.loads(user[6])
  sessions[user_session] += 20

  # update session
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  sessions_string = json.dumps(sessions)
  c.execute('''UPDATE users SET points = ? WHERE uname = ?''', (sessions_string, username))
  conn.commit()
  conn.close()

def get_password_spraying_points():

  ip = session.get('ip_address')

  # Add ip 
  conn = sqlite3.connect('users.db')
  c = conn.cursor()
  c.execute('''SELECT * FROM bruteforce WHERE ip = ?''', (ip,))
  ip_bruteforce_data = c.fetchone()
  conn.commit()
  conn.close()

  # ip in table
  if ip_bruteforce_data:
    
    bruteforce_attempts = json.loads(ip_bruteforce_data[2])
    
    # Create 2 weeks old time
    current_date = datetime.now().replace(microsecond=0)
    two_weeks_ago = current_date - timedelta(weeks=2)

    # Collect keys to remove
    keys_to_remove = []

    for key, date_str in bruteforce_attempts.items():
        
        # convert to datetime object
        date_obj = datetime.fromisoformat(date_str)
        
        # Check if the date is at least two weeks before the current date
        if date_obj < two_weeks_ago:
            keys_to_remove.append(key)
    
    # Remove keys that are not at least two weeks old
    for key in keys_to_remove:
        del bruteforce_attempts[key]
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''UPDATE bruteforce SET failed_tries = ? WHERE ip = ?''', (json.dumps(bruteforce_attempts),ip,))
        conn.commit()
        conn.close()

    return int(len(bruteforce_attempts)) * 10
  
  return 0

#Only used to validate ip format
def validate_ip_address(ip):

    # Define the regex for a valid IPv4 address
    ip_pattern = re.compile(r'^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})$')

    # Validate the IP address
    if ip_pattern.match(ip):
        return True
    else:
        return False

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080)

