from __future__ import print_function

import random
import subprocess

import firebase_admin
import grpc
import server_pb2
import server_pb2_grpc
from firebase_admin import credentials

cred = credentials.Certificate(
    "dnd-game-manager-firebase-adminsdk-34ek4-cccabd3dd6.json")
firebase = firebase_admin.initialize_app(cred)

server = 'localhost:50051'
# server = 'develop.optimizeprime.co.za:50051'
test_session_id = ''
uid = 'mT8HzwXWjDc1FX472qTfcsUUcQt1'


def getRandomCharacter():
    _character = server_pb2.Character()
    _character.name = "MyTestCharacter"

    _character.gender = "Male"
    _character.level = 34

    _character.strength = random.randint(1, 50)
    _character.strength_subscript = random.randint(1, 50)
    _character.dexterity = random.randint(1, 50)
    _character.dexterity_subscript = random.randint(1, 50)
    _character.constitution = random.randint(1, 50)
    _character.constitution_subscript = random.randint(1, 50)
    _character.intelligence = random.randint(1, 50)
    _character.intelligence_subscript = random.randint(1, 50)
    _character.wisdom = random.randint(1, 50)
    _character.wisdom_subscript = random.randint(1, 50)
    _character.charisma = random.randint(1, 50)
    _character.charisma_subscript = random.randint(1, 50)
    _character.character_class = "TEST CLASS"
    _character.race = "TEST RACE"
    _character.xp = random.randint(1, 50)
    _character.alignment = "TEST ALIGNMENT"
    _character.background = "TEST BACKGROUND"
    _character.inspiration = random.randint(1, 50)
    _character.proficiency_bonus = random.randint(1, 50)

    _character.passive_wisdom = random.randint(1, 50)
    _character.personality_traits = "TEST PERSONALITY TRAITS"
    _character.ideals = "TEST IDEALS"
    _character.bonds = "TEST BONDS"
    _character.flaws = "TEST FLAWS"

    _character.skills.acrobatics = random.randint(1, 50)
    _character.skills.acrobatics_proficient = random.choice([True, False])
    _character.skills.animal_handling = random.randint(1, 50)
    _character.skills.animal_handling_proficient = random.choice([True, False])
    _character.skills.arcana = random.randint(1, 50)
    _character.skills.arcana_proficient = random.choice([True, False])
    _character.skills.athletics = random.randint(1, 50)
    _character.skills.athletics_proficient = random.choice([True, False])
    _character.skills.deception = random.randint(1, 50)
    _character.skills.deception_proficient = random.choice([True, False])
    _character.skills.history = random.randint(1, 50)
    _character.skills.history_proficient = random.choice([True, False])
    _character.skills.insight = random.randint(1, 50)
    _character.skills.insight_proficient = random.choice([True, False])
    _character.skills.intimidation = random.randint(1, 50)
    _character.skills.intimidation_proficient = random.choice([True, False])
    _character.skills.investigation = random.randint(1, 50)
    _character.skills.investigation_proficient = random.choice([True, False])
    _character.skills.medicine = random.randint(1, 50)
    _character.skills.medicine_proficient = random.choice([True, False])
    _character.skills.nature = random.randint(1, 50)
    _character.skills.nature_proficient = random.choice([True, False])
    _character.skills.perception = random.randint(1, 50)
    _character.skills.perception_proficient = random.choice([True, False])
    _character.skills.performance = random.randint(1, 50)
    _character.skills.performance_proficient = random.choice([True, False])
    _character.skills.persuasion = random.randint(1, 50)
    _character.skills.persuasion_proficient = random.choice([True, False])
    _character.skills.religion = random.randint(1, 50)
    _character.skills.religion_proficient = random.choice([True, False])
    _character.skills.sleight_of_hand = random.randint(1, 50)
    _character.skills.sleight_of_hand_proficient = random.choice([True, False])
    _character.skills.stealth = random.randint(1, 50)
    _character.skills.stealth_proficient = random.choice([True, False])
    _character.skills.survival = random.randint(1, 50)
    _character.skills.survival_proficient = random.choice([True, False])

    _character.hitpoints.armor_class = random.randint(1, 50)
    _character.hitpoints.current_hitpoints = random.randint(1, 50)
    _character.hitpoints.max_hitpoints = random.randint(1, 50)
    _character.hitpoints.temporary_hitpoints = random.randint(1, 50)
    _character.hitpoints.hitdice = "HIT DICE"

    _character.equipment.extend([])

    _eq = server_pb2.Equipment()
    _eq.name = "TEST EQ"
    _eq.value = random.randint(1, 50)
    _eq2 = server_pb2.Equipment()
    _eq2.name = "TEST EQ"
    _eq2.value = random.randint(1, 50)

    _character.equipment.extend([_eq])
    _character.equipment.extend([_eq2])

    _character.features_and_traits = 'FEATURESANDTRAITS'

    return _character


