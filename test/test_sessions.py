from __future__ import print_function

import grpc

import server_pb2
import server_pb2_grpc

import pytest
import pytest_benchmark

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

import subprocess

cred = credentials.Certificate("dnd-game-manager-firebase-adminsdk-34ek4-cccabd3dd6.json")
firebase = firebase_admin.initialize_app(cred)

server = 'localhost:50051'
#server = 'develop.optimizeprime.co.za:50051'
test_session_id = ''
uid = 'mT8HzwXWjDc1FX472qTfcsUUcQt1'

def _create_rpc_good_login():
    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    response = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=7))
    return response

def test_create_rpc_good_login(benchmark):        
    response = benchmark(_create_rpc_good_login)

    assert(response.name == 'mysession')
    assert(len(response.session_id) == 36)
    assert(response.status == 'SUCCESS')

def test_create_rpc_bad_login():
    auth.revoke_refresh_tokens(uid)

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    response = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token='invalidtoken'))
    assert(response.name == 'NULL')
    assert(response.session_id == 'NULL')
    assert(response.status == 'FAILED')

def test_list_rpc_good_login():
    auth.revoke_refresh_tokens(uid)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    response = stub.List(server_pb2.ListRequest(auth_id_token=token, limit=3))

    assert(response.status == 'SUCCESS')
    assert(len(response.sessions) <= 3)

def test_rpc_good_login_leave_if_not_in_session():
    auth.revoke_refresh_tokens(uid)

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    # Create session
    token = str(subprocess.check_output('node ./login.mjs mockuser@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2))

    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Leave(server_pb2.LeaveRequest(auth_id_token=token, session_id=session.session_id))

    assert(response.status == 'FAILED')
    assert(response.status_message == '[Leave] User is not in the session!')

def test_join_rpc_good_login_existing_session():
    auth.revoke_refresh_tokens(uid)
    
    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = _create_rpc_good_login()

    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

    assert(response.name == 'mysession')
    assert(len(response.session_id) == 36)
    assert(response.status == 'SUCCESS')

def test_leave_rpc_good_login_leave_session_multiple_already_joined():
    auth.revoke_refresh_tokens(uid)
    
    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    # Add new session in case none exist.
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2))
    
    # Third player join
    token = str(subprocess.check_output('node ./login.mjs mockuser3@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

    assert(response.status == 'SUCCESS')
    assert(len(response.users) == 1)
    assert(response.users[0].name == 'mockuser3@test.co.za')

    # Second player join
    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

    assert(response.status == 'SUCCESS')
    assert(len(response.users) == 2)
    assert(response.users[0].name == 'mockuser3@test.co.za')
    assert(response.users[1].name == 'mockuser2@test.co.za')

    # Second player leaves
    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Leave(server_pb2.LeaveRequest(auth_id_token=token, session_id=session.session_id))

    assert(response.status == 'SUCCESS')

    # get session
    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.GetSessionById(server_pb2.GetSessionRequest(auth_id_token=token, session_id=session.session_id))
    assert(response.status == 'SUCCESS')
    assert(len(response.users) == 1)
    assert(response.users[0].name == 'mockuser3@test.co.za')

def test_join_rpc_good_login_nonexisting_session():
    auth.revoke_refresh_tokens(uid)
    
    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id='invalid_id'))

    assert(response.name == 'NULL')
    assert(response.session_id == 'NULL')
    assert(response.status == 'FAILED')
    assert(response.status_message == '[JOIN] No session with that ID exists!')

