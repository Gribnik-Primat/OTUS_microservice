import unittest
import json
from auth import app


class AuthServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.battle_id = 'test_battle'
        self.participants = ['user1', 'user2']

    def test_create_battle(self):
        data = {'participants': self.participants}
        response = self.app.post('/create_battle', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('battle_id', data)

    def test_get_token(self):
        data = {'participants': self.participants}
        response = self.app.post('/create_battle', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIn('battle_id', result)
        data = {'user_id': 'user1', 'battle_id': result['battle_id']}
        response = self.app.post('/get_token', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)

    def test_get_token_invalid_user(self):
        data = {'user_id': 'invalid_user', 'battle_id': self.battle_id}
        response = self.app.post('/get_token', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertIn('message', data)


if __name__ == '__main__':
    unittest.main()
