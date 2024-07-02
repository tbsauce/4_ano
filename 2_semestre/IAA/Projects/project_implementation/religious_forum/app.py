from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

posts = []

@app.route('/', methods=['GET', 'POST'])
def index():

  if request.method == 'POST':
    session['device'] = request.form.get('device')
    session['location'] = request.form.get('location')
    session['ip_address'] = request.form.get('ip')
    if "create" in request.form:
      return redirect(url_for('create'))
    elif "change" in request.form:
      return redirect(url_for('change_pass'))

  access_token = session.get('access_token')
  
  
  if access_token == None:
    return redirect('http://localhost:8080/login')
  
  # Get Posts with access token
  headers = {'Authorization': f'{access_token}'}
  response = requests.get('http://religious_resource_server:8021/get_all_posts', headers=headers)
  
  if response.status_code == 200:
    posts = response.json().get('posts')
  elif response.status_code == 403:
    # if access token is invalid if not it creates new one
    if get_access_token():
      return redirect(url_for('index')) 
    else: 
      # Expiration of refresh token is invalid aumentar o refresh token
      #Get new user points 
      if 'device' in session or 'username' in session or 'location' in session or 'ip_address' in session:
        json={
                'device': session.get('device'),
                'location': session.get('location'),
                'ip': session.get('ip_address'),
                'username': session.get('username')
            }
        response = requests.get('http://idp:8080/recalculate_points', json=json)
        response_data = response.json()
        if response_data.get('message') > 0:
          return redirect(f'http://localhost:8080/login?location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')
      else:
        return redirect('http://localhost:8080/login')

      # Get new refresh token
      uname = session.get('username')
      response, status = get_tokens(uname)

      if status == 401:
        return redirect('http://localhost:8080/login')
        
      return redirect(url_for('index'))
  else:
    return redirect('http://localhost:8080/login')
    
  return render_template('index.html', posts=posts, default_device=session.get('device'), default_location=session.get('location'), default_ip=session.get('ip_address'))

@app.route('/login', methods=['GET', 'POST'])
def login():

  # If redirected from idp
  
  if request.referrer == "http://localhost:8080/":
    uname = request.args.get('uname')
    session['device'] = request.args.get('device')
    session['location'] = request.args.get('location')
    session['ip_address'] = request.args.get('ip_address')
    session['username'] = uname

    # Get Tokens - authorization, refresh, access
    response, status = get_tokens(uname)

    if status == 401:
      return redirect('http://localhost:8080/login')
      
    return redirect(url_for('index'))
  return redirect('http://localhost:8080/login')

@app.route('/change_pass', methods=['GET', 'POST'])
def change_pass():
  return redirect(f'http://localhost:8080/change_pass?location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')

def get_tokens(username):

  #Get authorization token
  response = requests.get('http://idp:8080/authorization', json=username)
  
  if response.status_code != 200:
    return jsonify({'message': 'Authorization code error'}), 401

  response_data = response.json()
  auth_token = response_data.get('auth_code')

  #Get refresh token
  response = requests.get('http://idp:8080/refresh', json=auth_token)

  if response.status_code == 401:
    return response_data.get('message'), 401
  
  response_data = response.json()
  refresh_token = response_data.get('refresh_token')
  session['refresh_token'] = refresh_token

  #Get access token
  get_access_token() 

  return jsonify({'message': 'Valid User'}), 200

def get_access_token():
  refresh_token = session.get('refresh_token')
  
  if refresh_token == None:
    return jsonify({'message': 'No Refresh Token Found'}), 401
  
  #Get access token
  response = requests.get('http://idp:8080/access', json=refresh_token)
  response_data = response.json()

  # Refresh token has expired
  if response.status_code == 401:
    return False
  
  access_token = response_data.get('access_token')
  session['access_token'] = access_token
  return True


@app.route('/create', methods=['GET', 'POST'])
def create():
  if request.method == 'POST':
    title = request.form['title']
    content = request.form['content']
    superior = 'superior' in request.form
    
    session['device'] = request.form['device']
    session['location'] = request.form['location']
    session['ip_address'] = request.form['ip']

    data = {
      'post': content,
      'title': title, 
      'superior': superior, 
    }

    access_token = session.get('access_token')
    if access_token == None:
      # No access Token Found
      return redirect('http://localhost:8080/login')
    
    headers = {'Authorization': f'{access_token}'}
    response = requests.post('http://religious_resource_server:8021/create_post', json=data, headers=headers)
    
    if response.status_code == 200:
      # Post creation successful
      return redirect(url_for('index'))
    elif response.status_code == 403:
      # if access token is invalid
      if get_access_token():
        access_token = session.get('access_token')
        headers = {'Authorization': f'{access_token}'}
        response = requests.post('http://religious_resource_server:8021/create_post', json=data, headers=headers)
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
          return redirect(url_for('login'))
      else:
        # Expiration of refresh token is invalid

        #Get new user points 
        if 'device' in session or 'username' in session or 'location' in session or 'ip_address' in session:
          json={
                  'device': session.get('device'),
                  'location': session.get('location'),
                  'ip': session.get('ip_address'),
                  'username': session.get('username')
              }
          response = requests.get('http://idp:8080/recalculate_points', json=json)
          response_data = response.json()
          if response_data.get('message') > 0:
            return redirect(f'http://localhost:8080/login?location={session.get("location")}&ip_address={session.get("ip_address")}&device={session.get("device")}')
        else:
          return redirect('http://localhost:8080/login')

        # Get new refresh token
        uname = session.get('username')
        response, status = get_tokens(uname)

        if status == 401:
          return redirect('http://localhost:8080/login')
        
        # Create the post again
        access_token = session.get('access_token')
        headers = {'Authorization': f'{access_token}'}
        response = requests.post('http://religious_resource_server:8021/create_post', json=data, headers=headers)
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
          return redirect(url_for('login'))
    else:
      return redirect('http://localhost:8080/login')
      
  return render_template('create.html', default_device=session.get('device'), default_location=session.get('location'), default_ip=session.get('ip_address'))

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8011)

