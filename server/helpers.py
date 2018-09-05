import datetime

from . import db
from . import firebase
from . import server_pb2


def _conecterToORMCharacter(character, request, conn):
    character.character_id = request.character_id
    character.name = request.name
    character.strength = request.strength
    character.strength_subscript = request.strength_subscript
    character.dexterity = request.dexterity
    character.dexterity_subscript = request.dexterity_subscript
    character.constitution = request.constitution
    character.constitution_subscript = request.constitution_subscript
    character.intelligence = request.intelligence
    character.intelligence_subscript = request.intelligence_subscript
    character.wisdom = request.wisdom
    character.wisdom_subscript = request.wisdom_subscript
    character.charisma = request.charisma
    character.charisma_subscript = request.charisma_subscript
    character.character_class = request.character_class
    character.race = request.race
    character.xp = request.xp
    character.alignment = request.alignment
    character.background = request.background
    character.inspiration = request.inspiration
    character.proficiency_bonus = request.proficiency_bonus

    # character.session_id = request.session_id
    character.features_and_traits = request.features_and_traits

    character.gender = request.gender
    character.level = request.level

    character.skills.acrobatics = request.skills.acrobatics
    character.skills.acrobatics_proficient = request.skills.acrobatics_proficient
    character.skills.animal_handling = request.skills.animal_handling
    character.skills.animal_handling_proficient = request.skills.animal_handling_proficient
    character.skills.arcana = request.skills.arcana
    character.skills.arcana_proficient = request.skills.arcana_proficient
    character.skills.athletics = request.skills.athletics
    character.skills.athletics_proficient = request.skills.athletics_proficient
    character.skills.deception = request.skills.deception
    character.skills.deception_proficient = request.skills.deception_proficient
    character.skills.history = request.skills.history
    character.skills.history_proficient = request.skills.history_proficient
    character.skills.insight = request.skills.insight
    character.skills.insight_proficient = request.skills.insight_proficient
    character.skills.intimidation = request.skills.intimidation
    character.skills.intimidation_proficient = request.skills.intimidation_proficient
    character.skills.investigation = request.skills.investigation
    character.skills.investigation_proficient = request.skills.investigation_proficient
    character.skills.medicine = request.skills.medicine
    character.skills.medicine_proficient = request.skills.medicine_proficient
    character.skills.nature = request.skills.nature
    character.skills.nature_proficient = request.skills.nature_proficient
    character.skills.perception = request.skills.perception
    character.skills.perception_proficient = request.skills.perception_proficient
    character.skills.performance = request.skills.performance
    character.skills.performance_proficient = request.skills.performance_proficient
    character.skills.persuasion = request.skills.persuasion
    character.skills.persuasion_proficient = request.skills.persuasion_proficient
    character.skills.religion = request.skills.religion
    character.skills.religion_proficient = request.skills.religion_proficient
    character.skills.sleight_of_hand = request.skills.sleight_of_hand
    character.skills.sleight_of_hand_proficient = request.skills.sleight_of_hand_proficient
    character.skills.stealth = request.skills.stealth
    character.skills.stealth_proficient = request.skills.stealth_proficient
    character.skills.survival = request.skills.survival
    character.skills.survival_proficient = request.skills.survival_proficient

    character.hitpoints.armor_class = request.hitpoints.armor_class
    character.hitpoints.current_hitpoints = request.hitpoints.current_hitpoints
    character.hitpoints.max_hitpoints = request.hitpoints.max_hitpoints
    character.hitpoints.temporary_hitpoints = request.hitpoints.temporary_hitpoints
    character.hitpoints.hitdice = request.hitpoints.hitdice

    character.passive_wisdom = request.passive_wisdom
    character.personality_traits = request.personality_traits
    character.ideals = request.ideals
    character.bonds = request.bonds
    character.flaws = request.flaws

    for equipment in character.equipment:
        conn.delete(equipment)

    # Equipment
    for equipment in request.equipment:
        _eq = db.Equipment(
            character_id=character.character_id,
            name=equipment.name,
            value=equipment.value
        )
        character.equipment.append(_eq)


