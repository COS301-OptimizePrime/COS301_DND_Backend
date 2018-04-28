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

#import database.db as db
#conn = db.connect()

class TestSessionManager(unittest.TestCase):
    test_session_id = ''

    def setUp(self):
        self.uid = 'mT8HzwXWjDc1FX472qTfcsUUcQt1'

    def test_create_rpc_good_login(self):
        auth.revoke_refresh_tokens(self.uid)
        
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        response = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token))

        self.__class__.test_session_id = response.session_id

        self.assertEqual(response.name, 'mysession')
        self.assertEqual(len(response.session_id), 36)
        self.assertEqual(response.status, 'SUCCESS')

    def test_create_rpc_bad_login(self):
        auth.revoke_refresh_tokens(self.uid)

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        response = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token='invalidtoken'))
        self.assertEqual(response.name, 'NULL')
        self.assertEqual(response.session_id, 'NULL')
        self.assertEqual(response.status, 'FAILED')

    def test_list_rpc_good_login(self):
        auth.revoke_refresh_tokens(self.uid)

        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        response = stub.List(server_pb2.ListRequest(auth_id_token=token, limit=3))

        self.assertEqual(response.status, 'SUCCESS')

    def test_join_rpc_good_login_existing_session(self):
        auth.revoke_refresh_tokens(self.uid)
        
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=self.__class__.test_session_id))

        self.assertEqual(response.name, 'mysession')
        self.assertEqual(len(response.session_id), 36)
        self.assertEqual(response.status, 'SUCCESS')

    def test_join_rpc_good_login_leave_session(self):
        auth.revoke_refresh_tokens(self.uid)
        
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)

        response = stub.Leave(server_pb2.LeaveRequest(auth_id_token=token, session_id=self.__class__.test_session_id))

        self.assertEqual(response.status, 'SUCCESS')

    def test_join_rpc_good_login_nonexisting_session(self):
        auth.revoke_refresh_tokens(self.uid)
        
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id='invalid_id'))

        self.assertEqual(response.name, 'NULL')
        self.assertEqual(response.session_id, 'NULL')
        self.assertEqual(response.status, 'FAILED')
        self.assertEqual(response.status_message, '[JOIN] No session with that ID exists!')

    def test_join_rpc_good_login_setmax_session(self):
        auth.revoke_refresh_tokens(self.uid)
        
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)

        
        response = stub.SetMax(server_pb2.SetMaxPlayersRequest(auth_id_token=token, session_id=self.__class__.test_session_id, number=0))

        self.assertEqual(response.name, 'mysession')
        self.assertEqual(len(response.session_id), 36)
        self.assertEqual(response.status, 'SUCCESS')
        self.assertEqual(response.max_players, 0)

    def test_join_rpc_good_login_full_session(self):
        auth.revoke_refresh_tokens(self.uid)
        
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)

        stub.SetMax(server_pb2.SetMaxPlayersRequest(auth_id_token=token, session_id=self.__class__.test_session_id, number=0))
        response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=self.__class__.test_session_id))

        self.assertEqual(response.name, 'NULL')
        self.assertEqual(response.session_id, 'NULL')
        self.assertEqual(response.status, 'FAILED')
        self.assertEqual(response.status_message, '[JOIN] This session is full!')

if __name__ == '__main__':
    unittest.main()