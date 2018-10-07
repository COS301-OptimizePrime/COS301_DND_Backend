from __future__ import print_function

import subprocess

import grpc
import server_pb2
import server_pb2_grpc

server = 'localhost:50051'
# server = 'develop.optimizeprime.co.za:50051'
test_session_id = ''
uid = 'mT8HzwXWjDc1FX472qTfcsUUcQt1'

token1 = str(
    subprocess.check_output(
        'node ./login.mjs',
        shell=True,
        universal_newlines=False).decode("utf-8")).strip()
token2 = str(
    subprocess.check_output(
        'node ./login.mjs mockuser2@test.co.za',
        shell=True,
        universal_newlines=False).decode("utf-8")).strip()
token3 = str(
    subprocess.check_output(
        'node ./login.mjs mockuser3@test.co.za',
        shell=True,
        universal_newlines=False).decode("utf-8")).strip()
token4 = str(
    subprocess.check_output(
        'node ./login.mjs mockuser4@test.co.za',
        shell=True,
        universal_newlines=False).decode("utf-8")).strip()
token5 = str(
    subprocess.check_output(
        'node ./login.mjs mockuser5@test.co.za',
        shell=True,
        universal_newlines=False).decode("utf-8")).strip()


def _create_rpc_good_login(token=token1, session_name=None):
    if session_name is None:
        session_name = 'mysession'

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    response = stub.Create(
        server_pb2.NewSessionRequest(
            name=session_name,
            auth_id_token=token,
            max_players=7))

    assert response.name == session_name
    assert len(response.session_id) == 36
    assert response.status == 'SUCCESS'

    return response


def _create_rpc_good_login_reuse_stub(stub, token):
    response = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token,
            max_players=7))

    assert response.name == 'mysession'
    assert len(response.session_id) == 36
    assert response.status == 'SUCCESS'

    return response


def test_create_rpc_good_login_fresh_stubs(benchmark):
    benchmark(_create_rpc_good_login)


def test_create_rpc_good_login_reuse_stub(benchmark):
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    benchmark(_create_rpc_good_login_reuse_stub, stub, token=token1)
    channel.close()


def test_create_rpc_bad_login():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    response = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token='invalidtoken'))
    assert response.name == 'NULL'
    assert response.session_id == 'NULL'
    assert response.status == 'FAILED'
    channel.close()


def test_list_rpc_good_login():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    response = stub.List(server_pb2.ListRequest(auth_id_token=token1, limit=3))

    assert response.status == 'SUCCESS'
    assert len(response.sessions) <= 3
    channel.close()


def test_rpc_good_login_leave_if_not_in_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    # Create session
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=2))

    response = stub.Leave(
        server_pb2.LeaveRequest(
            auth_id_token=token2,
            session_id=session.session_id))

    assert response.status == 'FAILED'
    assert response.status_message == '[Leave] User is not in the session!'
    channel.close()


def test_join_rpc_good_login_existing_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = _create_rpc_good_login(token2)

    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token2,
            session_id=session.session_id))

    assert response.name == 'mysession'
    assert len(response.session_id) == 36
    assert response.status == 'SUCCESS'
    channel.close()


def test_leave_rpc_good_login_leave_session_multiple_already_joined():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    # Add new session in case none exist.
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=2))

    # Third player join
    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token3,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'
    assert len(response.users) == 1
    assert response.users[0].name == 'mockuser3@test.co.za'

    # Second player join
    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token2,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'
    assert len(response.users) == 2
    assert response.users[0].name == 'mockuser3@test.co.za'
    assert response.users[1].name == 'mockuser2@test.co.za'

    # Second player leaves
    response = stub.Leave(
        server_pb2.LeaveRequest(
            auth_id_token=token2,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'

    # get session
    response = stub.GetSessionById(
        server_pb2.GetSessionRequest(
            auth_id_token=token1,
            session_id=session.session_id))
    assert response.status == 'SUCCESS'
    assert len(response.users) == 1
    assert response.users[0].name == 'mockuser3@test.co.za'
    channel.close()


def test_join_rpc_good_login_nonexisting_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token1,
            session_id='invalid_id'))

    assert response.name == 'NULL'
    assert response.session_id == 'NULL'
    assert response.status == 'FAILED'
    assert response.status_message == '[JOIN] No session with that ID exists!'
    channel.close()


def test_setmax_rpc_good_login_setmax_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    # Create session
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=2))

    assert (session.status == 'SUCCESS')

    response = stub.SetMax(
        server_pb2.SetMaxPlayersRequest(
            auth_id_token=token1,
            session_id=session.session_id,
            number=0))

    assert response.name == 'mysession'
    assert len(response.session_id) == 36
    assert response.status == 'SUCCESS'
    assert response.max_players == 0
    channel.close()


