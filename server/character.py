import calendar
import datetime
import logging
import uuid

from sqlalchemy import and_, desc, Enum, exc

import database.db as db
import firebase
import log
import server_pb2
import server_pb2_grpc


class Character(server_pb2_grpc.CharactersManagerServicer):
    conn = None
    logger = logging.getLogger("cos301-DND")

    def _connectDatabase(self):
        if not self.conn:
            self.conn = db.connect()
        return self.conn

    # Converts a Database Character object to a grpc Character object
    def _convertToGrpcCharacter(self, character, status):
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

        charObj.saving_throws.strength = character.saving_throws.strength
        charObj.saving_throws.strength_proficient = character.saving_throws.strength_proficient
        charObj.saving_throws.dexterity = character.saving_throws.dexterity
        charObj.saving_throws.dexterity_proficient = character.saving_throws.dexterity_proficient
        charObj.saving_throws.constitution = character.saving_throws.constitution
        charObj.saving_throws.constitution = character.saving_throws.constitution_proficient
        charObj.saving_throws.intelligence = character.saving_throws.intelligence
        charObj.saving_throws.intelligence_proficient = character.saving_throws.intelligence_proficient
        charObj.saving_throws.wisdom = character.saving_throws.wisdom
        charObj.saving_throws.wisdom_proficient = character.saving_throws.wisdom_proficient
        charObj.saving_throws.charisma = character.saving_throws.charisma
        charObj.saving_throws.charisma_subscript = character.saving_throws.charisma_subscript

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
        charObj.skills.intimidation = character.skills.intimidation
        charObj.skills.intimidation_proficient = character.skills.investigation_proficient
        charObj.skills.medicine = character.skills.medicine
        charObj.skills.medicine_proficient = character.skills.medicine_proficient
        charObj.skills.nature = character.skills.nature
        charObj.skills.nature_proficient = character.skills.nature_proficient
        charObj.skills.perception = character.skills.perception
        charObj.skills.perception_proficient = character.skills.persuasion_proficient
        charObj.skills.performance = character.skills.performance
        charObj.skills.performance_proficient = character.skills.performance_proficient
        charObj.skills.religion = character.skills.religion
        charObj.skills.sleight_of_hand = character.skills.sleight_of_hand
        charObj.skills.sleight_of_hand_proficient = character.skills.sleight_of_hand_proficient
        charObj.skills.stealth = character.skills.stealth
        charObj.skills.stealth_proficient = character.skills.stealth_proficient
        charObj.skills.survival = character.skills.survival
        charObj.skills.survival_proficient = character.skills.survival_proficient

        charObj.status = status

        return charObj

    def GetCharacters(self, request, context):
        self.logger.debug(context.peer())
        self.logger.info("Get characters called!")

        _auth_id_token = request.auth_id_token
        _limit = request.limit

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.error("Failed to verify login!")
            return server_pb2.GetCharactersReply(
                status="FAILED",
                status_message="[GetCharacters] Failed to verify user token!")

        self._connectDatabase()
        user = self.conn.query(db.User).filter(db.User.uid == uid).first()
        if not user:
            user = db.User(uid=uid, name=firebase.auth.get_user(uid).email)
            self.conn.add(user)
            self.conn.commit()

        self.logger.debug("Successfully verified token! UID=" + uid)

        # TODO: Implement limiting
        try:
            self._connectDatabase()

            _characters_query = user.characters
            _characters = []

            for _character in _characters_query:
                charObj = self._convertToGrpcCharacter(_character, status="SUCCESS")
                _characters.append(charObj)

            return server_pb2.GetCharactersReply(status="SUCCESS", characters=_characters)
        except exc.SQLAlchemyError:
            self.logger.error("[GetCharacters] SQLAlchemyError!")
            return server_pb2.GetCharactersReply(
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    def DeleteCharacter(self, request, context):
        self.logger.debug(context.peer())
        self.logger.info("Delete character called!")

        _auth_id_token = request.auth_id_token
        _character_id = request.character_id

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.error("Failed to verify login!")
            return server_pb2.DeleteCharacterReply(
                status="FAILED",
                status_message="[Delete Character] Failed to verify login!")

        self._connectDatabase()
        user = self.conn.query(db.User).filter(db.User.uid == uid).first()
        if not user:
            user = db.User(uid=uid, name=firebase.auth.get_user(uid).email)
            self.conn.add(user)
            self.conn.commit()

        self.logger.debug("Successfully verified token! UID=" + uid)

        # Check if the character is owned by the user.
        character = self.conn.query(db.Character).filter(db.Character.character_id == _character_id).first()
        if not character:
            self.logger.error("Character doesn't exist!")
            return server_pb2.DeleteCharacterReply(
                status="FAILED",
                status_message="[Delete Character] Character doesn't exist!")

        if character.creator.uid != uid:
            # Not the creator.
            self.logger.error("Character is not yours!")
            return server_pb2.DeleteCharacterReply(
                status="FAILED",
                status_message="[Delete Character] Character is not yours!")

        # Else continue deleting

        self.conn.delete(character)
        self.conn.commit()

        self.logger.debug("Successfully deleted character!")

        return server_pb2.DeleteCharacterReply(
                status="SUCCESS",
                status_message="[Delete Character] Successfully deleted character!")

    def GetCharacterById(self, request, context):
        self.logger.debug(context.peer())
        self.logger.info("GetCharacterById called!")
        _auth_id_token = request.auth_id_token

        _character_id = request.character_id

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.error("Failed to verify login!")
            return server_pb2.Character(
                status="FAILED",
                status_message="[Delete Character] Failed to verify login!")

        self._connectDatabase()
        user = self.conn.query(db.User).filter(db.User.uid == uid).first()
        if not user:
            user = db.User(uid=uid, name=firebase.auth.get_user(uid).email)
            self.conn.add(user)
            self.conn.commit()

        self.logger.debug("Successfully verified token! UID=" + uid)

        # Check if the user owns the character
        character = self.conn.query(db.Character).filter(db.Character.character_id == _character_id).first()
        if not character:
            self.logger.error("Character doesn't exist!")
            return server_pb2.Character(
                status="FAILED",
                status_message="[GetCharacterById] Character doesn't exist!")

        if character.creator.uid != uid:
            # Not the creator.
            self.logger.error("Character is not yours!")
            return server_pb2.Character(
                status="FAILED",
                status_message="[GetCharacterById] Character doesn't exist!")

        # Else return the character
        return self._convertToGrpcCharacter(character=character, status="SUCCESS")

    def CreateCharacter(self, request, context):
        self.logger.debug(context.peer())
        self.logger.info("Create new character called!")

        _character_id = str(uuid.uuid4())
        _auth_id_token = request.auth_id_token

        _date_created = datetime.datetime.utcnow()

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.error("Failed to verify login!")
            return server_pb2.Character(
                name="NULL",
                status="FAILED",
                status_message="[Create] Failed to verify user token!")

        self._connectDatabase()
        user = self.conn.query(db.User).filter(db.User.uid == uid).first()
        if not user:
            user = db.User(uid=uid, name=firebase.auth.get_user(uid).email)
            self.conn.add(user)
            self.conn.commit()

        # Check how many characters the user has.
        if len(user.characters) >= 100:
            self.logger.error(
                "Failed to create new character, user has reached max characters")

            return server_pb2.Character(
                status="FAILED",
                status_message="[CreateChar] User has too many characters already!")

        #
        _creator = server_pb2.User()
        _creator.name = user.name
        _creator.uid = user.uid
        _name = request.character.name
        _strength = request.character.strength
        _strength_subscript = request.character.strength_subscript
        _dexterity = request.character.dexterity
        _dexterity_subscript = request.character.dexterity_subscript
        _constitution = request.character.constitution
        _constitution_subscript = request.character.constitution_subscript
        _intelligence = request.character.intelligence
        _intelligence_subscript = request.character.intelligence_subscript
        _wisdom = request.character.wisdom
        _wisdom_subscript = request.character.wisdom_subscript
        _charisma = request.character.charisma
        _charisma_subscript = request.character.charisma_subscript
        _character_class = request.character.character_class
        _race = request.character.race
        _xp = request.character.xp
        _alignment = request.character.alignment
        _background = request.character.background
        _inspiration = request.character.inspiration
        _proficiency_bonus = request.character.proficiency_bonus

        _saving_throws = server_pb2.SavingThrows()
        _saving_throws.strength = request.character.saving_throws.strength
        _saving_throws.strength_proficient = request.character.saving_throws.strength_proficient
        _saving_throws.dexterity = request.character.saving_throws.dexterity
        _saving_throws.dexterity_proficient = request.character.saving_throws.dexterity_proficient
        _saving_throws.constitution = request.character.saving_throws.constitution
        _saving_throws.constitution_proficient = request.character.saving_throws.constitution_proficient
        _saving_throws.intelligence = request.character.saving_throws.intelligence
        _saving_throws.intelligence_proficient = request.character.saving_throws.intelligence_proficient
        _saving_throws.wisdom = request.character.saving_throws.wisdom
        _saving_throws.wisdom_proficient = request.character.saving_throws.wisdom_proficient
        _saving_throws.charisma = request.character.saving_throws.charisma
        _saving_throws.charisma_subscript = request.character.saving_throws.charisma_subscript

        saving_throws_db = db.SavingThrow(
            strength=_saving_throws.strength,
            strength_proficient=_saving_throws.strength_proficient,
            dexterity=_saving_throws.dexterity,
            dexterity_proficient=_saving_throws.dexterity_proficient,
            constitution=_saving_throws.constitution,
            constitution_proficient=_saving_throws.constitution_proficient,
            intelligence=_saving_throws.intelligence,
            intelligence_proficient=_saving_throws.intelligence_proficient,
            wisdom=_saving_throws.wisdom,
            wisdom_proficient=_saving_throws.wisdom_proficient,
            charisma=_saving_throws.charisma,
            charisma_subscript=_saving_throws.charisma_subscript
            )

        _skills = server_pb2.Skills()
        _skills.acrobatics = request.character.skills.acrobatics
        _skills.acrobatics_proficient = request.character.skills.acrobatics_proficient
        _skills.animal_handling = request.character.skills.animal_handling
        _skills.animal_handling_proficient = request.character.skills.animal_handling_proficient
        _skills.arcana = request.character.skills.arcana
        _skills.arcana_proficient = request.character.skills.arcana_proficient
        _skills.athletics = request.character.skills.athletics
        _skills.athletics_proficient = request.character.skills.athletics_proficient
        _skills.deception = request.character.skills.deception
        _skills.deception_proficient = request.character.skills.deception_proficient
        _skills.history = request.character.skills.history
        _skills.history_proficient = request.character.skills.history_proficient
        _skills.insight = request.character.skills.insight
        _skills.insight_proficient = request.character.skills.insight_proficient
        _skills.intimidation = request.character.skills.intimidation
        _skills.intimidation_proficient = request.character.skills.intimidation_proficient
        _skills.investigation = request.character.skills.investigation
        _skills.investigation_proficient = request.character.skills.investigation_proficient
        _skills.medicine = request.character.skills.medicine
        _skills.medicine_proficient = request.character.skills.medicine_proficient
        _skills.nature = request.character.skills.nature
        _skills.nature_proficient = request.character.skills.nature_proficient
        _skills.perception = request.character.skills.perception
        _skills.perception_proficient = request.character.skills.perception_proficient
        _skills.performance = request.character.skills.performance
        _skills.performance_proficient = request.character.skills.performance_proficient
        _skills.persuasion = request.character.skills.persuasion
        _skills.persuasion_proficient = request.character.skills.persuasion_proficient
        _skills.religion = request.character.skills.religion
        _skills.religion_proficient = request.character.skills.religion_proficient
        _skills.sleight_of_hand = request.character.skills.sleight_of_hand
        _skills.sleight_of_hand_proficient = request.character.skills.sleight_of_hand_proficient
        _skills.stealth = request.character.skills.stealth
        _skills.stealth_proficient = request.character.skills.stealth_proficient
        _skills.survival = request.character.skills.survival
        _skills.survival_proficient = request.character.skills.survival_proficient

        skills_db = db.Skill(
            acrobatics=_skills.acrobatics,
            acrobatics_proficient=_skills.acrobatics_proficient,
            animal_handling=_skills.animal_handling,
            animal_handling_proficient=_skills.animal_handling_proficient,
            arcana=_skills.arcana,
            arcana_proficient=_skills.arcana_proficient,
            athletics=_skills.athletics,
            athletics_proficient=_skills.athletics_proficient,
            deception=_skills.deception,
            deception_proficient=_skills.deception_proficient,
            history=_skills.history,
            history_proficient=_skills.history_proficient,
            insight=_skills.insight,
            insight_proficient=_skills.insight_proficient,
            intimidation=_skills.intimidation,
            intimidation_proficient=_skills.intimidation_proficient,
            investigation=_skills.investigation,
            investigation_proficient=_skills.investigation_proficient,
            medicine=_skills.medicine,
            medicine_proficient=_skills.medicine_proficient,
            nature=_skills.nature,
            nature_proficient=_skills.nature_proficient,
            perception=_skills.perception,
            perception_proficient=_skills.persuasion_proficient,
            performance=_skills.performance,
            performance_proficient=_skills.performance_proficient,
            persuasion=_skills.persuasion,
            persuasion_proficient=_skills.persuasion_proficient,
            religion=_skills.religion,
            sleight_of_hand=_skills.sleight_of_hand,
            sleight_of_hand_proficient=_skills.sleight_of_hand_proficient,
            stealth=_skills.stealth,
            stealth_proficient=_skills.stealth_proficient,
            survival=_skills.survival,
            survival_proficient=_skills.survival_proficient
        )

        character = db.Character(
            character_id=_character_id,
            name=_name,
            creator=user,
            strength=_strength,
            strength_subscript=_strength_subscript,
            dexterity=_dexterity,
            dexterity_subscript=_dexterity_subscript,
            constitution=_constitution,
            constitution_subscript=_constitution_subscript,
            intelligence=_intelligence,
            intelligence_subscript=_intelligence_subscript,
            wisdom=_wisdom,
            wisdom_subscript=_wisdom_subscript,
            charisma=_charisma,
            charisma_subscript=_charisma_subscript,
            character_class=_character_class,
            race=_race,
            xp=_xp,
            alignment=_alignment,
            background=_background,
            inspiration=_inspiration,
            proficiency_bonus=_proficiency_bonus,
            skills=skills_db,
            saving_throws=saving_throws_db
            )

        self.conn.add(character)
        self.conn.commit()

        grpcSession = self._convertToGrpcCharacter(character, "SUCCESS")

        return grpcSession