def compareCharacters(character1, character2):
    # assert character1.character_id == character2.character_id

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

    assert character1.gender == character2.gender
    assert character1.level == character2.level

    assert character1.passive_wisdom == character2.passive_wisdom
    assert character1.personality_traits == character2.personality_traits
    assert character1.ideals == character2.ideals
    assert character1.bonds == character2.bonds
    assert character1.flaws == character2.flaws

    assert character1.hitpoints.armor_class == character2.hitpoints.armor_class
    assert character1.hitpoints.current_hitpoints == character2.hitpoints.current_hitpoints
    assert character1.hitpoints.max_hitpoints == character2.hitpoints.max_hitpoints
    assert character1.hitpoints.temporary_hitpoints == character2.hitpoints.temporary_hitpoints
    assert character1.hitpoints.hitdice == character2.hitpoints.hitdice

    assert character1.skills.acrobatics == character2.skills.acrobatics
    assert character1.skills.acrobatics_proficient == character2.skills.acrobatics_proficient
    assert character1.skills.animal_handling == character2.skills.animal_handling
    assert character1.skills.animal_handling_proficient == character2.skills.animal_handling_proficient
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

    # assert character1.session_id == character2.session_id

    assert character1.features_and_traits == character2.features_and_traits


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


def test_create_character():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'
    _char.skills.acrobatics = 5

    response = stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1,
            character=_char))
    assert response.status == 'SUCCESS'

    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.skills.acrobatics == 5

    compareCharacters(_char, response)


# Will however test for empty name
def test_create_character_empty_name():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = server_pb2.Character()
    _char.name = ""

    response = stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1,
            character=_char))
    assert response.status == 'FAILED'
    assert response.status_message == '[CreateChar] Character name may not be blank!'


def test_get_characters():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    response = stub.GetCharacters(
        server_pb2.GetCharactersRequest(
            auth_id_token=token1))

    assert response.status == 'SUCCESS'
    assert response.status_message == ''
    assert len(response.light_characters) > 0
    assert response.light_characters[0].name == 'MyTestCharacter'


def test_delete_character_does_not_exist():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)
    response = stub.DeleteCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1,
            character=None))

    assert response.status == 'FAILED'
    assert response.status_message == '[Delete Character] Character doesn\'t exist!'


def test_delete_character_that_not_ours():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    character = stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1, character=_char))
    assert character.status == "SUCCESS"

    response = stub.DeleteCharacter(
        server_pb2.DeleteCharacterRequest(
            auth_id_token=token2,
            character_id=character.character_id))

    assert response.status == "FAILED"
    assert response.status_message == "[Delete Character] Character is not yours!"


def test_delete_character():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'

    _char = response

    # Delete
    response = stub.DeleteCharacter(
        server_pb2.DeleteCharacterRequest(
            auth_id_token=token1,
            character_id=_char.character_id))

    assert response.status == "SUCCESS"


def test_get_character_by_id():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'

    _char_id = response.character_id

    response = stub.GetCharacterById(
        server_pb2.GetCharacterByIdRequest(
            auth_id_token=token1,
            character_id=_char_id))
    assert response.status == 'SUCCESS'
    assert response.character_id == _char_id
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'


def test_get_character_by_id_user_should_not_have_access():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'

    _char_id = response.character_id

    response = stub.GetCharacterById(
        server_pb2.GetCharacterByIdRequest(
            auth_id_token=token3,
            character_id=_char_id))
    assert response.status == 'FAILED'
    assert response.status_message == '[GetCharacterById] Character is not yours!'


