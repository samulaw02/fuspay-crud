import unittest
import json
from app import app
from model import db
from config import StagingConfig


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        # Use the test configuration
        app.config.from_object(StagingConfig)       
        # Initialize/reset the test database
        with app.app_context():
            db.create_all()
                 
         
    def test_create_user(self):
        data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john@example.com",
            "password": "securepassword"
        }
        response = self.app.post('/users', json=data)
        self.assertEqual(response.status_code, 201)

    
    def login(self):
        login_data = {
            "email": "john@example.com",
            "password": "securepassword"
        }
        login_response = self.app.post('/users/login', json=login_data)
        if (login_response.status_code == 200):
            # Extract access token from the login response and set it to self.access_token
            login_response_data = json.loads(login_response.data)
            return login_response_data.get('access_token')
        else:
            return ''
    
    
    def test_get_paginated_users(self):
        access_token = self.login()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.get('/users', headers=headers)
        self.assertEqual(response.status_code, 200)
        

    def test_get_user(self):
        access_token = self.login()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.get('/users/1', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        data = {
            "firstName": "Updated",
            "lastName": "Name"
        }
        access_token = self.login()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.put('/users/1', json=data, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_user_deletion(self):
        access_token = self.login()
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.delete('/users/1', headers=headers)
        self.assertEqual(response.status_code, 200)