# Converts a Database Character object to a grpc Character object
def _convertToGrpcCharacter(character, status):
    charObj = server_pb2.Character()
    charObj.creator.name = character.creator.name
    charObj.creator.uid = character.creator.uid

    charObj.character_id = character.character_id
    charObj.name = character.name
    charObj.strength = character.strength
    charObj.strength_subscript = character.strength_subscript
    charObj.dexterity = character.dexterity
    charObj.dexterity_subscript = character.dexterity_subscript
    charObj.constitution = character.constitution
    charObj.constitution_subscript = character.constitution_subscript
    charObj.intelligence = character.intelligence
    charObj.intelligence_subscript = character.intelligence_subscript
    charObj.wisdom = character.wisdom
    charObj.wisdom_subscript = character.wisdom_subscript
    charObj.charisma = character.charisma
    charObj.charisma_subscript = character.charisma_subscript
    charObj.character_class = character.character_class
    charObj.race = character.race
    charObj.xp = character.xp
    charObj.alignment = character.alignment
    charObj.background = character.background
    charObj.inspiration = character.inspiration
    charObj.proficiency_bonus = character.proficiency_bonus

    if character.session:
        charObj.session_id = character.session.session_id

    charObj.features_and_traits = character.features_and_traits

    charObj.gender = character.gender
    charObj.level = character.level

    charObj.last_updated = str(character.date_updated)

    charObj.skills.acrobatics = character.skills.acrobatics
    charObj.skills.acrobatics_proficient = character.skills.acrobatics_proficient
    charObj.skills.animal_handling = character.skills.animal_handling
    charObj.skills.animal_handling_proficient = character.skills.animal_handling_proficient
    charObj.skills.arcana = character.skills.arcana
    charObj.skills.arcana_proficient = character.skills.arcana_proficient
    charObj.skills.athletics = character.skills.athletics
    charObj.skills.athletics_proficient = character.skills.athletics_proficient
    charObj.skills.deception = character.skills.deception
    charObj.skills.deception_proficient = character.skills.deception_proficient
    charObj.skills.history = character.skills.history
    charObj.skills.history_proficient = character.skills.history_proficient
    charObj.skills.insight = character.skills.insight
    charObj.skills.insight_proficient = character.skills.insight_proficient
    charObj.skills.investigation = character.skills.investigation
    charObj.skills.investigation_proficient = character.skills.investigation_proficient
    charObj.skills.intimidation = character.skills.intimidation
    charObj.skills.intimidation_proficient = character.skills.intimidation_proficient
    charObj.skills.medicine = character.skills.medicine
    charObj.skills.medicine_proficient = character.skills.medicine_proficient
    charObj.skills.nature = character.skills.nature
    charObj.skills.nature_proficient = character.skills.nature_proficient
    charObj.skills.persuasion = character.skills.persuasion
    charObj.skills.persuasion_proficient = character.skills.persuasion_proficient
    charObj.skills.perception = character.skills.perception
    charObj.skills.perception_proficient = character.skills.perception_proficient
    charObj.skills.performance = character.skills.performance
    charObj.skills.performance_proficient = character.skills.performance_proficient
    charObj.skills.religion = character.skills.religion
    charObj.skills.religion_proficient = character.skills.religion_proficient
    charObj.skills.sleight_of_hand = character.skills.sleight_of_hand
    charObj.skills.sleight_of_hand_proficient = character.skills.sleight_of_hand_proficient
    charObj.skills.stealth = character.skills.stealth
    charObj.skills.stealth_proficient = character.skills.stealth_proficient
    charObj.skills.survival = character.skills.survival
    charObj.skills.survival_proficient = character.skills.survival_proficient

    charObj.hitpoints.armor_class = character.hitpoints.armor_class
    charObj.hitpoints.current_hitpoints = character.hitpoints.current_hitpoints
    charObj.hitpoints.max_hitpoints = character.hitpoints.max_hitpoints
    charObj.hitpoints.temporary_hitpoints = character.hitpoints.temporary_hitpoints
    charObj.hitpoints.hitdice = character.hitpoints.hitdice

    charObj.passive_wisdom = character.passive_wisdom
    charObj.personality_traits = character.personality_traits
    charObj.ideals = character.ideals
    charObj.bonds = character.bonds
    charObj.flaws = character.flaws

    charObj.equipment.extend([])

    for eq in character.equipment:
        _eq = server_pb2.Equipment()
        _eq.name = eq.name
        _eq.value = eq.value
        charObj.equipment.extend([_eq])

    charObj.status = status

    return charObj


def _convertToGrpcLightCharacter(character):
    charObj = server_pb2.LightCharacter()
    charObj.creator_id = character.creator.uid

    charObj.character_id = character.character_id

    charObj.name = character.name
    charObj.character_class = character.character_class
    charObj.race = character.race
    charObj.xp = character.xp

    if character.session:
        charObj.session_id = character.session.session_id

    charObj.gender = character.gender

    charObj.hitpoints.armor_class = character.hitpoints.armor_class
    charObj.hitpoints.current_hitpoints = character.hitpoints.current_hitpoints
    charObj.hitpoints.max_hitpoints = character.hitpoints.max_hitpoints
    charObj.hitpoints.temporary_hitpoints = character.hitpoints.temporary_hitpoints
    charObj.hitpoints.hitdice = character.hitpoints.hitdice

    charObj.last_updated = str(character.date_updated)

    return charObj


def goOnline(conn, uid, ip):
    user = conn.query(db.User).filter(db.User.uid == uid).first()
    if not user:
        user = db.User(uid=uid, name=firebase.auth.get_user(uid).email, online=True, ip=str(ip))
        conn.add(user)

    user.online = True
    user.ip = ip
    user.date_updated = datetime.datetime.now()
    conn.commit()
    return user