def test_update_character():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.level == 34
    assert response.gender == "Male"

    _char = getRandomCharacter()
    _char.character_id = response.character_id
    _char.name = 'Modified name!'
    _char.equipment[0].name = "Modified name!"
    _char.equipment[0].value = 99
    _char.level = 100
    _char.gender = "Female"

    response = stub.UpdateCharacter(
        server_pb2.UpdateCharacterRequest(
            auth_id_token=token1,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'Modified name!'
    assert response.equipment[0].name == 'Modified name!'
    assert response.equipment[0].value == 99
    assert response.level == 100
    assert response.gender == "Female"

    compareCharacters(_char, response)


def test_character_added_to_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.level == 34
    assert response.gender == "Male"

    char_id = response.character_id

    session_stub = server_pb2_grpc.SessionsManagerStub(channel)

    response = session_stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=7))

    assert response.name == 'mysession'
    assert len(response.session_id) == 36
    assert response.status == 'SUCCESS'

    session_last_updated = response.last_updated
    assert len(session_last_updated) > 0

    sesh_id = response.session_id

    response = session_stub.AddCharacterToSession(
        server_pb2.AddCharacterToSessionRequest(auth_id_token=token1, session_id=sesh_id, character_id=char_id))
    assert response.status == 'SUCCESS'
    assert response.last_updated != session_last_updated
    session_last_updated = response.last_updated

    response = session_stub.GetCharactersInSession(
        server_pb2.AddCharacterToSessionRequest(auth_id_token=token1, session_id=sesh_id))
    assert response.status == 'SUCCESS'

    assert len(response.light_characters) == 1

    # Test remove
    response = session_stub.RemoveCharacterFromSession(
        server_pb2.AddCharacterToSessionRequest(auth_id_token=token1, session_id=sesh_id, character_id=char_id))
    assert response.status == 'SUCCESS'
    assert response.last_updated != session_last_updated

    response = session_stub.GetCharactersInSession(
        server_pb2.AddCharacterToSessionRequest(auth_id_token=token1, session_id=sesh_id))
    assert response.status == 'SUCCESS'

    assert len(response.light_characters) == 0


def test_character_added_to_session_already_in():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.level == 34
    assert response.gender == "Male"

    char_id = response.character_id

    session_stub = server_pb2_grpc.SessionsManagerStub(channel)

    response = session_stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=7))

    assert response.name == 'mysession'
    assert len(response.session_id) == 36
    assert response.status == 'SUCCESS'

    sesh_id = response.session_id

    response = session_stub.AddCharacterToSession(
        server_pb2.AddCharacterToSessionRequest(auth_id_token=token1, session_id=sesh_id, character_id=char_id))
    assert response.status == 'SUCCESS'

    response = session_stub.AddCharacterToSession(
        server_pb2.AddCharacterToSessionRequest(auth_id_token=token1, session_id=sesh_id, character_id=char_id))
    assert response.status == 'FAILED'

    response = session_stub.GetCharactersInSession(
        server_pb2.AddCharacterToSessionRequest(auth_id_token=token1, session_id=sesh_id))
    assert response.status == 'SUCCESS'

    # Since we added the same character the number should remain the same.
    assert len(response.light_characters) == 1


def test_character_deleted_should_not_be_in_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.level == 34
    assert response.gender == "Male"

    char_id = response.character_id

    session_stub = server_pb2_grpc.SessionsManagerStub(channel)

    response = session_stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=7))

    assert response.name == 'mysession'
    assert len(response.session_id) == 36
    assert response.status == 'SUCCESS'

    sesh_id = response.session_id

    response = session_stub.AddCharacterToSession(
        server_pb2.AddCharacterToSessionRequest(auth_id_token=token1, session_id=sesh_id, character_id=char_id))
    assert response.status == 'SUCCESS'

    response = stub.DeleteCharacter(
        server_pb2.DeleteCharacterRequest(
            auth_id_token=token1,
            character_id=char_id))
    assert response.status == 'SUCCESS'

    response = session_stub.GetCharactersInSession(
        server_pb2.AddCharacterToSessionRequest(auth_id_token=token1, session_id=sesh_id))
    assert response.status == 'SUCCESS'

    # Since we deleted the character that character should no longer show.
    assert len(response.light_characters) == 0


