from __future__ import print_function

import subprocess

import firebase_admin
import grpc
import pytest
import pytest_benchmark
from firebase_admin import auth, credentials

import server_pb2
import server_pb2_grpc

import random

cred = credentials.Certificate(
    "dnd-game-manager-firebase-adminsdk-34ek4-cccabd3dd6.json")
firebase = firebase_admin.initialize_app(cred)

server = 'localhost:50051'
#server = 'develop.optimizeprime.co.za:50051'
test_session_id = ''
uid = 'mT8HzwXWjDc1FX472qTfcsUUcQt1'

def getRandomCharacter():
    _character = server_pb2.Character()
    _character.name = "MyTestCharacter"

    _character.strength = random.randint(1,50)
    _character.strength_subscript = random.randint(1,50)
    _character.dexterity = random.randint(1,50)
    _character.dexterity_subscript = random.randint(1,50)
    _character.constitution = random.randint(1,50)
    _character.constitution_subscript = random.randint(1,50)
    _character.intelligence = random.randint(1,50)
    _character.intelligence_subscript = random.randint(1,50)
    _character.wisdom = random.randint(1,50)
    _character.wisdom_subscript = random.randint(1,50)
    _character.charisma = random.randint(1,50)
    _character.charisma_subscript = random.randint(1,50)
    _character.character_class = "TEST CLASS"
    _character.race = "TEST RACE"
    _character.xp = random.randint(1,50)
    _character.alignment = "TEST ALIGNMENT"
    _character.background = "TEST BACKGROUND"
    _character.inspiration = random.randint(1,50)
    _character.proficiency_bonus = random.randint(1,50)
    
    _character.skills.acrobatics = random.randint(1,50)
    _character.skills.acrobatics_proficient = random.choice([True, False])
    _character.skills.animal_handling = random.randint(1,50)
    _character.skills.animal_handling_proficient = random.choice([True, False])
    _character.skills.arcana = random.randint(1,50)
    _character.skills.arcana_proficient = random.choice([True, False])
    _character.skills.athletics = random.randint(1,50)
    _character.skills.athletics_proficient = random.choice([True, False])
    _character.skills.deception = random.randint(1,50)
    _character.skills.deception_proficient = random.choice([True, False])
    _character.skills.history = random.randint(1,50)
    _character.skills.history_proficient = random.choice([True, False])
    _character.skills.insight = random.randint(1,50)
    _character.skills.insight_proficient = random.choice([True, False])
    _character.skills.intimidation = random.randint(1,50)
    _character.skills.intimidation_proficient = random.choice([True, False])
    _character.skills.investigation = random.randint(1,50)
    _character.skills.investigation_proficient = random.choice([True, False])
    _character.skills.medicine = random.randint(1,50)
    _character.skills.medicine_proficient = random.choice([True, False])
    _character.skills.nature = random.randint(1,50)
    _character.skills.nature_proficient = random.choice([True, False])
    _character.skills.perception = random.randint(1,50)
    _character.skills.perception_proficient = random.choice([True, False])
    _character.skills.performance = random.randint(1,50)
    _character.skills.performance_proficient = random.choice([True, False])
    _character.skills.persuasion = random.randint(1,50)
    _character.skills.persuasion_proficient = random.choice([True, False])
    _character.skills.religion = random.randint(1,50)
    _character.skills.religion_proficient = random.choice([True, False])
    _character.skills.sleight_of_hand = random.randint(1,50)
    _character.skills.sleight_of_hand_proficient = random.choice([True, False])
    _character.skills.stealth = random.randint(1,50)
    _character.skills.stealth_proficient = random.choice([True, False])
    _character.skills.survival = random.randint(1,50)
    _character.skills.survival_proficient = random.choice([True, False])

    return _character

