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
    
    _character.passive_wisdom = random.randint(1,50)
    _character.personality_traits = "TEST PERSONALITY TRAITS"
    _character.ideals = "TEST IDEALS"
    _character.bonds = "TEST BONDS"
    _character.flaws = "TEST FLAWS"

    _character.saving_throws.strength = random.randint(1,50)
    _character.saving_throws.strength_proficient = random.choice([True, False])
    _character.saving_throws.dexterity = random.randint(1,50)
    _character.saving_throws.dexterity_proficient = random.choice([True, False])
    _character.saving_throws.constitution = random.randint(1,50)
    _character.saving_throws.constitution_proficient = random.choice([True, False])
    _character.saving_throws.intelligence = random.randint(1,50)
    _character.saving_throws.intelligence_proficient = random.choice([True, False])
    _character.saving_throws.wisdom = random.randint(1,50)
    _character.saving_throws.wisdom_proficient = random.choice([True, False])
    _character.saving_throws.charisma = random.randint(1,50)
    _character.saving_throws.charisma_subscript = random.randint(1,50)

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

    _character.hitpoints.armor_class = random.randint(1,50)
    _character.hitpoints.initiative = random.randint(1,50)
    _character.hitpoints.speed = random.randint(1,50)
    _character.hitpoints.current_hitpoints = random.randint(1,50)
    _character.hitpoints.max_hitpoints = random.randint(1,50)
    _character.hitpoints.temporary_hitpoints = random.randint(1,50)
    _character.hitpoints.hitdice = "HIT DICE"

    _character.hitpoints.deathsaves_success1 = random.choice([True, False])
    _character.hitpoints.deathsaves_success2 = random.choice([True, False])
    _character.hitpoints.deathsaves_success3 = random.choice([True, False])

    _character.hitpoints.deathsaves_failures1 = random.choice([True, False])
    _character.hitpoints.deathsaves_failures2 = random.choice([True, False])
    _character.hitpoints.deathsaves_failures3 = random.choice([True, False])

    _character.equipment.extend([])

    _eq = server_pb2.Equipment()
    _eq.name  = "TEST EQ"
    _eq.value  = random.randint(1,50)
    _eq2 = server_pb2.Equipment()
    _eq2.name  = "TEST EQ"
    _eq2.value  = random.randint(1,50)

    _character.equipment.extend([_eq])
    _character.equipment.extend([_eq2])

    _character.session_id = 'TESTSESSIONID'

    return _character

def compareCharacters(character1,character2):
    #assert character1.character_id == character2.character_id

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

    assert character1.passive_wisdom == character2.passive_wisdom
    assert character1.personality_traits == character2.personality_traits
    assert character1.ideals == character2.ideals
    assert character1.bonds == character2.bonds
    assert character1.flaws == character2.flaws

    assert character1.hitpoints.armor_class == character2.hitpoints.armor_class
    assert character1.hitpoints.initiative == character2.hitpoints.initiative
    assert character1.hitpoints.speed == character2.hitpoints.speed
    assert character1.hitpoints.current_hitpoints == character2.hitpoints.current_hitpoints
    assert character1.hitpoints.max_hitpoints == character2.hitpoints.max_hitpoints
    assert character1.hitpoints.temporary_hitpoints == character2.hitpoints.temporary_hitpoints
    assert character1.hitpoints.hitdice == character2.hitpoints.hitdice

    assert character1.hitpoints.deathsaves_success1 == character2.hitpoints.deathsaves_success1
    assert character1.hitpoints.deathsaves_success2 == character2.hitpoints.deathsaves_success2
    assert character1.hitpoints.deathsaves_success3 == character2.hitpoints.deathsaves_success3

    assert character1.hitpoints.deathsaves_failures1 == character2.hitpoints.deathsaves_failures1
    assert character1.hitpoints.deathsaves_failures2 == character2.hitpoints.deathsaves_failures2
    assert character1.hitpoints.deathsaves_failures3 == character2.hitpoints.deathsaves_failures3

    assert character1.saving_throws.strength == character2.saving_throws.strength
    assert character1.saving_throws.strength_proficient == character2.saving_throws.strength_proficient
    assert character1.saving_throws.dexterity == character2.saving_throws.dexterity
    assert character1.saving_throws.dexterity_proficient == character2.saving_throws.dexterity_proficient
    assert character1.saving_throws.constitution == character2.saving_throws.constitution
    assert character1.saving_throws.constitution_proficient == character2.saving_throws.constitution_proficient
    assert character1.saving_throws.intelligence == character2.saving_throws.intelligence
    assert character1.saving_throws.intelligence_proficient == character2.saving_throws.intelligence_proficient
    assert character1.saving_throws.wisdom == character2.saving_throws.wisdom
    assert character1.saving_throws.wisdom_proficient == character2.saving_throws.wisdom_proficient
    assert character1.saving_throws.charisma == character2.saving_throws.charisma
    assert character1.saving_throws.charisma_subscript == character2.saving_throws.charisma_subscript

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

    assert character1.equipment[0].name == character2.equipment[0].name 
    assert character1.equipment[1].name == character2.equipment[1].name 
    assert character1.equipment[0].value == character2.equipment[0].value 
    assert character1.equipment[1].value == character2.equipment[1].value 

    assert character1.session_id == character2.session_id

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

    # Appears to be a front end error.
    # Will however test for empty name
    def test_create_character_empty_name():
        channel = grpc.insecure_channel(server)
        stub = server_pb2_grpc.CharactersManagerStub(channel)

        _char = server_pb2.Character()
        _char.name = ""

        response = stub.CreateCharacter(server_pb2.NewCharacterRequest(auth_id_token=global_token, character=_char))
        assert response.status == 'FAILED'
        assert response.status_message == '[CreateChar] Character name may not be blank!'

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

    _char = getRandomCharacter()
    _char.character_id = response.character_id
    _char.name = 'Modified name!'
    _char.equipment[0].name = "Modified name!"
    _char.equipment[0].value = 99
    
    response = stub.UpdateCharacter(server_pb2.UpdateCharacterRequest(auth_id_token=global_token, character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'Modified name!'
    assert response.equipment[0].name == 'Modified name!'
    assert response.equipment[0].value == 99

    compareCharacters(_char, response)