def test_join_rpc_good_login_full_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = _create_rpc_good_login()

    # User 1
    stub.SetMax(
        server_pb2.SetMaxPlayersRequest(
            auth_id_token=token1,
            session_id=session.session_id,
            number=0))

    # User 2
    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token2,
            session_id=session.session_id))

    assert response.name == 'NULL'
    assert response.session_id == 'NULL'
    assert response.status == 'FAILED'
    assert response.status_message == '[JOIN] This session is full!'
    assert response.full
    channel.close()


def test_rpc_good_login_get_session_by_id():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = _create_rpc_good_login(token1)
    response = stub.GetSessionById(
        server_pb2.GetSessionRequest(
            auth_id_token=token1,
            session_id=session.session_id))

    assert response.name == 'mysession'
    assert response.session_id == session.session_id
    assert response.status == 'SUCCESS'
    channel.close()


def test_rpc_good_login_get_light_session_by_id():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = _create_rpc_good_login(token1)
    response = stub.GetLightSessionById(
        server_pb2.GetSessionRequest(
            auth_id_token=token1,
            session_id=session.session_id))

    assert response.name == 'mysession'
    assert response.session_id == session.session_id
    assert response.status == 'SUCCESS'
    channel.close()


def test_setmax_rpc_good_login_setmax_session_invalid_user():
    session = _create_rpc_good_login()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    response = stub.SetMax(
        server_pb2.SetMaxPlayersRequest(
            auth_id_token=token2,
            session_id=session.session_id,
            number=0))

    assert response.name == 'NULL'
    assert response.status_message == '[SetMax] You must be the dungeon master to use this command!'
    assert response.status == 'FAILED'
    channel.close()


def test_list_rpc_good_login_list_sessions_that_are_full():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=0))
    stub.SetMax(
        server_pb2.SetMaxPlayersRequest(
            session_id=session.session_id,
            auth_id_token=token1,
            number=0))
    response = stub.List(
        server_pb2.ListRequest(
            auth_id_token=token1,
            limit=3,
            full=True))

    assert response.status == 'SUCCESS'
    assert response.sessions[0].full
    assert len(response.sessions) <= 3
    channel.close()


def test_kick_good_login():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=2))

    # Third player join
    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token3,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'
    assert len(response.users) == 1
    assert response.users[0].name == 'mockuser3@test.co.za'

    # Second player join
    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token2,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'
    assert len(response.users) == 2
    assert response.users[0].name == 'mockuser3@test.co.za'
    assert response.users[1].name == 'mockuser2@test.co.za'

    user2 = response.users[1]

    # kick player 2
    # login as DM
    response = stub.Kick(
        server_pb2.KickPlayerRequest(
            auth_id_token=token1,
            session_id=session.session_id,
            user=user2))

    # check if user still in session
    assert response.status == 'SUCCESS'
    assert len(response.users) == 1
    assert response.users[0].name == 'mockuser3@test.co.za'


def test_kick_unauthorised_good_login():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=2))

    # Third player join
    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token3,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'
    assert len(response.users) == 1
    assert response.users[0].name == 'mockuser3@test.co.za'

    # Second player join
    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token2,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'
    assert len(response.users) == 2
    assert response.users[0].name == 'mockuser3@test.co.za'
    assert response.users[1].name == 'mockuser2@test.co.za'

    user2 = response.users[1]

    # kick player 2
    # login as player 2
    response = stub.Kick(
        server_pb2.KickPlayerRequest(
            auth_id_token=token2,
            session_id=session.session_id,
            user=user2))

    # should fail
    assert response.status == 'FAILED'
    assert response.status_message == '[Kick] You must be the dungeon master to use this command!'


def test_private_session_should_not_be_listed():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=2,
            private=True))
    # should be first result, if something is wrong
    response = stub.List(server_pb2.ListRequest(auth_id_token=token1, limit=1))

    assert response.sessions[0].session_id != session.session_id


def test_non_private_session_should_be_listed():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=2,
            private=False))
    # should be first result
    response = stub.List(server_pb2.ListRequest(auth_id_token=token1, limit=1))

    assert response.sessions[0].session_id == session.session_id


def test_join_own_session_should_pass_session_should_not_grow():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=2,
            private=False))
    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token1,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'
    assert len(response.users) == 0
    assert response.full is False


def test_leaving_a_session_as_last_user_should_delete_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=2,
            private=False))
    response = stub.Leave(
        server_pb2.JoinRequest(
            auth_id_token=token1,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'

    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token1,
            session_id=session.session_id))

    assert response.status == 'FAILED'
    assert response.status_message == '[JOIN] No session with that ID exists!'