def test_setmax_rpc_good_login_setmax_session():
    auth.revoke_refresh_tokens(uid)
    
    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

        # Create session
    token = str(subprocess.check_output('node ./login.mjs mockuser@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2))
    
    assert(session.status == 'SUCCESS')

    response = stub.SetMax(server_pb2.SetMaxPlayersRequest(auth_id_token=token, session_id=session.session_id, number=0))

    assert(response.name == 'mysession')
    assert(len(response.session_id) == 36)
    assert(response.status == 'SUCCESS')
    assert(response.max_players == 0)

def test_join_rpc_good_login_full_session():
    auth.revoke_refresh_tokens(uid)
    
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = _create_rpc_good_login()

    token = str(subprocess.check_output('node ./login.mjs mockuser@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    stub.SetMax(server_pb2.SetMaxPlayersRequest(auth_id_token=token, session_id=session.session_id, number=0))
    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

    assert(response.name == 'NULL')
    assert(response.session_id == 'NULL')
    assert(response.status == 'FAILED')
    assert(response.status_message == '[JOIN] This session is full!')
    assert(response.full == True)

def test_rpc_good_login_get_session_by_id():
    auth.revoke_refresh_tokens(uid)
    
    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = _create_rpc_good_login()
    response = stub.GetSessionById(server_pb2.GetSessionRequest(auth_id_token=token, session_id=session.session_id))

    assert(response.name == 'mysession')
    assert(response.session_id == session.session_id)
    assert(response.status == 'SUCCESS')

def test_setmax_rpc_good_login_setmax_session_invalid_user():
    auth.revoke_refresh_tokens(uid)
    
    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = _create_rpc_good_login()

    response = stub.SetMax(server_pb2.SetMaxPlayersRequest(auth_id_token=token, session_id=session.session_id, number=0))

    assert(response.name == 'NULL')
    assert(response.status_message == '[SetMax] You must be the dungeon master to use this command!')
    assert(response.status == 'FAILED')

def test_list_rpc_good_login_list_sessions_that_are_full():
    auth.revoke_refresh_tokens(uid)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=0))
    stub.SetMax(server_pb2.SetMaxPlayersRequest(session_id=session.session_id, auth_id_token=token, number=0))
    response = stub.List(server_pb2.ListRequest(auth_id_token=token, limit=3, full=True))

    assert(response.status == 'SUCCESS')
    assert(response.sessions[0].full == True)
    assert(len(response.sessions) <= 3)

def test_kick_good_login():
    auth.revoke_refresh_tokens(uid)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2))
    
    # Third player join
    token = str(subprocess.check_output('node ./login.mjs mockuser3@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

    assert(response.status == 'SUCCESS')
    assert(len(response.users) == 1)
    assert(response.users[0].name == 'mockuser3@test.co.za')

    # Second player join
    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

    assert(response.status == 'SUCCESS')
    assert(len(response.users) ==  2)
    assert(response.users[0].name == 'mockuser3@test.co.za')
    assert(response.users[1].name == 'mockuser2@test.co.za')

    user2 = response.users[1]

    # kick player 2
    # login as DM
    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Kick(server_pb2.KickPlayerRequest(auth_id_token=token, session_id=session.session_id, user=user2))

    # check if user still in session
    assert(response.status == 'SUCCESS')
    assert(len(response.users) == 1)
    assert(response.users[0].name == 'mockuser3@test.co.za')

def test_kick_unauthorised_good_login():
    auth.revoke_refresh_tokens(uid)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2))
    
    # Third player join
    token = str(subprocess.check_output('node ./login.mjs mockuser3@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

    assert(response.status == 'SUCCESS')
    assert(len(response.users) == 1)
    assert(response.users[0].name == 'mockuser3@test.co.za')

    # Second player join
    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

    assert(response.status ==  'SUCCESS')
    assert(len(response.users) ==  2)
    assert(response.users[0].name ==  'mockuser3@test.co.za')
    assert(response.users[1].name ==  'mockuser2@test.co.za')

    user2 = response.users[1]

    # kick player 2
    # login as player 2
    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Kick(server_pb2.KickPlayerRequest(auth_id_token=token, session_id=session.session_id, user=user2))

    # should fail
    assert(response.status ==  'FAILED')
    assert(response.status_message ==  '[Kick] You must be the dungeon master to use this command!')

def test_private_session_should_not_be_listed():
    auth.revoke_refresh_tokens(uid)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=True))
    # should be first result, if something is wrong
    response = stub.List(server_pb2.ListRequest(auth_id_token=token, limit=1))

    assert(response.sessions[0].session_id != session.session_id)

def test_non_private_session_should_be_listed():
    auth.revoke_refresh_tokens(uid)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=False))
    # should be first result
    response = stub.List(server_pb2.ListRequest(auth_id_token=token, limit=1))

    assert(response.sessions[0].session_id ==  session.session_id)

def test_join_own_session_should_pass_session_should_not_grow():
    auth.revoke_refresh_tokens(uid)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=False))
    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id = session.session_id))

    assert(response.status ==  'SUCCESS')
    assert(len(response.users) ==  0)
    assert(response.full ==  False)

def test_leaving_a_session_as_last_user_should_delete_session():
    auth.revoke_refresh_tokens(uid)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=False))
    response = stub.Leave(server_pb2.JoinRequest(auth_id_token=token, session_id = session.session_id))

    assert(response.status ==  'SUCCESS')

    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id = session.session_id))
    assert(response.status ==  'FAILED')
    assert(response.status_message == '[JOIN] No session with that ID exists!')