def test_remove_character_that_is_not_ours():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.level == 34
    assert response.gender == "Male"

    char_id = response.character_id

    session_stub = server_pb2_grpc.SessionsManagerStub(channel)

    response = session_stub.Create(
        server_pb2.NewSessionRequest(
            name='mysession',
            auth_id_token=token1,
            max_players=7))

    assert response.name == 'mysession'
    assert len(response.session_id) == 36
    assert response.status == 'SUCCESS'

    sesh_id = response.session_id

    response = session_stub.AddCharacterToSession(
        server_pb2.AddCharacterToSessionRequest(auth_id_token=token1, session_id=sesh_id, character_id=char_id))
    assert response.status == 'SUCCESS'

    # Test remove as another ueer
    response = session_stub.RemoveCharacterFromSession(
        server_pb2.AddCharacterToSessionRequest(auth_id_token=token3, session_id=sesh_id, character_id=char_id))
    assert response.status == 'FAILED'
    assert response.status_message == '[RemoveCharacterFromSession] Failed to remove character from session, this is not your character'

    response = session_stub.GetCharactersInSession(
        server_pb2.AddCharacterToSessionRequest(auth_id_token=token1, session_id=sesh_id))
    assert response.status == 'SUCCESS'

    assert len(response.light_characters) == 1


# def test_get_all_characters_in_session():

def test_give_xp():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='my session mock4',
            auth_id_token=token4,
            max_players=7))

    assert session.status == 'SUCCESS'

    char_stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = char_stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token4,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser4@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.level == 34
    assert response.gender == "Male"

    previous_xp = response.xp
    _char_id = response.character_id

    # Add char to session
    response = stub.AddCharacterToSession(
        server_pb2.AddCharacterToSessionRequest(
            auth_id_token=token4,
            session_id=session.session_id,
            character_id=_char_id))
    assert response.status == 'SUCCESS'
    session_last_updated = response.last_updated
    assert len(session_last_updated) > 0

    # Give own character xp
    response = stub.GiveXp(
        server_pb2.GiveXpRequest(
            auth_id_token=token4,
            session_id=session.session_id,
            character_id=_char_id,
            xp=100))
    assert response.status == 'SUCCESS'

    # Test server updating
    response = stub.GetLightSessionById(server_pb2.GetSessionRequest(
        auth_id_token=token4,
        session_id=session.session_id,
    ))
    assert response.status == 'SUCCESS'
    assert len(response.last_updated) != session_last_updated

    # Check if character gained xp
    response = char_stub.GetCharacterById(
        server_pb2.GetCharacterByIdRequest(
            auth_id_token=token4,
            character_id=_char_id))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser4@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.level == 34
    assert response.gender == "Male"
    assert response.xp == (previous_xp + 100)
    assert response.character_id == _char_id


def test_give_xp_invalid_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    response = stub.GiveXp(
        server_pb2.GiveXpRequest(
            auth_id_token=token1,
            session_id='',
            character_id='',
            xp=100))
    assert response.status == 'FAILED'
    assert response.status_message == '[GiveXp] No session with that ID exists!'


def test_give_xp_invalid_character():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='my session mock global',
            auth_id_token=token1,
            max_players=7))

    assert session.status == 'SUCCESS'

    response = stub.GiveXp(
        server_pb2.GiveXpRequest(
            auth_id_token=token1,
            session_id=session.session_id,
            character_id='',
            xp=100))
    assert response.status == 'FAILED'
    assert response.status_message == '[GiveXp] No character with that ID exists!'


def test_give_xp_valid_session_valid_character_but_not_in_the_dm_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='my session mock4',
            auth_id_token=token4,
            max_players=7))

    assert session.status == 'SUCCESS'

    char_stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = char_stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token4,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser4@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.level == 34
    assert response.gender == "Male"

    _char_id = response.character_id

    # Give own character xp
    response = stub.GiveXp(
        server_pb2.GiveXpRequest(
            auth_id_token=token4,
            session_id=session.session_id,
            character_id=_char_id,
            xp=100))
    assert response.status == 'FAILED'
    assert response.status_message == '[GiveXp] This character is not in your session!'


