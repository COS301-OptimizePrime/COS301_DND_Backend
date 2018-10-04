import datetime
import logging
import uuid

from sqlalchemy import exc

from . import db
from . import firebase
from . import helpers
from . import server_pb2
from . import server_pb2_grpc


class CharacterManager(server_pb2_grpc.CharactersManagerServicer):
    conn = None
    logger = logging.getLogger("cos301-DND")
    ip = ""

    def _connectDatabase(self):
        if not self.conn:
            self.conn = db.connect()

        return self.conn

    def UpdateCharacter(self, request, context):
        self.ip = context.peer()
        self.logger.info("UpdateCharacter called!")

        _auth_id_token = request.auth_id_token
        _character = request.character
        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Character(
                status="FAILED",
                status_message="[UpdateCharacter] Failed to verify user token!")

        self.logger.debug("Successfully verified token! UID=" + uid)

        try:
            self.conn = self._connectDatabase()
            # Go Online
            helpers.goOnline(self.conn, uid, self.ip)

            # Check if the user owns the character
            character = self.conn.query(db.Character).filter(
                db.Character.character_id == _character.character_id).first()
            if not character:
                self.logger.warning("Character doesn't exist!")
                return server_pb2.Character(
                    status="FAILED",
                    status_message="[UpdateCharacter] Character doesn't exist!")

            if character.creator.uid != uid:
                # Not the creator.
                self.logger.warning("Character is not yours!")
                return server_pb2.Character(
                    status="FAILED",
                    status_message="[UpdateCharacter] Character doesn't exist!")

            helpers._conecterToORMCharacter(character, _character, self.conn)
            self.conn.commit()

            self.logger.info("Updated character!")

            return helpers._convertToGrpcCharacter(
                character=character, status="SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[UpdateCharacter] SQLAlchemyError!" + str(err))
            return server_pb2.Character(
                status="FAILED",
                status_message="Database error!")
        except Exception:
            self.logger.exception("[UpdateCharacter] Unhandled exception occurred!")
            return server_pb2.Character(
                status="FAILED",
                status_message="[UpdateCharacter] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    # [CHEAP] Using light characters
    def GetCharacters(self, request, context):
        self.ip = context.peer()
        self.logger.info("Get characters called!")

        _auth_id_token = request.auth_id_token
        _limit = request.limit

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.GetCharactersReply(
                status="FAILED",
                status_message="[GetCharacters] Failed to verify user token!")

        self.logger.debug("Successfully verified token! UID=" + uid)

        # TODO: Implement limiting
        try:
            self.conn = self._connectDatabase()
            # Go Online
            user = helpers.goOnline(self.conn, uid, self.ip)

            _characters_query = user.characters
            _characters = []

            for _character in _characters_query:
                charObj = helpers._convertToGrpcLightCharacter(
                    _character)
                _characters.append(charObj)

            return server_pb2.GetCharactersReply(
                status="SUCCESS", light_characters=_characters)
        except exc.SQLAlchemyError as err:
            self.logger.error("[GetCharacters] SQLAlchemyError!" + str(err))
            return server_pb2.GetCharactersReply(
                status="FAILED",
                status_message="Database error!")
        except Exception:
            self.logger.exception("[GetCharacters] Unhandled exception occurred!")
            return server_pb2.GetCharactersReply(
                status="FAILED",
                status_message="[GetCharacters] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def DeleteCharacter(self, request, context):
        self.ip = context.peer()
        self.logger.info("Delete character called!")

        _auth_id_token = request.auth_id_token
        _character_id = request.character_id

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
            self.logger.debug("Successfully verified token! UID=" + uid)
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.DeleteCharacterReply(
                status="FAILED",
                status_message="[Delete Character] Failed to verify login!")

        try:
            self.conn = self._connectDatabase()
            helpers.goOnline(self.conn, uid, self.ip)

            # Check if the character is owned by the user.
            character = self.conn.query(db.Character).filter(
                db.Character.character_id == _character_id).first()
            if not character:
                self.logger.warning("Character doesn't exist!")
                return server_pb2.DeleteCharacterReply(
                    status="FAILED",
                    status_message="[Delete Character] Character doesn't exist!")

            if character.creator.uid != uid:
                # Not the creator.
                self.logger.warning("Character is not yours!")
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

        except exc.SQLAlchemyError as err:
            self.logger.error("[DeleteCharacters] SQLAlchemyError!" + str(err))
            return server_pb2.DeleteCharacterReply(
                status="FAILED",
                status_message="Database error!")
        except Exception:
            self.logger.exception("[DeleteCharacters] Unhandled exception occurred!")
            return server_pb2.DeleteCharacterReply(
                status="FAILED",
                status_message="[DeleteCharacters] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def GetCharacterById(self, request, context):
        self.ip = context.peer()
        self.logger.info("GetCharacterById called!")
        _auth_id_token = request.auth_id_token

        _character_id = request.character_id

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
            self.logger.debug("Successfully verified token! UID=" + uid)
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Character(
                status="FAILED",
                status_message="[Delete Character] Failed to verify login!")

        try:
            self.conn = self._connectDatabase()
            helpers.goOnline(self.conn, uid, self.ip)

            # Check if the user owns the character
            character = self.conn.query(db.Character).filter(
                db.Character.character_id == _character_id).first()
            if not character:
                self.logger.warning("Character doesn't exist!")
                return server_pb2.Character(
                    status="FAILED",
                    status_message="[GetCharacterById] Character doesn't exist!")

            # This allows the DM of the session to get the character.
            # This blocks anyone else.
            if character.session and character.session.dungeon_master.uid == uid:
                self.logger.debug("[GetCharacterById] DM accessed character!")
                return helpers._convertToGrpcCharacter(
                    character=character, status="SUCCESS")
            elif character.creator.uid != uid:
                # Not the creator.
                self.logger.warning("Character is not yours!")
                return server_pb2.Character(
                    status="FAILED",
                    status_message="[GetCharacterById] Character is not yours!")

            # Else return the character
            return helpers._convertToGrpcCharacter(
                character=character, status="SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[GetCharacterById] SQLAlchemyError!" + str(err))
            return server_pb2.Character(
                status="FAILED",
                status_message="Database error!")
        except Exception:
            self.logger.exception("[GetCharacterById] Unhandled exception occurred!")
            return server_pb2.Character(
                status="FAILED",
                status_message="[GetCharacterById] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def CreateCharacter(self, request, context):
        self.ip = context.peer()
        self.logger.info("Create new character called!")

        _character_id = str(uuid.uuid4())
        _auth_id_token = request.auth_id_token

        _date_created = datetime.datetime.utcnow()

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Character(
                name="NULL",
                status="FAILED",
                status_message="[Create] Failed to verify user token!")

        try:
            self.conn = self._connectDatabase()
            user = helpers.goOnline(self.conn, uid, self.ip)

            # Check how many characters the user has.
            if len(user.characters) >= 100:
                self.logger.warning(
                    "Failed to create new character, user has reached max characters")

                return server_pb2.Character(
                    status="FAILED",
                    status_message="[CreateChar] User has too many characters already!")

            # Name may not be blank
            if len(request.character.name.strip()) == 0:
                self.logger.warning(
                    "Failed to create new character, character name can not be blank")
                return server_pb2.Character(
                    status="FAILED",
                    status_message="[CreateChar] Character name may not be blank!")

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

            _passive_wisdom = request.character.passive_wisdom
            _personality_traits = request.character.personality_traits
            _ideals = request.character.ideals
            _bonds = request.character.bonds
            _flaws = request.character.flaws

            # _session_id = request.character.session_id
            _features_and_traits = request.character.features_and_traits

            _gender = request.character.gender
            _level = request.character.level

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
                perception_proficient=_skills.perception_proficient,
                performance=_skills.performance,
                performance_proficient=_skills.performance_proficient,
                persuasion=_skills.persuasion,
                persuasion_proficient=_skills.persuasion_proficient,
                religion=_skills.religion,
                religion_proficient=_skills.religion_proficient,
                sleight_of_hand=_skills.sleight_of_hand,
                sleight_of_hand_proficient=_skills.sleight_of_hand_proficient,
                stealth=_skills.stealth,
                stealth_proficient=_skills.stealth_proficient,
                survival=_skills.survival,
                survival_proficient=_skills.survival_proficient
            )

            _hitpoints = server_pb2.Hitpoints()
            _hitpoints.armor_class = request.character.hitpoints.armor_class
            _hitpoints.current_hitpoints = request.character.hitpoints.current_hitpoints
            _hitpoints.max_hitpoints = request.character.hitpoints.max_hitpoints
            _hitpoints.temporary_hitpoints = request.character.hitpoints.temporary_hitpoints
            _hitpoints.hitdice = request.character.hitpoints.hitdice

            hitpoints_db = db.Hitpoints(
                armor_class=_hitpoints.armor_class,
                current_hitpoints=_hitpoints.current_hitpoints,
                max_hitpoints=_hitpoints.max_hitpoints,
                temporary_hitpoints=_hitpoints.temporary_hitpoints,
                hitdice=_hitpoints.hitdice,
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
                hitpoints=hitpoints_db,
                passive_wisdom=_passive_wisdom,
                personality_traits=_personality_traits,
                ideals=_ideals,
                bonds=_bonds,
                flaws=_flaws,
                features_and_traits=_features_and_traits,
                level=_level,
                gender=_gender,
                session_id=None,
            )

            # Equipment
            for equipment in request.character.equipment:
                _eq = db.Equipment(
                    character_id=_character_id,
                    name=equipment.name,
                    value=equipment.value
                )
                character.equipment.append(_eq)

            self.conn.add(character)
            self.conn.commit()

            return helpers._convertToGrpcCharacter(character, "SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[CreateCharacter] SQLAlchemyError!" + str(err))
            return server_pb2.Character(
                status="FAILED",
                status_message="[CreateCharacter] Database error!")
        except Exception:
            self.logger.exception("[CreateCharacter] Unhandled exception occurred!")
            return server_pb2.Character(
                status="FAILED",
                status_message="[CreateCharacter] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()