def test_leaving_a_session_as_dungeon_master_should_assign_new_DM():
    auth.revoke_refresh_tokens(uid)

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=False))
    
    assert(session.status ==  'SUCCESS')

    # Join as player 2
    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id = session.session_id))

    assert(response.status ==  'SUCCESS')

    # Leave as Dungeon Master
    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Leave(server_pb2.JoinRequest(auth_id_token=token, session_id = session.session_id))

    assert(response.status ==  'SUCCESS')

    # player 2 should now have become the next dungeon master
    response = stub.GetSessionById(server_pb2.GetSessionRequest(auth_id_token=token, session_id = session.session_id))
    assert(response.status ==  'SUCCESS')
    assert(response.dungeon_master.name ==  'mockuser2@test.co.za')
    assert(len(response.users) ==  0)

def test_setname_rpc():
    auth.revoke_refresh_tokens(uid)
    
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=False))

    assert(session.status ==  'SUCCESS')

    response = stub.SetName(server_pb2.SetNameRequest(session_id=session.session_id, name='newNameForMySession', auth_id_token=token))

    assert(response.status ==  'SUCCESS')
    assert(response.name ==  'newNameForMySession')

def test_setname_rpc_unauthorised_user():
    auth.revoke_refresh_tokens(uid)
    
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=False))

    assert(session.status ==  'SUCCESS')

    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.SetName(server_pb2.SetNameRequest(session_id=session.session_id, name='newNameForMySession', auth_id_token=token))

    assert(response.status ==  'FAILED')
    assert(response.status_message ==  '[SetName] You must be the dungeon master to use this command!')

def test_setprivate_rpc():
    auth.revoke_refresh_tokens(uid)
    
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=False))

    assert(session.status ==  'SUCCESS')

    response = stub.SetPrivate(server_pb2.SetPrivateRequest(session_id=session.session_id, private=True, auth_id_token=token))

    assert(response.status ==  'SUCCESS')
    assert(response.private ==  True)

def test_setprivate_rpc_unauthorised_user():
    auth.revoke_refresh_tokens(uid)
    
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=False))

    assert(session.status ==  'SUCCESS')

    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.SetPrivate(server_pb2.SetPrivateRequest(session_id=session.session_id, private=True, auth_id_token=token))

    assert(response.status ==  'FAILED')
    assert(response.status_message ==  '[SetPrivate] You must be the dungeon master to use this command!')

def test_joining_session_you_are_already_in_should_return_normal_session():
    auth.revoke_refresh_tokens(uid)
    
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=False))

    assert(session.status ==  'SUCCESS')

    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(server_pb2.JoinRequest(session_id=session.session_id, auth_id_token=token))

    assert(response.status ==  'SUCCESS')
    assert(len(response.users) ==  1)
    assert(response.full ==  False)
    assert(response.users[0].name == 'mockuser2@test.co.za')

    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(server_pb2.JoinRequest(session_id=session.session_id, auth_id_token=token))
    
    assert(response.status == 'SUCCESS')
    # This is what we are really testing. This should not increase.
    assert(len(response.users) == 1)
    assert(response.full == False)
    assert(response.users[0].name == 'mockuser2@test.co.za')

def test_list_user_sessions_rpc_good_login():
    auth.revoke_refresh_tokens(uid)

    token = str(subprocess.check_output('node ./login.mjs mockuser2@test.co.za', shell=True, universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = _create_rpc_good_login()

    response = stub.Join(server_pb2.JoinRequest(auth_id_token=token, session_id=session.session_id))

    assert(response.status == 'SUCCESS')

    response = stub.GetSessionsOfUser(server_pb2.GetSessionsOfUserRequest(auth_id_token=token, limit=3))

    assert(response.status == 'SUCCESS')
    assert(len(response.sessions) <= 3)
    assert(len(response.sessions) > 0)

    # Should not list a session where another user is not in.
    assert(response.sessions[0].users[0].name == 'mockuser2@test.co.za')
    assert(len(response.sessions[0].users) == 1)


#def test_max_sessions_for_user():
#    auth.revoke_refresh_tokens(uid)
    
#    channel = grpc.insecure_channel(server)
#    stub = server_pb2_grpc.SessionsManagerStub(channel)

#    token = str(subprocess.check_output('node ./login.mjs', shell=True, universal_newlines=False).decode("utf-8")).strip()
    
#    for i in range(0, 9):
#        session = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=False))
#        assert(session.status, 'SUCCESS')

#    response = stub.Create(server_pb2.NewSessionRequest(name='mysession', auth_id_token=token, max_players=2, private=False))

#    assert(response.status, 'FAILED')
#    assert(response.status_message, '[Create] User has too many sessions already!')