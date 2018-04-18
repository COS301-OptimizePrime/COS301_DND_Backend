from __future__ import print_function

import grpc

import server_pb2
import server_pb2_grpc

import unittest
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

import subprocess

# Mock user mT8HzwXWjDc1FX472qTfcsUUcQt1
cred = credentials.Certificate("dnd-game-manager-firebase-adminsdk-34ek4-cccabd3dd6.json")
firebase = firebase_admin.initialize_app(cred)

class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self.uid = 'mT8HzwXWjDc1FX472qTfcsUUcQt1'

    def test_create_rpc_good_login(self):
        auth.revoke_refresh_tokens(self.uid)

        stdoutdata = subprocess.getoutput("node login.mjs")
        token = str(stdoutdata.split()[0])

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        response = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token))

        self.assertEqual(response.name, 'mysession')
        self.assertEqual(len(response.session_id), 36)

    def test_create_rpc_bad_login(self):
        auth.revoke_refresh_tokens(self.uid)

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        response = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token='invalidtoken'))
        self.assertEqual(response.name, 'NULL')
        self.assertEqual(response.session_id, 'NULL')
        self.assertEqual(response.status, 'FAILED')


if __name__ == '__main__':
    unittest.main()