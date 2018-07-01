from __future__ import print_function

import subprocess

import firebase_admin
import grpc
import pytest
import pytest_benchmark
from firebase_admin import auth, credentials

import server_pb2
import server_pb2_grpc

cred = credentials.Certificate(
    "dnd-game-manager-firebase-adminsdk-34ek4-cccabd3dd6.json")
firebase = firebase_admin.initialize_app(cred)

server = 'localhost:50051'
#server = 'develop.optimizeprime.co.za:50051'
test_session_id = ''
uid = 'mT8HzwXWjDc1FX472qTfcsUUcQt1'

_character = server_pb2.Character()
_character.name = "MyTestCharacter"
_character.strength = 6
_character.strength_subscript = 3

global_token = str(
        subprocess.check_output(
            'node ./login.mjs',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()

def test_create_character():
    token = str(
        subprocess.check_output(
            'node ./login.mjs',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()

    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    response = stub.CreateCharacter(server_pb2.NewCharacterRequest(auth_id_token=token, character=_character))
    assert response.status == 'SUCCESS'

    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'


def test_get_characters():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    response = stub.GetCharacters(server_pb2.GetCharactersRequest(auth_id_token=global_token))
    
    assert response.status == 'SUCCESS'
    assert len(response.characters) > 0 
    assert response.characters[0].name == 'MyTestCharacter'
    assert response.characters[0].creator.name == 'mockuser@test.co.za'

def test_delete_character_does_not_exist():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)
    response = stub.DeleteCharacter(server_pb2.NewCharacterRequest(auth_id_token=global_token, character=None))

    assert response.status == 'FAILED'
    assert response.status_message == '[Delete Character] Character doesn\'t exist!'

def test_delete_character_that_not_ours():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    token = str(
        subprocess.check_output(
            'node ./login.mjs mockuser@test.co.za',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    character = stub.CreateCharacter(server_pb2.NewCharacterRequest(auth_id_token=token, character=_character))
    assert character.status == "SUCCESS"

    token = str(
        subprocess.check_output(
            'node ./login.mjs mockuser2@test.co.za',
            shell=True,
            universal_newlines=False).decode("utf-8")).strip()
    response = stub.DeleteCharacter(
        server_pb2.DeleteCharacterRequest(
            auth_id_token=token,
            character_id=character.character_id))

    assert response.status == "FAILED"
    assert response.status_message == "[Delete Character] Character is not yours!"

def test_delete_character():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    response = stub.CreateCharacter(server_pb2.NewCharacterRequest(auth_id_token=global_token, character=_character))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'

    _char = response

    # Delete
    response = stub.DeleteCharacter(server_pb2.DeleteCharacterRequest(auth_id_token=global_token, character_id=_char.character_id))

    assert response.status == "SUCCESS"

def test_get_character_by_id():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    response = stub.CreateCharacter(server_pb2.NewCharacterRequest(auth_id_token=global_token, character=_character))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'

    _char_id = response.character_id

    response = stub.GetCharacterById(server_pb2.GetCharacterByIdRequest(auth_id_token=global_token, character_id=_char_id))
    assert response.status == 'SUCCESS'
    assert response.character_id == _char_id
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'