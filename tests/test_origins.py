import json
import unittest

import requests

from app import app


class TestOrigins(unittest.TestCase):
    def setUp(self):
        r = requests.post(app.config.get('OAUTH2_TOKEN_URI'), {
            'grant_type': 'password',
            'client_id': 'server',
            'username': app.config.get('OAUTH2_USERNAME'),
            'password': app.config.get('OAUTH2_PASSWORD')
        })
        self.assertEqual(r.status_code, 200)
        j = r.json()
        self.headers = {
            'Authorization': 'Bearer ' + j.get('access_token'),
            'Content-Type': 'application/json'
        }
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_rest(self):
        r = self.app.post('/api/v1/origins', data=json.dumps({
            'name': 'Test 1'
        }), follow_redirects=True, headers=self.headers)
        self.assertEqual(r.status_code, 200)
        json_response = json.loads(r.get_data(as_text=True))
        self.assertIn('uuid', json_response)
        r = self.app.get('/api/v1/origins', follow_redirects=True, headers=self.headers)
        self.assertEqual(r.status_code, 200)
        json_response = json.loads(r.get_data(as_text=True))
        self.assertIn('response', json_response)
        self.assertEqual(len(json_response.get('response')), 1)
        uuid = json_response['response'][0].get('uuid')
        self.assertIsNotNone(uuid)
        r = self.app.get('/api/v1/origins/{uuid}'.format(uuid=uuid),
                         follow_redirects=True, headers=self.headers)
        self.assertEqual(r.status_code, 200)
        json_response = json.loads(r.get_data(as_text=True))
        self.assertEqual('Test 1', json_response['response'].get('name'))
        r = self.app.delete('/api/v1/origins/{uuid}'.format(uuid=uuid),
                            follow_redirects=True, headers=self.headers)
        self.assertEqual(r.status_code, 200)
