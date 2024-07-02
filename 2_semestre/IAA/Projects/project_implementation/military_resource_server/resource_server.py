from flask import Flask, request, jsonify
import sqlite3
import jwt
import time
from datetime import datetime, timedelta

app = Flask(__name__)

conn = sqlite3.connect('posts.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS posts (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               uname TEXT NOT NULL,
               post TEXT NOT NULL,
               title TEXT NOT NULL,
               clearance TEXT NOT NULL
             )''')
conn.commit()
conn.close()

clearance_levels = ["Unclassified", "Restricted", "Confidential", "Top-Secret"]

@app.route('/verify', methods=['POST'])
def verify_token():
  # Should be the public key of the idp
  secret_key = "secret_key"
  access_token = request.headers.get('Authorization')
  try:
      payload = jwt.decode(access_token, secret_key, algorithms=['HS256'])
      # Check expiration time against current time
      current_time = datetime.now()
      if current_time >= datetime.utcfromtimestamp(payload['exp']):
        #raise error if expired
        raise jwt.ExpiredSignatureError
      return payload, 200
  except jwt.ExpiredSignatureError:
      return jsonify({'message': 'Expired access token'}), 403
  except jwt.InvalidTokenError:
      return jsonify({'message': 'Invalid access token'}), 401
  except Exception as e:
      return jsonify({'message': 'Error on access token'}), 401

# Route to create a post (requires valid access token)
@app.route('/create_post', methods=['POST'])
def create_new_post():

  # Verify access token
  access_token = request.headers.get('Authorization')
  if not access_token:
    return jsonify({'message': 'Missing access token'}), 401
  result, status_code = verify_token()
  if status_code == 403:
    return jsonify({'message': 'Expired access token'}), 403
  if status_code != 200:
    return jsonify({'message': 'Invalid access token'}), 401
  
  # Get values from access token
  clearance = result['clearance']
  if not clearance in clearance_levels:
    return jsonify({'message': 'Clearance not Valid'}), 401
  
  uname = result['username']

  data = request.json
  # add fields to data
  data['uname'] = uname
  data['clearance'] = clearance
  created_post = create_post(data)

  return jsonify(created_post)

def create_post(data):
  
  # write to superiors if true
  if(data['superior'] ):
    current_index = clearance_levels.index(data['clearance'])
    if current_index + 1 < len(clearance_levels):   
      data['clearance'] = clearance_levels[current_index + 1]
      
  conn = sqlite3.connect('posts.db')
  c = conn.cursor()
  c.execute('''INSERT INTO posts (uname, post, title, clearance) VALUES (?, ?, ?, ?)''', (data['uname'], data['post'], data['title'], data['clearance']))
  conn.commit()
  conn.close()
  return {'message': 'Post created successfully'}

# Route to get posts (requires valid access token and optional filters)
@app.route('/get_all_posts', methods=['GET'])
def get_all_posts():

  # Verify access token
  access_token = request.headers.get('Authorization')
  if not access_token:
    return jsonify({'message': 'Missing access token'}), 401
  result, status_code = verify_token()
  
  if status_code == 403:
    return jsonify({'message': 'Expired access token'}), 403
  if status_code != 200:
    return jsonify({'message': 'Invalid access token'}), 401
  
  clearance = result['clearance']
  if not clearance in clearance_levels:
    return jsonify({'message': 'Clearance not Valid'}), 401
  
  posts = get_posts(clearance)
  return jsonify({'posts': posts})

def get_posts(clearance):
  conn = sqlite3.connect('posts.db')
  c = conn.cursor()
  # Get clearance of lower levels
  current_index = clearance_levels.index(clearance)
  if current_index != 0:   
    clearance_below = clearance_levels[current_index - 1]
    c.execute("SELECT * FROM posts Where clearance = ? or clearance = ?", (clearance, clearance_below))
  else:
    c.execute("SELECT * FROM posts Where clearance = ?", (clearance,))
  posts = c.fetchall()
  conn.commit()
  conn.close()

  return posts

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8020)
