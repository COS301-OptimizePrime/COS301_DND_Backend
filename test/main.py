from __future__ import print_function

import grpc

import server_pb2
import server_pb2_grpc

import unittest
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

# Mock user cgq5p1Xa0dW4qrVeymdwhbBGNHo1

class TestSessionManager(unittest.TestCase):
    def test_create_rpc(self):
        cred = credentials.Certificate("dnd-game-manager-firebase-adminsdk-34ek4-cccabd3dd6.json")
        firebase = firebase_admin.initialize_app(cred)

        uid = 'cgq5p1Xa0dW4qrVeymdwhbBGNHo1'
        auth.revoke_refresh_tokens(uid)

        custom_token = auth.create_custom_token(uid)
        user = auth.get_user(uid)

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        response = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=custom_token))
        self.assertEqual(response.name, 'mysession')
        self.assertEqual(len(response.session_id), 36)

if __name__ == '__main__':
    unittest.main()