def test_leaving_a_session_as_dungeon_master_should_assign_new_DM():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    # Add new session in case none exist.
    token = str(
        subprocess.check_output(
            'node ./login.mjs',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token,
            max_players=2,
            private=False))

    assert session.status == 'SUCCESS'

    # Join as player 2
    token = str(
        subprocess.check_output(
            'node ./login.mjs mockuser2@test.co.za',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'

    # Leave as Dungeon Master
    token = str(
        subprocess.check_output(
            'node ./login.mjs',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    response = stub.Leave(
        server_pb2.JoinRequest(
            auth_id_token=token,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'

    # player 2 should now have become the next dungeon master
    response = stub.GetSessionById(
        server_pb2.GetSessionRequest(
            auth_id_token=token,
            session_id=session.session_id))
    assert response.status == 'SUCCESS'
    assert response.dungeon_master.name == 'mockuser2@test.co.za'
    assert len(response.users) == 0


def test_setname_rpc():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    token = str(
        subprocess.check_output(
            'node ./login.mjs',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token,
            max_players=2,
            private=False))

    assert session.status == 'SUCCESS'

    response = stub.SetName(
        server_pb2.SetNameRequest(
            session_id=session.session_id,
            name='newNameForMySession',
            auth_id_token=token))

    assert response.status == 'SUCCESS'
    assert response.name == 'newNameForMySession'


def test_setname_rpc_unauthorised_user():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    token = str(
        subprocess.check_output(
            'node ./login.mjs',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token,
            max_players=2,
            private=False))

    assert session.status == 'SUCCESS'

    token = str(
        subprocess.check_output(
            'node ./login.mjs mockuser2@test.co.za',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    response = stub.SetName(
        server_pb2.SetNameRequest(
            session_id=session.session_id,
            name='newNameForMySession',
            auth_id_token=token))

    assert response.status == 'FAILED'
    assert response.status_message == '[SetName] You must be the dungeon master to use this command!'


def test_setprivate_rpc():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    token = str(
        subprocess.check_output(
            'node ./login.mjs',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token,
            max_players=2,
            private=False))

    assert session.status == 'SUCCESS'

    response = stub.SetPrivate(
        server_pb2.SetPrivateRequest(
            session_id=session.session_id,
            private=True,
            auth_id_token=token))

    assert response.status == 'SUCCESS'
    assert response.private is True


def test_setprivate_rpc_unauthorised_user():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    token = str(
        subprocess.check_output(
            'node ./login.mjs',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token,
            max_players=2,
            private=False))

    assert session.status == 'SUCCESS'

    token = str(
        subprocess.check_output(
            'node ./login.mjs mockuser2@test.co.za',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    response = stub.SetPrivate(
        server_pb2.SetPrivateRequest(
            session_id=session.session_id,
            private=True,
            auth_id_token=token))

    assert response.status == 'FAILED'
    assert response.status_message == '[SetPrivate] You must be the dungeon master to use this command!'


def test_joining_session_you_are_already_in_should_return_normal_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    token = str(
        subprocess.check_output(
            'node ./login.mjs',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token,
            max_players=2,
            private=False))

    assert session.status == 'SUCCESS'

    token = str(
        subprocess.check_output(
            'node ./login.mjs mockuser2@test.co.za',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(
        server_pb2.JoinRequest(
            session_id=session.session_id,
            auth_id_token=token))

    assert response.status == 'SUCCESS'
    assert len(response.users) == 1
    assert response.full is False
    assert response.users[0].name == 'mockuser2@test.co.za'

    token = str(
        subprocess.check_output(
            'node ./login.mjs mockuser2@test.co.za',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(
        server_pb2.JoinRequest(
            session_id=session.session_id,
            auth_id_token=token))

    assert response.status == 'SUCCESS'
    # This is what we are really testing. This should not increase.
    assert len(response.users) == 1
    assert response.full is False
    assert response.users[0].name == 'mockuser2@test.co.za'


def test_list_user_sessions_rpc_good_login():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = _create_rpc_good_login()

    token = str(
        subprocess.check_output(
            'node ./login.mjs mockuser4@test.co.za',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'

    response = stub.GetSessionsOfUser(
        server_pb2.GetSessionsOfUserRequest(
            auth_id_token=token, limit=3))

    assert response.status == 'SUCCESS'
    assert len(response.light_sessions) == 3

    # Should not list a session where another user is not in.
    assert response.light_sessions[0].dungeon_master.name == 'mockuser4@test.co.za'
    # Removed for light sessions
    # assert response.light_sessions[0].users[0].name == 'mockuser4@test.co.za'


def test_ready_up():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = _create_rpc_good_login()

    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token4,
            session_id=session.session_id))
    assert response.status == 'SUCCESS'

    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token3,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'

    # Now we should have 2 users in our session

    # Change state as DM
    response = stub.ChangeState(
        server_pb2.ChangeStateRequest(
            auth_id_token=token1,
            session_id=session.session_id,
            state="READYUP"))

    assert response.status == 'SUCCESS'

    response = stub.GetSessionById(
        server_pb2.GetSessionRequest(
            auth_id_token=token1,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'

    org_state_meta = response.state_meta
    org_state_ready = response.state_ready_start_time

    # Other users should now be able to ready up
    response = stub.Ready(
        server_pb2.ReadyUpRequest(
            auth_id_token=token4,
            session_id=session.session_id))
    assert response.status == 'SUCCESS'

    response = stub.GetSessionById(
        server_pb2.GetSessionRequest(
            auth_id_token=token4,
            session_id=session.session_id))
    assert response.status == 'SUCCESS'
    assert response.state == 'READYUP'
    assert response.first_started_time == 'None'
    assert response.state_meta == org_state_meta
    assert response.state_ready_start_time == org_state_ready

    response = stub.Ready(
        server_pb2.ReadyUpRequest(
            auth_id_token=token3,
            session_id=session.session_id))
    assert response.status == 'SUCCESS'

    # Session should now be in exploring state
    response = stub.GetSessionById(
        server_pb2.GetSessionRequest(
            auth_id_token=token3,
            session_id=session.session_id))
    assert response.status == 'SUCCESS'
    assert response.state == 'EXPLORING'
    assert len(response.first_started_time) > 0
    assert response.state_meta > org_state_meta
    assert response.state_ready_start_time == org_state_ready


def test_expiry_readyup_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = _create_rpc_good_login()
    # DM
    response = stub.ChangeReadyUpExpiryTime(
        server_pb2.ChangeReadyUpExpiryTimeRequest(
            auth_id_token=token1,
            session_id=session.session_id,
            ready_up_expiry_time=0))
    assert response.status == 'SUCCESS'

    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token4,
            session_id=session.session_id))
    assert response.status == 'SUCCESS'

    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token3,
            session_id=session.session_id))

    assert response.status == 'SUCCESS'

    # Other users should now be able to ready up

    response = stub.Ready(
        server_pb2.ReadyUpRequest(
            auth_id_token=token4,
            session_id=session.session_id))
    assert response.status == 'FAILED'


def test_list_user_sessions_when_none_exist():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    response = stub.GetSessionsOfUser(
        server_pb2.GetSessionsOfUserRequest(
            auth_id_token=token5, limit=3))
    assert response.status == 'SUCCESS'
    assert len(response.light_sessions) == 0


def test_list_user_sessions_check_that_both_dm_and_non_dm_show():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    stub.Create(
        server_pb2.NewSessionRequest(
            name='my session mock5',
            auth_id_token=token5,
            max_players=7))

    response = stub.GetSessionsOfUser(
        server_pb2.GetSessionsOfUserRequest(
            auth_id_token=token5, limit=3))

    assert response.status == 'SUCCESS'
    assert len(response.light_sessions) == 1
    assert response.light_sessions[0].name == 'my session mock5'

    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='not my session mock4',
            auth_id_token=token4,
            max_players=7))

    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token5, session_id=session.session_id))

    assert response.status == 'SUCCESS'

    response = stub.GetSessionsOfUser(
        server_pb2.GetSessionsOfUserRequest(
            auth_id_token=token5, limit=3))
    assert response.status == 'SUCCESS'
    assert len(response.light_sessions) == 2
    assert response.light_sessions[0].name == 'my session mock5'
    assert response.light_sessions[1].name == 'not my session mock4'


def test_multiple_ready_up_should_not_cause_sessions_to_start_if_from_same_user():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='my session mock5',
            auth_id_token=token5,
            max_players=7))

    assert session.status == 'SUCCESS'

    stub.ChangeState(
        server_pb2.ChangeStateRequest(
            auth_id_token=token5,
            session_id=session.session_id,
            state='READYUP'))

    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token4, session_id=session.session_id))

    assert response.status == 'SUCCESS'

    response = stub.Join(
        server_pb2.JoinRequest(
            auth_id_token=token3, session_id=session.session_id))

    assert response.status == 'SUCCESS'

    response = stub.Ready(
        server_pb2.ReadyUpRequest(
            auth_id_token=token4, session_id=session.session_id))

    assert response.status == 'SUCCESS'
    response = stub.Ready(
        server_pb2.ReadyUpRequest(
            auth_id_token=token4, session_id=session.session_id))

    assert response.status == 'SUCCESS'

    session = stub.GetSessionById(server_pb2.GetSessionRequest(auth_id_token=token4, session_id=session.session_id))

    assert session.state == 'READYUP'
    assert len(session.users) == 2
