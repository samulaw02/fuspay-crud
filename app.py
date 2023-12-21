import os
import json
import bcrypt
from flask import Flask, request, url_for, Response
from flask_jwt_extended import create_access_token, JWTManager
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from config import StagingConfig, ProductionConfig
from model import db, User
from auth_middleware import token_required
from schema import CreateUserSchema, LoginSchema, UpdateUserSchema


load_dotenv()

app = Flask(__name__)

# Load environment-specific configurations
env = os.getenv('FLASK_ENV', 'staging')
if env == 'staging':
    app.config.from_object(StagingConfig)
else:
    app.config.from_object(ProductionConfig)
    
# Connect the database to the app instance
db.init_app(app)

# Create tables if they don't exist
with app.app_context():
    db.create_all()
    
# Setup jwt
jwt = JWTManager(app)
    
    
#login
@app.route('/users/login', methods=['POST'])
def login():
    login_schema = LoginSchema()
    try:
        data = login_schema.load(request.json)
        # Find user by email
        user = User.query.filter_by(email=data['email']).first()
        if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            # Invalid credentials
            response = {'status': False, 'message': 'Invalid email or password'}
            return Response(json.dumps(response), status=401, mimetype='application/json')
        # Generate access token if credentials are correct
        access_token = create_access_token(identity=user.id)  # Assuming user.id is unique
        response = {'status': True, 'message': 'Login successful', 'access_token': access_token}
        return Response(json.dumps(response), status=200, mimetype='application/json')
    except Exception as e:
        response = {'status': False,'message': f'error login user: {str(e)}'}
        return Response(json.dumps(response), status=500, mimetype='application/json')
        
    

# create a user
@app.route('/users', methods=['POST'])
def create_user():
    create_user_schema = CreateUserSchema()
    try:
        data = create_user_schema.load(request.json)
        password = data['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        data['password'] = hashed_password.decode('utf-8')
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        # Return the details of the created user in the response
        response = {
            'status': True,
            'message': 'User created successfully',
            'user': new_user.json()
        }
        return Response(json.dumps(response), status=201, mimetype='application/json')
    except IntegrityError as e:
        response = {'status': False,'message': 'Email already exists'}
        return Response(json.dumps(response), status=409, mimetype='application/json')
    except Exception as e:
        response = {'status': False,'message': f'error creating user: {str(e)}'}
        return Response(json.dumps(response), status=500, mimetype='application/json')

# get all users
@app.route('/users', methods=['GET'])
@token_required
def get_paginated_users(current_user):
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        paginated_users = User.query.order_by(desc(User.createdAt)).paginate(page=page, per_page=per_page)
        if not paginated_users.items:
            response = {'status': False, 'message': 'No users found', 'users': []}
            return Response(json.dumps(response), status=200, mimetype='application/json')
        users = [user.json() for user in paginated_users.items]
        base_url = request.base_url
        full_next_page = f"{base_url}?page={paginated_users.next_num}&per_page={per_page}" if paginated_users.has_next else None
        full_prev_page = f"{base_url}?page={paginated_users.prev_num}&per_page={per_page}" if paginated_users.has_prev else None
        response = {
            'status': True,
            'message': 'Users retrieved successfully',
            'users': users,
            'page': page,
            'per_page': per_page,
            'next_page': full_next_page,
            'prev_page': full_prev_page
        }
        return Response(json.dumps(response), status=200, mimetype='application/json')
    except Exception as e:
        response = {'status': False,'message': f'Error getting users: {str(e)}'}
        return Response(json.dumps(response), status=500, mimetype='application/json')

# get a user by id
@app.route('/users/<int:id>', methods=['GET'])
@token_required
def get_user(current_user, id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            response = {'status': True,'message': 'User fecthed successfully','user': user.json()}
            return Response(json.dumps(response), status=200, mimetype='application/json')
        response = {'status': False,'message': 'User not found'}
        return Response(json.dumps(response), status=404, mimetype='application/json')
    except Exception as e:
        response = {'status': False,'message': f'Error getting user: {str(e)}'}
        return Response(json.dumps(response), status=500, mimetype='application/json')
        

# update a user
@app.route('/users/<int:id>', methods=['PUT'])
@token_required
def update_user(current_user, id):
    update_user_schema = UpdateUserSchema()
    try:
        data = update_user_schema.load(request.json)
        user = User.query.filter_by(id=id).first()
        if user:
            # Update all provided fields except for the password
            for key, value in data.items():
                if key not in ['password', 'email']:
                    setattr(user, key, value)
            db.session.commit()
            # Return the updated user details in the response
            response = {
                'status': True,
                'message': 'User updated successfully',
                'user': user.json()
            }
            return Response(json.dumps(response), status=200, mimetype='application/json')
        response = {'status': False,'message': 'user not found'}
        return Response(json.dumps(response), status=404, mimetype='application/json')
    except IntegrityError as e:
        response = {'status': False,'message': 'Email already exists'}
        return Response(json.dumps(response), status=409, mimetype='application/json')
    except Exception as e:
        response = {'status': False,'message': f'error updating user: {str(e)}'}
        return Response(json.dumps(response), status=500, mimetype='application/json')

# delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            response = {'status': True,'message': 'user deleted successfully'}
            return Response(json.dumps(response), status=200, mimetype='application/json')
        response = {'status': False,'message': 'user not found'}
        return Response(json.dumps(response), status=404, mimetype='application/json')
    except Exception as e:
        response = {'status': False,'message': f'error deleting user: {str(e)}'}
        return Response(json.dumps(response), status=500, mimetype='application/json')