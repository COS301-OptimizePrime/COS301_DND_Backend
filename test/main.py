from __future__ import print_function

import grpc

import server_pb2
import server_pb2_grpc

import unittest
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

import subprocess

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
        response = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=7))

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
        self.assertLessEqual(len(response.sessions), 3)

    def test_rpc_good_login_leave_if_not_in_session(self):
        auth.revoke_refresh_tokens(self.uid)
        
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
    
        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)

        response = stub.Leave(server_pb2.LeaveRequest(auth_id_token=token, session_id=self.__class__.test_session_id))

        self.assertEqual(response.status, 'FAILED')
        self.assertEqual(response.status_message, '[Leave] User is not in the session!')

    def test_join_rpc_good_login_existing_session(self):
        auth.revoke_refresh_tokens(self.uid)
        
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=self.__class__.test_session_id))

        self.assertEqual(response.name, 'mysession')
        self.assertEqual(len(response.session_id), 36)
        self.assertEqual(response.status, 'SUCCESS')

    def test_leave_rpc_good_login_leave_session(self):
        auth.revoke_refresh_tokens(self.uid)
        
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)

        response = stub.Leave(server_pb2.LeaveRequest(auth_id_token=token, session_id=self.__class__.test_session_id))

        self.assertEqual(response.status, 'SUCCESS')

    def test_leave_rpc_good_login_leave_session_multiple_already_joined(self):
        auth.revoke_refresh_tokens(self.uid)
        
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)

        # Add new session in case none exist.
        session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2))
        response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

        self.assertEqual(response.status, 'SUCCESS')
        self.assertEqual(len(response.users), 1)
        self.assertEqual(response.users[0].name, 'mockuser@test.co.za')

        # Second player join
        token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
        response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

        self.assertEqual(response.status, 'SUCCESS')
        self.assertEqual(len(response.users), 2)
        self.assertEqual(response.users[0].name, 'mockuser@test.co.za')
        self.assertEqual(response.users[1].name, 'mockuser2@test.co.za')

        # Second player leaves
        token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
        response = stub.Leave(server_pb2.LeaveRequest(auth_id_token=token, session_id=session.session_id))

        self.assertEqual(response.status, 'SUCCESS')

        # get session
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
        response = stub.GetSessionById(server_pb2.GetSessionRequest(auth_id_token=token, session_id=session.session_id))
        self.assertEqual(response.status, 'SUCCESS')
        self.assertEqual(len(response.users), 1)
        self.assertEqual(response.users[0].name, 'mockuser@test.co.za')

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

    def test_setmax_rpc_good_login_setmax_session(self):
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
        self.assertEqual(response.full, True)

    def test_rpc_good_login_get_session_by_id(self):
        auth.revoke_refresh_tokens(self.uid)
        
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)

        response = stub.GetSessionById(server_pb2.GetSessionRequest(auth_id_token=token, session_id=self.__class__.test_session_id))

        self.assertEqual(response.name, 'mysession')
        self.assertEqual(response.session_id, self.__class__.test_session_id)
        self.assertEqual(response.status, 'SUCCESS')

    def test_setmax_rpc_good_login_setmax_session_invalid_user(self):
        auth.revoke_refresh_tokens(self.uid)
        
        token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)

        response = stub.SetMax(server_pb2.SetMaxPlayersRequest(auth_id_token=token, session_id=self.__class__.test_session_id, number=0))

        self.assertEqual(response.name, 'NULL')
        self.assertEqual(response.status_message, '[SetMax] You must be the dungeon master to use this command!')
        self.assertEqual(response.status, 'FAILED')

    def test_list_rpc_good_login_list_sessions_that_are_full(self):
        auth.revoke_refresh_tokens(self.uid)

        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        # Add new session in case none exist.
        stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=0))
        response = stub.List(server_pb2.ListRequest(auth_id_token=token, limit=3, full=True))

        self.assertEqual(response.status, 'SUCCESS')
        self.assertEqual(response.sessions[0].full, True)
        self.assertLessEqual(len(response.sessions), 3)

    def test_kick_good_login(self):
        auth.revoke_refresh_tokens(self.uid)

        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        # Add new session in case none exist.
        session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2))
        response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

        self.assertEqual(response.status, 'SUCCESS')
        self.assertEqual(len(response.users), 1)
        self.assertEqual(response.users[0].name, 'mockuser@test.co.za')

        # Second player join
        token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
        response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

        self.assertEqual(response.status, 'SUCCESS')
        self.assertEqual(len(response.users), 2)
        self.assertEqual(response.users[0].name, 'mockuser@test.co.za')
        self.assertEqual(response.users[1].name, 'mockuser2@test.co.za')

        user2 = response.users[1]

        # kick player 2
        # login as DM
        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
        response = stub.Kick(server_pb2.KickPlayerRequest(auth_id_token=token, session_id=session.session_id, user=user2))

        # check if user still in session
        self.assertEqual(response.status, 'SUCCESS')
        self.assertEqual(len(response.users), 1)
        self.assertEqual(response.users[0].name, 'mockuser@test.co.za')

    def test_kick_unauthorised_good_login(self):
        auth.revoke_refresh_tokens(self.uid)

        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        # Add new session in case none exist.
        session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2))
        response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

        self.assertEqual(response.status, 'SUCCESS')
        self.assertEqual(len(response.users), 1)
        self.assertEqual(response.users[0].name, 'mockuser@test.co.za')

        # Second player join
        token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
        response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

        self.assertEqual(response.status, 'SUCCESS')
        self.assertEqual(len(response.users), 2)
        self.assertEqual(response.users[0].name, 'mockuser@test.co.za')
        self.assertEqual(response.users[1].name, 'mockuser2@test.co.za')

        user2 = response.users[1]

        # kick player 2
        # login as player 2
        token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
        response = stub.Kick(server_pb2.KickPlayerRequest(auth_id_token=token, session_id=session.session_id, user=user2))

        # should fail
        self.assertEqual(response.status, 'FAILED')
        self.assertEqual(response.status_message, '[Kick] You must be the dungeon master to use this command!')

    def test_private_session_should_not_be_listed(self):
        auth.revoke_refresh_tokens(self.uid)

        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        # Add new session in case none exist.
        session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=True))
        # should be first result, if something is wrong
        response = stub.List(server_pb2.ListRequest(auth_id_token=token, limit=1))

        self.assertNotEqual(response.sessions[0].session_id, session.session_id)

    def test_non_private_session_should_be_listed(self):
        auth.revoke_refresh_tokens(self.uid)

        token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

        channel = grpc.insecure_channel('localhost:50051')
        stub = server_pb2_grpc.SessionsManagerStub(channel)
        # Add new session in case none exist.
        session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=False))
        # should be first result
        response = stub.List(server_pb2.ListRequest(auth_id_token=token, limit=1))

        self.assertEqual(response.sessions[0].session_id, session.session_id)

if __name__ == '__main__':
    unittest.main()