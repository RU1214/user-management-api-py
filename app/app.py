from flask import Flask, jsonify, request
from models import User
import os, db, re, datetime
app = Flask(__name__)

@app.route('/')
def root():
    return 'Welcome to User Management API developed in Python'

@app.route('/about')
def about():
    return jsonify({
            'name': 'User Management API',
            'developer': 'Naseem Sultana',
            'organisation': 'National College of Ireland',
            'academic-year': '2023-2024',
            'libraries': {
                'webframework': 'Flask v2.2.3',
                'scripting': 'Python v3.11',
                'database': 'SQLLite3'
            }
        })

@app.route('/version')
def version():
    return jsonify({
            'api': '1.0.0',
            'components': {
                'documentation': '1.0.0'
            }
        })

if __name__ == '__main__':
    app.run()

if not os.path.isfile('users.db'):
    db.connect()

def isValid(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, email):
      return True
    else:
      return False

# Create Request
@app.route("/request", methods=['POST'])
def postRequest():
    req_data = request.get_json()
    email = req_data['email']
    if not isValid(email):
        return jsonify({
            'status': '422',
            'res': 'failure',
            'error': 'Invalid email format. Please enter a valid email address'
        })
    username = req_data['username']
    users = [u.serialize() for u in db.view()]
    for u in users:
        if u['username'] == username:
            return jsonify({
                # 'error': '',
                'res': f'Error! User with username {username} is already in database!',
                'status': '404'
            })

    user = User(db.getNewId(), True, username, datetime.datetime.now())
    print('new user: ', user.serialize())
    db.insert(user)
    new_users = [u.serialize() for u in db.view()]
    print('users in lib: ', new_users)
    
    return jsonify({
                # 'error': '',
                'res': user.serialize(),
                'status': '200',
                'msg': 'Success creating a new user!'
            })

# Get All Users
@app.route('/request', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    users = [u.serialize() for u in db.view()]
    if (content_type == 'application/json'):
        json = request.json
        for u in users:
            if u['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': u,
                    'status': '200',
                    'msg': 'Success getting all users in database!'
                })
        return jsonify({
            'error': f"Error! User with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': users,
                    'status': '200',
                    'msg': 'Success getting all users in database!',
                    'no_of_users': len(users)
                })

#Get one user by Id
@app.route('/request/<id>', methods=['GET'])
def getRequestId(id):
    req_args = request.view_args
    # print('req_args: ', req_args)
    users = [u.serialize() for u in db.view()]
    if req_args:
        for u in users:
            if u['id'] == int(req_args['id']):
                return jsonify({
                    # 'error': '',
                    'res': u,
                    'status': '200',
                    'msg': 'Success getting user by ID!'
                })
        return jsonify({
            'error': f"Error! User with id '{req_args['id']}' was not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': users,
                    'status': '200',
                    'msg': 'Success getting user by ID!',
                    'no_of_users': len(users)
                })
# Update a User
@app.route("/request", methods=['PUT'])
def putRequest():
    req_data = request.get_json()
    availability = req_data['active']
    username = req_data['username']
    the_id = req_data['id']
    users = [u.serialize() for u in db.view()]
    for u in users:
        if u['id'] == the_id:
            user = User(
                the_id, 
                availability, 
                username, 
                datetime.datetime.now()
            )
            print('new user: ', user.serialize())
            db.update(user)
            new_users = [u.serialize() for u in db.view()]
            print('users in lib: ', new_users)
            return jsonify({
                # 'error': '',
                'res': user.serialize(),
                'status': '200',
                'msg': f'Success updating the user titled {username}!'
            })        
    return jsonify({
                # 'error': '',
                'res': f'Error! Failed to update User with username: {username}!',
                'status': '404'
            })

@app.route('/request/<id>', methods=['DELETE'])
def deleteRequest(id):
    req_args = request.view_args
    users = [u.serialize() for u in db.view()]
    print('req_args', req_args)
    if req_args:        
        for u in users:
            if u['id'] == int(req_args['id']):
                db.delete(u['id'])
                updated_users = [u.serialize() for u in db.view()]
                print('updated_users: ', updated_users)
                return jsonify({
                    'res': updated_users,
                    'status': '200',
                    'msg': 'Success deleting user by ID!',
                    'no_of_users': len(updated_users)
                })            
        return jsonify({
            'error': f"Error! User with id '{req_args['id']}' was not found!",
            'res': '',
            'status': '404'
        })