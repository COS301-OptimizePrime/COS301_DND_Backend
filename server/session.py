import datetime
import logging
import uuid

from sqlalchemy import and_, desc, exc

from . import config
from . import db
from . import firebase
from . import helpers
from . import server_pb2
from . import server_pb2_grpc


class Session(server_pb2_grpc.SessionsManagerServicer):
    conn = None
    logger = logging.getLogger("cos301-DND")

    def _connectDatabase(self):
        if not self.conn:
            self.conn = db.connect()

        return self.conn

    # Converts a Database Session object to a grpc Session object
    def _convertToGrpcSession(self, session, status):
        sessionObj = server_pb2.Session()
        sessionObj.session_id = session.session_id
        sessionObj.name = session.name
        sessionObj.dungeon_master.uid = session.dungeon_master.uid
        sessionObj.dungeon_master.name = session.dungeon_master.name
        sessionObj.date_created = str(session.date_created)
        sessionObj.max_players = session.max_players
        sessionObj.full = session.full
        sessionObj.private = session.private

        sessionObj.state = session.state
        sessionObj.state_meta = session.state_meta
        sessionObj.state_ready_start_time = str(session.state_ready_start_time)

        sessionObj.ready_up_expiry_time = session.ready_up_expiry_time

        sessionObj.last_updated = str(session.date_updated)

        sessionObj.users.extend([])

        for _user in session.users_in_session:
            userInSession = server_pb2.User()
            userInSession.uid = _user.uid
            userInSession.name = _user.name

            if _user in session.ready_users:
                userInSession.ready_in_this_session = True
            else:
                userInSession.ready_in_this_session = False

            sessionObj.users.extend([userInSession])

        sessionObj.ready_users.extend([])

        for _user in session.ready_users:
            userInSession = server_pb2.User()
            userInSession.uid = _user.uid
            userInSession.name = _user.name
            userInSession.ready_in_this_session = True
            sessionObj.ready_users.extend([userInSession])

        sessionObj.status = status

        return sessionObj

    def _convertToGrpcLightSession(self, session, status):
        sessionObj = server_pb2.LightSession()
        sessionObj.session_id = session.session_id
        sessionObj.name = session.name
        sessionObj.dungeon_master.uid = session.dungeon_master.uid
        sessionObj.dungeon_master.name = session.dungeon_master.name

        sessionObj.state = session.state
        sessionObj.last_updated = str(session.date_updated)
        sessionObj.status = status

        return sessionObj

    def Create(self, request, context):
        self.logger.debug(context.peer())
        self.logger.info("Create new session called! Name:" + request.name)

        _auth_id_token = request.auth_id_token
        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="[Create] Failed to verify user token!")

        _session_id = str(uuid.uuid4())
        _name = request.name
        _max_players = request.max_players
        _private = request.private

        try:
            self.conn = self._connectDatabase()
            user = self.conn.query(db.User).filter(db.User.uid == uid).first()
            if not user:
                user = db.User(uid=uid, name=firebase.auth.get_user(uid).email)
                self.conn.add(user)
                self.conn.commit()

            # Check how many sessions the user has.
            if len(user.session_dungeon_masters) >= config.val['server']['max_sessions_per_user']:
                self.logger.warning(
                    "Failed to create new session, user has reached max sessions")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[Create] User has too many sessions already!")

            if _max_players == 0:
                _max_players = 7

            session = db.Session(
                session_id=_session_id,
                name=_name,
                dungeon_master_id=user.id,
                max_players=_max_players,
                private=_private,
                state="PAUSED",
                state_meta=0,
                ready_up_expiry_time=20  # Default expiry time
            )
            if session.max_players <= len(session.users_in_session):
                session.full = True
            self.conn.add(session)
            self.conn.commit()

            return self._convertToGrpcSession(session, "SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[CREATE] SQLAlchemyError! " + str(err))
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        except Exception:
            self.logger.exception("[CREATE] Unhandled exception occurred!")
            return server_pb2.Session(
                status="FAILED",
                status_message="[CREATE] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def Join(self, request, context):
        self.logger.info("Join requested!")
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL", name="NULL", status="FAILED")

        self.logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        try:
            self.conn = self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning("Failed to join session, that ID does not exist!")
                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[JOIN] No session with that ID exists!")

            if uid == session.dungeon_master.uid:
                self.logger.warning(
                    "Failed to join session, you can not join your own session!")
                return self._convertToGrpcSession(session, "SUCCESS")

            if len(session.users_in_session) >= session.max_players:
                session.full = True
                self.logger.warning("Failed to join session, this session is full!")
                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[JOIN] This session is full!",
                    full=True)

            user = self.conn.query(db.User).filter(db.User.uid == uid).first()
            if not user:
                user = db.User(uid=uid, name=firebase.auth.get_user(uid).email)
                self.conn.add(user)
                self.conn.commit()

            if user in session.users_in_session:
                self.logger.warning(
                    "Failed to join session, you are already in this session!"
                    " Returning normal session!")
                return self._convertToGrpcSession(session, "SUCCESS")

            session.users_in_session.append(user)
            if session.max_players <= len(session.users_in_session):
                session.full = True
            self.conn.commit()

            return self._convertToGrpcSession(session, "SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[JOIN] SQLAlchemyError!" + str(err))
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        except Exception:
            self.logger.exception("[JOIN] Unhandled exception occurred!")
            return server_pb2.Session(
                status="FAILED",
                status_message="[JOIN] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def Leave(self, request, context):
        self.logger.info("Leave request called!")
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL", name="NULL", status="FAILED")

        self.logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        try:
            self.conn = self._connectDatabase()

            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning(
                    "Failed to leave session, that ID does not exist!")

                return server_pb2.Session(
                    status="FAILED",
                    status_message="[Leave] No session with that ID exists!")

            if uid == session.dungeon_master.uid:
                if len(session.users_in_session) == 0:
                    self.logger.warning(
                        "No users left in this session, deleting the session!")
                    self.conn.delete(session)
                    self.conn.commit()

                    return server_pb2.LeaveReply(status="SUCCESS")
                elif len(session.users_in_session) > 0:
                    # Assign new dungeon master.
                    self.logger.info(
                        "Original Dungeon Master left assigning a new one!")
                    new_DM = self.conn.query(
                        db.User).join(
                        db.User.joined_sessions).filter(
                        db.Session.session_id == _session_id).first()
                    session.dungeon_master = new_DM
                    # Remove DM from users array.
                    session.users_in_session.remove(new_DM)
                    self.conn.commit()

                    return server_pb2.LeaveReply(status="SUCCESS")

            user = self.conn.query(
                db.User).join(
                db.User.joined_sessions).filter(
                and_(
                    db.Session.session_id == _session_id,
                    db.User.uid == uid)).first()

            if not user:
                self.logger.warning(
                    "User does not exist. This could mean that the"
                    " user is not in the session")

                return server_pb2.Session(
                    status="FAILED",
                    status_message="[Leave] User is not in the session!")

            # logger.debug(user)

            session.users_in_session.remove(user)
            if session.max_players > len(session.users_in_session):
                session.full = False

            if len(session.users_in_session) == 0:
                self.logger.info(
                    "No users left in this session, deleting the session!")
                self.conn.delete(session)

            self.conn.commit()

            return server_pb2.LeaveReply(status="SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[LEAVE] SQLAlchemyError!" + str(err))
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        except Exception:
            self.logger.exception("[LEAVE] Unhandled exception occurred!")
            return server_pb2.Session(
                status="FAILED",
                status_message="[LEAVE] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def Ready(self, request, context):
        self.logger.info("Ready request called!")
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.ReadyUpReply(
                status="FAILED",
                status_message="Failed to verify login!")

        self.logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        try:
            self.conn = self._connectDatabase()

            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning(
                    "Failed to ready up in session, that ID does not exist!")

                return server_pb2.ReadyUpReply(
                    status="FAILED",
                    status_message="[Ready] No session with that ID exists!")

            if session.state != "READYUP":
                self.logger.warning(
                    "Failed to ready up in session, not in READYUP phase!")
                return server_pb2.ReadyUpReply(
                    status="FAILED",
                    status_message="[Ready] Can't ready up now. Not in the ready up phase!")
            else:
                # If ready up older than 20 seconds it has expired
                if session.state_ready_start_time < datetime.datetime.now() - datetime.timedelta(
                        seconds=session.ready_up_expiry_time):
                    # Expired ready up phase reset.
                    # Delete all ready users in session

                    for _user in session.ready_users:
                        session.ready_users.remove(_user)

                    # Update state
                    session.state = "PAUSED"
                    session.state_meta = session.state_meta + 1

                    self.logger.warning(
                        "Failed to ready up in session, READYUP phase has expired!")

                    return server_pb2.ReadyUpReply(
                        status="FAILED",
                        status_message="[Ready] Can't ready up now. Ready up time expired!")

            user = self.conn.query(
                db.User).join(
                db.User.joined_sessions).filter(
                and_(
                    db.Session.session_id == _session_id,
                    db.User.uid == uid)).first()

            if not user:
                self.logger.warning(
                    "User does not exist. This could mean that the"
                    " user is not in the session")

                return server_pb2.ReadyUpReply(
                    status="FAILED",
                    status_message="[Ready] User is not in the session!")

            session.ready_users.append(user)

            # TODO: There should be a more optimal way of doing this.
            if len(session.ready_users) == len(session.users_in_session):
                self.logger.info("[Ready] Everyone is ready starting game!")
                # All users are ready change the state
                session.state = "EXPLORING"
                session.state_meta = session.state_meta + 1
                for _user in session.ready_users:
                    session.ready_users.remove(_user)

            self.conn.commit()

            return server_pb2.ReadyUpReply(status="SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[Ready] SQLAlchemyError!" + str(err))
            return server_pb2.ReadyUpReply(
                status="FAILED",
                status_message="Database error!")
        except Exception:
            self.logger.exception("[Ready] Unhandled exception occurred!")
            return server_pb2.ReadyUpReply(
                status="FAILED",
                status_message="[Ready] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def Kick(self, request, context):
        self.logger.info("Kick player request called!")
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL", name="NULL", status="FAILED")

        self.logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        try:
            self.conn = self._connectDatabase()

            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning(
                    "Failed to leave session, that ID does not exist!")

                return server_pb2.Session(
                    status="FAILED",
                    status_message="[Kick] No session with that ID exists!")

            if session.dungeon_master.uid != uid:
                self.logger.warning(
                    "[Kick] Unauthorised user tried to"
                    " modify (Not the dungeon master)")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[Kick] You must be the dungeon master"
                                   " to use this command!")

            player_to_kick = request.user

            if player_to_kick.uid == uid:
                self.logger.warning("[Kick] Attempted to kick dungeon master!")

                return server_pb2.Session(
                    status="FAILED",
                    status_message="[Kick] Attempted to kick dungeon master!")

            user = self.conn.query(
                db.User).filter(
                and_(
                    db.Session.session_id == _session_id,
                    db.User.uid == player_to_kick.uid)).first()

            # logger.debug(player_to_kick)

            if not user:
                self.logger.warning(
                    "User does not exist. This could mean that the"
                    " user is not in the session")

                return server_pb2.Session(
                    status="FAILED",
                    status_message="[Kick] User is not in the session!")

            session.users_in_session.remove(user)
            if session.max_players > len(session.users_in_session):
                session.full = False
            self.conn.commit()

            return self._convertToGrpcSession(session, "SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[KICK] SQLAlchemyError! " + str(err))
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="[KICK] Database error!")
        except Exception:
            self.logger.exception("[KICK] Unhandled exception occurred!")
            return server_pb2.Session(
                status="FAILED",
                status_message="[KICK] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    # This is a Dungeon Master only command.
    def SetMax(self, request, context):
        self.logger.info("SetMax called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="[SetMax] Failed to verify login!")

        _session_id = request.session_id

        try:
            self.conn = self._connectDatabase()

            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning(
                    "[SetMax] Failed to update max players of session,"
                    " that ID does not exist!")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[SetMax] No session with that ID exists!")

            if session.dungeon_master.uid != uid:
                self.logger.warning(
                    "[SetMax] Unauthorised user tried to modify"
                    " (Not the dungeon master)")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[SetMax] You must be the dungeon"
                                   " master to use this command!")

            session.max_players = request.number
            if session.max_players <= len(session.users_in_session):
                session.full = True
            self.conn.commit()

            return self._convertToGrpcSession(session, "SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[SETMAX] SQLAlchemyError!" + str(err))
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        except Exception:
            self.logger.exception("[SETMAX] Unhandled exception occurred!")
            return server_pb2.Session(
                status="FAILED",
                status_message="[SETMAX] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    # This is a Dungeon Master only command.
    def SetName(self, request, context):
        self.logger.info("SetName called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="[SETNAME] Failed to verify login!")

        _session_id = request.session_id

        try:
            self.conn = self._connectDatabase()

            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning(
                    "[SetName] Failed to update name of session,"
                    " that ID does not exist!")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[SetName] No session with that ID exists!")

            if session.dungeon_master.uid != uid:
                self.logger.warning(
                    "[SetName] Unauthorised user tried to"
                    " modify (Not the dungeon master)")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[SetName] You must be the dungeon"
                                   " master to use this command!")

            session.name = request.name

            self.conn.commit()

            return self._convertToGrpcSession(session, "SUCCESS")
        except exc.SQLAlchemyError:
            self.logger.error("[SETNAME] SQLAlchemyError!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="[SETNAME] Database error!")
        except Exception:
            self.logger.exception("[SETNAME] Unhandled exception occurred!")
            return server_pb2.Session(
                status="FAILED",
                status_message="[SETNAME] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    # This is a Dungeon Master only command.
    def ChangeState(self, request, context):
        self.logger.info("ChangeState called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[ChangeState] Failed to verify login!")

        _session_id = request.session_id

        try:
            self.conn = self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning(
                    "[ChangeState] Failed to change state of session,"
                    " that ID does not exist!")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[ChangeState] No session with that ID exists!")

            if session.dungeon_master.uid != uid:
                self.logger.warning(
                    "[ChangeState] Unauthorised user tried to"
                    " modify (Not the dungeon master)")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[ChangeState] You must be the dungeon"
                                   " master to use this command!")

            # Check if it is a valid state
            if request.state in ["PAUSED", "READYUP", "BATTLE", "EXPLORING"]:
                if session.state == "BATTLE" and request.state == "PAUSED":
                    return server_pb2.Session(
                        session_id="NULL",
                        name="NULL",
                        status="FAILED",
                        status_message="[ChangeState] Can not pause during battle!")

                session.state = request.state
                session.state_meta = session.state_meta + 1
                if request.state == "READYUP":
                    session.state_ready_start_time = datetime.datetime.now()

            else:
                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[ChangeState] Invalid state can only be PAUSED, READYUP, BATTLE or EXPLORING")

            self.conn.commit()

            return self._convertToGrpcSession(session, "SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[ChangeState] SQLAlchemyError! " + str(err))
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="[ChangeState] Database error!")
        except Exception:
            self.logger.exception("[ChangeState] Unhandled exception occurred!")
            return server_pb2.Session(
                status="FAILED",
                status_message="[ChangeState] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    # This is a Dungeon Master only command.
    def SetPrivate(self, request, context):
        self.logger.info("SetPrivate called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.error("Failed to verify login!")

        _session_id = request.session_id

        try:
            self.conn = self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning(
                    "[SetPrivate] Failed to update privacy state of session,"
                    " that ID does not exist!")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[SetPrivate] No session with that ID exists!")

            if session.dungeon_master.uid != uid:
                self.logger.warning(
                    "[SetPrivate] Unauthorised user tried to modify"
                    " (Not the dungeon master)")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[SetPrivate] You must be the dungeon"
                                   " master to use this command!")

            session.private = request.private

            self.conn.commit()

            return self._convertToGrpcSession(session, "SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[SETPRIVATE] SQLAlchemyError! " + str(err))
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="[SETPRIVATE] Database error!")
        except Exception:
            self.logger.exception("[SETPRIVATE] Unhandled exception occurred!")
            return server_pb2.Session(
                status="FAILED",
                status_message="[SETPRIVATE] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    # This is a Dungeon Master only command.
    def ChangeReadyUpExpiryTime(self, request, context):
        self.logger.info("ChangeReadyUpExpiryTime called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")

        _session_id = request.session_id

        try:
            self.conn = self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning(
                    "[ChangeReadyUpExpiryTime] Failed to update expiry time of ready up of session,"
                    " that ID does not exist!")

                return server_pb2.ChangeReadyUpExpiryTimeResponse(
                    status="FAILED",
                    status_message="[ChangeReadyUpExpiryTime] No session with that ID exists!")

            if session.dungeon_master.uid != uid:
                self.logger.warning(
                    "[ChangeReadyUpExpiryTime] Unauthorised user tried to modify"
                    " (Not the dungeon master)")

                return server_pb2.ChangeReadyUpExpiryTimeResponse(
                    status="FAILED",
                    status_message="[ChangeReadyUpExpiryTime] You must be the dungeon"
                                   " master to use this command!")

            session.ready_up_expiry_time = request.ready_up_expiry_time

            self.conn.commit()

            return self._convertToGrpcSession(session, "SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[ChangeReadyUpExpiryTime] SQLAlchemyError! " + str(err))
            return server_pb2.ChangeReadyUpExpiryTimeResponse(
                status="FAILED",
                status_message="[ChangeReadyUpExpiryTime] Database error!")
        except Exception:
            self.logger.exception("[ChangeReadyUpExpiryTime] Unhandled exception occurred!")
            return server_pb2.ChangeReadyUpExpiryTimeResponse(
                status="FAILED",
                status_message="[ChangeReadyUpExpiryTime] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def List(self, request, context):
        self.logger.info("List sessions called!")

        _limit = request.limit
        _full = request.full
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.ListReply(status="FAILED")

        self.logger.debug("Successfully verified token! UID=" + uid)

        try:
            self.conn = self._connectDatabase()

            if _full:
                _sessions_query = self.conn.query(
                    db.Session).filter(
                    db.Session.private == False).order_by(
                    desc(
                        db.Session.date_created)).limit(_limit)
            else:
                _sessions_query = self.conn.query(
                    db.Session).filter(
                    and_(
                        db.Session.private == False,
                        db.Session.full != True)).order_by(
                    desc(
                        db.Session.date_created)).limit(_limit)

            _sessions = []

            for _session in _sessions_query:
                # logger.debug(_session.session_id)
                # TODO: Remove this function or update it with ready up phase
                sessionObj = server_pb2.Session()
                sessionObj.session_id = _session.session_id
                sessionObj.name = _session.name
                sessionObj.dungeon_master.uid = _session.dungeon_master.uid
                sessionObj.dungeon_master.name = _session.dungeon_master.name
                sessionObj.date_created = str(_session.date_created)
                sessionObj.max_players = _session.max_players
                sessionObj.full = _session.full
                sessionObj.private = _session.private
                sessionObj.users.extend([])

                for _user in _session.users_in_session:
                    userInSession = server_pb2.User()
                    userInSession.uid = _user.uid
                    userInSession.name = _user.name
                    sessionObj.users.extend([userInSession])

                _sessions.append(sessionObj)

            return server_pb2.ListReply(status="SUCCESS", sessions=_sessions)
        except exc.SQLAlchemyError as err:
            self.logger.error("[List] SQLAlchemyError! " + str(err))
            return server_pb2.ListReply(
                status="FAILED",
                status_message="[List] Database error!")
        except Exception:
            self.logger.exception("[List] Unhandled exception occurred!")
            return server_pb2.ListReply(
                status="FAILED",
                status_message="[List] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def GetSessionById(self, request, context):
        self.logger.info("GetSessionById called!")

        _session_id = request.session_id
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="[GetSessionById] Failed to verify token!")

        self.logger.debug("Successfully verified token! UID=" + uid)

        try:
            self.conn = self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning(
                    "[GetSessionById] Failed to get session,"
                    " that ID does not exist!")
                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[GetSessionById] No session"
                                   " with that ID exists!")

            if session.state_ready_start_time < datetime.datetime.now() - datetime.timedelta(
                    seconds=session.ready_up_expiry_time):
                # Expired ready up phase reset.
                # Delete all ready users in session

                for _user in session.ready_users:
                    session.ready_users.remove(_user)

                # Update state
                session.state = "PAUSED"
                self.conn.commit()

            return self._convertToGrpcSession(session, "SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[SETPRIVATE] SQLAlchemyError! " + str(err))
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        except Exception:
            self.logger.exception("[GetSessionsOfUser] Unhandled exception occurred!")
            return server_pb2.GetSessionsOfUserReply(
                status="FAILED",
                status_message="[GetSessionsOfUser] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def GetSessionsOfUser(self, request, context):
        self.logger.info("GetSessionsOfUser sessions called!")

        _limit = request.limit
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.GetSessionsOfUserReply(status="FAILED",
                                                     status_message="[GetSessionsOfUser] Failed to verify login!")

        self.logger.debug("Successfully verified token! UID=" + uid)

        try:
            self.conn = self._connectDatabase()

            user = self.conn.query(
                db.User).filter(
                db.User.uid == uid).first()

            if not user:
                self.logger.warning("User does not exist adding!")
                user = db.User(uid=uid, name=firebase.auth.get_user(uid).email)
                self.conn.add(user)
                self.conn.commit()

            _sessions = []
            limit = 0

            user_sessions = user.session_dungeon_masters + user.joined_sessions

            for _session in user_sessions:
                limit = limit + 1

                _sessions.append(self._convertToGrpcLightSession(session=_session, status="SUCCESS"))
                if limit >= _limit:
                    break

            return server_pb2.GetSessionsOfUserReply(status="SUCCESS", light_sessions=_sessions)
        except exc.SQLAlchemyError as err:
            self.logger.error("[GetSessionsOfUser] SQLAlchemyError! " + str(err))
            return server_pb2.GetSessionsOfUserReply(
                status="FAILED",
                status_message="[GetSessionsOfUser] Database error!")
        except Exception:
            self.logger.exception("[GetSessionsOfUser] Unhandled exception occurred!")
            return server_pb2.GetSessionsOfUserReply(
                status="FAILED",
                status_message="[GetSessionsOfUser] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def GetCharactersInSession(self, request, context):
        self.logger.info("GetCharactersInSession called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.GetCharactersInSessionResponse(
                status="FAILED",
                status_message="[GetCharactersInSession] Failed to verify token!")

        self.logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        try:
            self.conn = self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning("Failed to get characters in session, that ID does not exist!")
                return server_pb2.GetCharactersInSessionResponse(
                    status="FAILED",
                    status_message="[GetCharactersInSession] No session with that ID exists!")

            # Get all characters.
            _light_characters = session.characters_in_session

            light_characters = []
            for _char in _light_characters:
                light_characters.append(helpers._convertToGrpcLightCharacter(_char))

            return server_pb2.GetCharactersInSessionResponse(status="SUCCESS", light_characters=light_characters)
        except exc.SQLAlchemyError as err:
            self.logger.error("[GetCharactersInSession] SQLAlchemyError!" + str(err))
            return server_pb2.GetCharactersInSessionResponse(
                status="FAILED",
                status_message="[GetCharactersInSession] Database error!")
        except Exception:
            self.logger.exception("[GetCharactersInSession] Unhandled exception occurred!")
            return server_pb2.GetCharactersInSessionResponse(
                status="FAILED",
                status_message="[GetCharactersInSession] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def AddCharacterToSession(self, request, context):
        self.logger.info("AddCharacterToSession called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Session(
                status="FAILED",
                status_message="[AddCharacterToSession] Failed to verify token!")

        self.logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        try:
            self.conn = self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning("Failed to add character to session, that ID does not exist!")
                return server_pb2.Session(
                    status="FAILED",
                    status_message="[AddCharacterToSession] No session with that ID exists!")

            _char_id = request.character_id
            char = self.conn.query(db.Character).filter(db.Character.character_id == _char_id).first()

            if not char:
                self.logger.warning("Failed to add character to session, that character does not exist!")
                return server_pb2.Session(
                    status="FAILED",
                    status_message="[AddCharacterToSession] No character with that ID exists!")

            if char.session:
                self.logger.warning("Failed to add character to session, that character is already in a session!")
                return server_pb2.Session(
                    status="FAILED",
                    status_message="[AddCharacterToSession] Failed to add character to session, that character is already in a session!")

            # Add character
            session.characters_in_session.append(char)
            self.conn.commit()

            return self._convertToGrpcSession(session, status="SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[AddCharacterToSession] SQLAlchemyError!" + str(err))
            return server_pb2.Session(
                status="FAILED",
                status_message="[AddCharacterToSession] Database error!")
        except Exception:
            self.logger.exception("[AddCharacterToSession] Unhandled exception occurred!")
            return server_pb2.Session(
                status="FAILED",
                status_message="[AddCharacterToSession] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def RemoveCharacterFromSession(self, request, context):
        self.logger.info("RemoveCharacterFromSession called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.warning("Failed to verify login!")
            return server_pb2.Session(
                status="FAILED",
                status_message="[RemoveCharacterFromSession] Failed to verify token!")

        self.logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        try:
            self.conn = self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                self.logger.warning("Failed to remove character from session, that ID does not exist!")
                return server_pb2.Session(
                    status="FAILED",
                    status_message="[RemoveCharacterFromSession] No session with that ID exists!")

            _char_id = request.character_id
            char = self.conn.query(db.Character).filter(db.Character.character_id == _char_id).first()

            if not char:
                self.logger.warning("Failed to remove character from session, that character does not exist!")
                return server_pb2.Session(
                    status="FAILED",
                    status_message="[RemoveCharacterFromSession] No character with that ID exists!")

            # Check if character is in the session.
            if not char.session.session_id == session.session_id:
                self.logger.warning("Failed to remove character from session, that character is not in this session!")
                return server_pb2.Session(
                    status="FAILED",
                    status_message="[RemoveCharacterFromSession] Failed to remove character from session, that character is not in this session!")

            # Check that the character is owned by the user
            if not char.creator.uid == uid:
                self.logger.warning("Failed to remove character from session, this is not your character!")
                return server_pb2.Session(
                    status="FAILED",
                    status_message="[RemoveCharacterFromSession] Failed to remove character from session, this is not your character")

            # Remove character
            session.characters_in_session.remove(char)
            self.conn.commit()

            return self._convertToGrpcSession(session, status="SUCCESS")
        except exc.SQLAlchemyError as err:
            self.logger.error("[RemoveCharacterFromSession] SQLAlchemyError!" + str(err))
            return server_pb2.Session(
                status="FAILED",
                status_message="[RemoveCharacterFromSession] Database error!")
        except Exception:
            self.logger.exception("[RemoveCharacterFromSession] Unhandled exception occurred!")
            return server_pb2.Session(
                status="FAILED",
                status_message="[RemoveCharacterFromSession] Internal server error! Blame Thomas!")
        finally:
            self.conn.close()

    def __del__(self):
        self.logger.info("Socket destroyed ...")