def test_distribute_xp():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='my session mock4',
            auth_id_token=token4,
            max_players=7))

    assert session.status == 'SUCCESS'
    session_last_updated = session.last_updated
    assert len(session_last_updated) > 0

    char_stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = char_stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token4,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser4@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.level == 34
    assert response.gender == "Male"

    previous_xp_1 = response.xp
    char_1_id = response.character_id

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = char_stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token3,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser3@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.level == 34
    assert response.gender == "Male"

    previous_xp_2 = response.xp
    char_2_id = response.character_id

    # Add char to session
    response = stub.AddCharacterToSession(
        server_pb2.AddCharacterToSessionRequest(
            auth_id_token=token4,
            session_id=session.session_id,
            character_id=char_1_id))
    assert response.status == 'SUCCESS'
    assert len(response.last_updated) != session_last_updated
    session_last_updated = response.last_updated

    response = stub.AddCharacterToSession(
        server_pb2.AddCharacterToSessionRequest(
            auth_id_token=token3,
            session_id=session.session_id,
            character_id=char_2_id))
    assert response.status == 'SUCCESS'
    assert len(response.last_updated) != session_last_updated

    # Distribute xp
    response = stub.DistributeXp(
        server_pb2.DistributeXpRequest(
            auth_id_token=token4,
            session_id=session.session_id,
            xp=100))
    assert response.status == 'SUCCESS'

    # Check if character gained xp
    response = char_stub.GetCharacterById(
        server_pb2.GetCharacterByIdRequest(
            auth_id_token=token4,
            character_id=char_1_id))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser4@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.level == 34
    assert response.gender == "Male"
    assert response.xp == (previous_xp_1 + 50)
    assert response.character_id == char_1_id

    response = char_stub.GetCharacterById(
        server_pb2.GetCharacterByIdRequest(
            auth_id_token=token3,
            character_id=char_2_id))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser3@test.co.za'
    assert response.name == 'MyTestCharacter'
    assert response.level == 34
    assert response.gender == "Male"
    assert response.xp == (previous_xp_2 + 50)
    assert response.character_id == char_2_id


def test_distribute_xp_invalid_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)
    response = stub.DistributeXp(
        server_pb2.DistributeXpRequest(
            auth_id_token=token1,
            session_id='',
            xp=100))
    assert response.status == 'FAILED'
    assert response.status_message == '[DistributeXp] No session with that ID exists!'


def test_distribute_xp_valid_session_but_not_dm_session():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = stub.Create(
        server_pb2.NewSessionRequest(
            name='my session mock4',
            auth_id_token=token4,
            max_players=7))

    assert session.status == 'SUCCESS'
    session_last_updated = session.last_updated
    assert len(session_last_updated) > 0

    # Give own character xp
    response = stub.DistributeXp(
        server_pb2.DistributeXpRequest(
            auth_id_token=token3,
            session_id=session.session_id,
            xp=100))
    assert response.status == 'FAILED'
    assert response.status_message == "[DistributeXp] You must be the dungeon master to use this command!"


def test_get_character_by_id_dm_should_have_access():
    channel = grpc.insecure_channel(server)
    stub = server_pb2_grpc.CharactersManagerStub(channel)

    _char = getRandomCharacter()
    _char.name = 'MyTestCharacter'

    response = stub.CreateCharacter(
        server_pb2.NewCharacterRequest(
            auth_id_token=token1,
            character=_char))
    assert response.status == 'SUCCESS'
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'

    _char_id = response.character_id

    response = stub.GetCharacterById(
        server_pb2.GetCharacterByIdRequest(
            auth_id_token=token1,
            character_id=_char_id))
    assert response.status == 'SUCCESS'
    assert response.character_id == _char_id
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'

    sess_stub = server_pb2_grpc.SessionsManagerStub(channel)

    session = sess_stub.Create(
        server_pb2.NewSessionRequest(
            name='my session mock4',
            auth_id_token=token4,
            max_players=7))

    assert session.status == 'SUCCESS'
    session_last_updated = session.last_updated
    assert len(session_last_updated) > 0

    # Add char to session
    response = sess_stub.AddCharacterToSession(
        server_pb2.AddCharacterToSessionRequest(
            auth_id_token=token1,
            session_id=session.session_id,
            character_id=_char_id))
    assert response.status == 'SUCCESS'

    # Session should update last updated time
    assert session_last_updated != response.last_updated

    response = stub.GetCharacterById(
        server_pb2.GetCharacterByIdRequest(
            auth_id_token=token4,
            character_id=_char_id))
    assert response.status == 'SUCCESS'
    assert response.character_id == _char_id
    assert response.creator.name == 'mockuser@test.co.za'
    assert response.name == 'MyTestCharacter'