def compareCharacters(character1,character2):

    assert character1.name == character2.name
    assert character1.strength == character2.strength
    assert character1.strength_subscript == character2.strength_subscript
    assert character1.dexterity == character2.dexterity
    assert character1.dexterity_subscript == character2.dexterity_subscript
    assert character1.constitution == character2.constitution
    assert character1.constitution_subscript == character2.constitution_subscript
    assert character1.intelligence == character2.intelligence
    assert character1.intelligence_subscript == character2.intelligence_subscript
    assert character1.wisdom == character2.wisdom
    assert character1.wisdom_subscript == character2.wisdom_subscript
    assert character1.charisma == character2.charisma
    assert character1.charisma_subscript == character2.charisma_subscript
    assert character1.character_class == character2.character_class
    assert character1.race == character2.race
    assert character1.xp == character2.xp
    assert character1.alignment == character2.alignment
    assert character1.background == character2.background
    assert character1.inspiration == character2.inspiration
    assert character1.proficiency_bonus == character2.proficiency_bonus

    assert character1.skills.acrobatics == character2.skills.acrobatics
    assert character1.skills.acrobatics_proficient == character2.skills.acrobatics_proficient
    assert character1.skills.animal_handling == character2.skills.animal_handling
    assert character1.skills.animal_handling_proficient ==                      character2.skills.animal_handling_proficient
    assert character1.skills.arcana == character2.skills.arcana
    assert character1.skills.arcana_proficient == character2.skills.arcana_proficient
    assert character1.skills.athletics == character2.skills.athletics
    assert character1.skills.athletics_proficient == character2.skills.athletics_proficient
    assert character1.skills.deception == character2.skills.deception
    assert character1.skills.deception_proficient == character2.skills.deception_proficient
    assert character1.skills.history == character2.skills.history
    assert character1.skills.history_proficient == character2.skills.history_proficient
    assert character1.skills.insight == character2.skills.insight
    assert character1.skills.insight_proficient == character2.skills.insight_proficient
    assert character1.skills.intimidation == character2.skills.intimidation
    assert character1.skills.intimidation_proficient == character2.skills.intimidation_proficient
    assert character1.skills.investigation == character2.skills.investigation
    assert character1.skills.investigation_proficient == character2.skills.investigation_proficient
    assert character1.skills.medicine == character2.skills.medicine
    assert character1.skills.medicine_proficient == character2.skills.medicine_proficient
    assert character1.skills.nature == character2.skills.nature
    assert character1.skills.nature_proficient == character2.skills.nature_proficient
    assert character1.skills.perception == character2.skills.perception
    assert character1.skills.perception_proficient == character2.skills.perception_proficient
    assert character1.skills.performance == character2.skills.performance
    assert character1.skills.performance_proficient == character2.skills.performance_proficient
    assert character1.skills.persuasion == character2.skills.persuasion
    assert character1.skills.persuasion_proficient == character2.skills.persuasion_proficient
    assert character1.skills.religion == character2.skills.religion
    assert character1.skills.religion_proficient == character2.skills.religion_proficient
    assert character1.skills.sleight_of_hand == character2.skills.sleight_of_hand
    assert character1.skills.sleight_of_hand_proficient == character2.skills.sleight_of_hand_proficient
    assert character1.skills.stealth == character2.skills.stealth
    assert character1.skills.stealth_proficient == character2.skills.stealth_proficient
    assert character1.skills.survival == character2.skills.survival
    assert character1.skills.survival_proficient == character2.skills.survival_proficient

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

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'
    _char.skills.acrobatics = 5

    response = stub.CreateCharacter(server_pb2.NewCharacterRequest(auth_id_token=token, character=_char))
    assert response.status == 'SUCCESS'

    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.skills.acrobatics == 5

    compareCharacters(_char, response)

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

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    character = stub.CreateCharacter(server_pb2.NewCharacterRequest(auth_id_token=token, character=_char))
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

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = stub.CreateCharacter(server_pb2.NewCharacterRequest(auth_id_token=global_token, character=_char))
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

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = stub.CreateCharacter(server_pb2.NewCharacterRequest(auth_id_token=global_token, character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'

    _char_id = response.character_id

    response = stub.GetCharacterById(server_pb2.GetCharacterByIdRequest(auth_id_token=global_token, character_id=_char_id))
    assert response.status == 'SUCCESS'
    assert response.character_id == _char_id
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'

def test_update_character():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = stub.CreateCharacter(server_pb2.NewCharacterRequest(auth_id_token=global_token, character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'

    _char = response
    _char.name = 'Modified name!'
    
    response = stub.UpdateCharacter(server_pb2.UpdateCharacterRequest(auth_id_token=global_token, character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'Modified name!'