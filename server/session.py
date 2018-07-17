import calendar
import datetime
import logging
import uuid

from sqlalchemy import and_, desc, exc

import database.db as db
import firebase
import log
import server_pb2
import server_pb2_grpc


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

        self.conn.close()

        return sessionObj

    def Create(self, request, context):
        self.logger.debug(context.peer())
        self.logger.info("Create new session called! Name:" + request.name)

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.error("Failed to verify login!")
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
            self._connectDatabase()
            user = self.conn.query(db.User).filter(db.User.uid == uid).first()
            if not user:
                user = db.User(uid=uid, name=firebase.auth.get_user(uid).email)
                self.conn.add(user)
                self.conn.commit()

            # Check how many sessions the user has.
            if len(user.session_dungeon_masters) >= 100:
                self.logger.error(
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
                state_meta=0
            )
            if session.max_players <= len(session.users_in_session):
                session.full = True
            self.conn.add(session)
            self.conn.commit()

            grpcSession = self._convertToGrpcSession(session, "SUCCESS")

            return grpcSession
        except exc.SQLAlchemyError as err:
            self.logger.error("[CREATE] SQLAlchemyError! " + str(err))
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    def Join(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("Join requested!")
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL", name="NULL", status="FAILED")

        logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        try:
            self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:

                logger.error("Failed to join session, that ID does not exist!")
                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[JOIN] No session with that ID exists!")

            if uid == session.dungeon_master.uid:
                logger.error(
                    "Failed to join session, you can not join your own session!")
                return self._convertToGrpcSession(session, "SUCCESS")

            if len(session.users_in_session) >= session.max_players:
                session.full = True
                logger.error("Failed to join session, this session is full!")
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
                logger.error(
                    "Failed to join session, you are already in this session!"
                    " Returning normal sessison!")
                return self._convertToGrpcSession(session, "SUCCESS")

            session.users_in_session.append(user)
            if session.max_players <= len(session.users_in_session):
                session.full = True
            self.conn.commit()

            grpcSession = self._convertToGrpcSession(session, "SUCCESS")

            return grpcSession
        except exc.SQLAlchemyError:
            self.logger.error("[JOIN] SQLAlchemyError!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    def Leave(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("Leave request called!")
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL", name="NULL", status="FAILED")

        logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        try:
            self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                logger.error(
                    "Failed to leave session, that ID does not exist!")

                return server_pb2.Session(
                    status="FAILED",
                    status_message="[Leave] No session with that ID exists!")

            if uid == session.dungeon_master.uid:
                if len(session.users_in_session) == 0:
                    logger.info(
                        "No users left in this session, deleting the session!")
                    self.conn.delete(session)
                    self.conn.commit()

                    return server_pb2.LeaveReply(status="SUCCESS")
                elif len(session.users_in_session) > 0:
                    # Assign new dungeon master.
                    logger.info(
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
                logger.error(
                    "User does not exist. This could mean that the"
                    " user is not in the session")

                return server_pb2.Session(
                    status="FAILED",
                    status_message="[Leave] User is not in the session!")

            logger.debug(user)

            session.users_in_session.remove(user)
            if session.max_players > len(session.users_in_session):
                session.full = False

            if len(session.users_in_session) == 0:
                logger.info(
                    "No users left in this session, deleting the session!")
                self.conn.delete(session)

            self.conn.commit()

            return server_pb2.LeaveReply(status="SUCCESS")
        except exc.SQLAlchemyError:
            self.logger.error("[LEAVE] SQLAlchemyError!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    def Ready(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("Ready request called!")
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.ReadyUpReply(
                status="FAILED",
                status_message="Failed to verify login!")

        logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        try:
            self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                logger.error(
                    "Failed to ready up in session, that ID does not exist!")

                return server_pb2.ReadyUpReply(
                    status="FAILED",
                    status_message="[Ready] No session with that ID exists!")

            if session.state != "READYUP":
                logger.error(
                    "Failed to ready up in session, not in READYUP phase!")
                return server_pb2.ReadyUpReply(
                    status="FAILED",
                    status_message="[Ready] Can't ready up now. Not in the ready up phase!")
            else:
                # If ready up older than 20 seconds it has expired
                if session.state_ready_start_time < datetime.datetime.now() - datetime.timedelta(seconds=20):
                    # Expired ready up phase reset.
                    # Delete all ready users in session

                    for _user in session.ready_users:
                        session.ready_users.remove(_user)

                    # Update state
                    session.state = "PAUSED"
                    session.state_meta = session.state_meta + 1

                    logger.error(
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
                logger.error(
                    "User does not exist. This could mean that the"
                    " user is not in the session")

                return server_pb2.ReadyUpReply(
                    status="FAILED",
                    status_message="[Ready] User is not in the session!")

            session.ready_users.append(user)

            if len(session.ready_users) == len(session.users_in_session):
                self.logger.info("[Ready] Everyone is ready starting game!")
                # All users are ready change the state
                session.state = "EXPLORING"
                session.state_meta = session.state_meta + 1
                for _user in session.ready_users:
                    session.ready_users.remove(_user)

            self.conn.commit()

            return server_pb2.ReadyUpReply(status="SUCCESS")
        except exc.SQLAlchemyError:
            self.logger.error("[Ready] SQLAlchemyError!")
            return server_pb2.ReadyUpReply(
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    def Kick(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("Kick player request called!")
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL", name="NULL", status="FAILED")

        logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        try:
            self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                logger.error(
                    "Failed to leave session, that ID does not exist!")

                return server_pb2.Session(
                    status="FAILED",
                    status_message="[Kick] No session with that ID exists!")

            if session.dungeon_master.uid != uid:
                logger.error(
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
                logger.error("[Kick] Attempted to kick dungeon master!")

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
                logger.error(
                    "User does not exist. This could mean that the"
                    " user is not in the session")

                return server_pb2.Session(
                    status="FAILED",
                    status_message="[Kick] User is not in the session!")

            session.users_in_session.remove(user)
            if session.max_players > len(session.users_in_session):
                session.full = False
            self.conn.commit()

            grpcSession = self._convertToGrpcSession(session, "SUCCESS")

            return grpcSession
        except exc.SQLAlchemyError as err:
            self.logger.error("[KICK] SQLAlchemyError! " + err)
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    # This is a Dungeon Master only command.
    def SetMax(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("SetMax called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")

        _session_id = request.session_id

        try:
            self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                logger.error(
                    "[SetMax] Failed to update max players of session,"
                    " that ID does not exist!")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[SetMax] No session with that ID exists!")

            if session.dungeon_master.uid != uid:
                logger.error(
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

            grpcSession = self._convertToGrpcSession(session, "SUCCESS")

            return grpcSession
        except exc.SQLAlchemyError:
            self.logger.error("[SETMAX] SQLAlchemyError!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    # This is a Dungeon Master only command.
    def SetName(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("SetName called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")

        _session_id = request.session_id

        try:
            self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                logger.error(
                    "[SetName] Failed to update name of session,"
                    " that ID does not exist!")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[SetName] No session with that ID exists!")

            if session.dungeon_master.uid != uid:
                logger.error(
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

            grpcSession = self._convertToGrpcSession(session, "SUCCESS")

            return grpcSession
        except exc.SQLAlchemyError:
            self.logger.error("[SETNAME] SQLAlchemyError!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    # This is a Dungeon Master only command.
    def ChangeState(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("ChangeState called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")

        _session_id = request.session_id

        try:
            self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                logger.error(
                    "[ChangeState] Failed to change state of session,"
                    " that ID does not exist!")

                return server_pb2.ChangeStateReply(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[ChangeState] No session with that ID exists!")

            if session.dungeon_master.uid != uid:
                logger.error(
                    "[ChangeState] Unauthorised user tried to"
                    " modify (Not the dungeon master)")

                return server_pb2.ChangeStateReply(
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

            grpcSession = self._convertToGrpcSession(session, "SUCCESS")

            return grpcSession
        except exc.SQLAlchemyError as err:
            self.logger.error("[ChangeState] SQLAlchemyError! " + str(err))
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    # This is a Dungeon Master only command.
    def SetPrivate(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("SetPrivate called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")

        _session_id = request.session_id

        try:
            self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                logger.error(
                    "[SetPrivate] Failed to update privacy state of session,"
                    " that ID does not exist!")

                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[SetPrivate] No session with that ID exists!")

            if session.dungeon_master.uid != uid:
                logger.error(
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

            grpcSession = self._convertToGrpcSession(session, "SUCCESS")

            return grpcSession
        except exc.SQLAlchemyError:
            self.logger.error("[SETPRIVATE] SQLAlchemyError!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    def List(self, request, context):
        #if not context.is_active():
        #    self.__del__()

        logger = logging.getLogger("cos301-DND")
        logger.info("List sessions called!")

        _limit = request.limit
        _full = request.full
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.ListReply(status="FAILED")

        logger.debug("Successfully verified token! UID=" + uid)

        try:
            self._connectDatabase()

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
        except exc.SQLAlchemyError:
            self.logger.error("[SETPRIVATE] SQLAlchemyError!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    def GetSessionById(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("GetSessionById called!")

        _session_id = request.session_id
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="[GetSessionById] Failed to verify token!")

        logger.debug("Successfully verified token! UID=" + uid)

        try:
            self._connectDatabase()
            session = self.conn.query(db.Session).filter(
                db.Session.session_id == _session_id).first()

            if not session:
                logger.error(
                    "[GetSessionById] Failed to get session,"
                    " that ID does not exist!")
                return server_pb2.Session(
                    session_id="NULL",
                    name="NULL",
                    status="FAILED",
                    status_message="[GetSessionById] No session"
                                   " with that ID exists!")

            grpcSession = self._convertToGrpcSession(session, "SUCCESS")

            return grpcSession
        except exc.SQLAlchemyError:
            self.logger.error("[SETPRIVATE] SQLAlchemyError!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    def GetSessionsOfUser(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("GetSessionsOfUser sessions called!")

        _limit = request.limit
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = firebase.auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.ListReply(status="FAILED")

        logger.debug("Successfully verified token! UID=" + uid)

        try:
            self._connectDatabase()

            _sessions_query = self.conn.query(
                db.User).filter(
                db.User.uid == uid).first()

            _sessions = []

            limit = 0

            user_sessions = _sessions_query.session_dungeon_masters + \
                _sessions_query.joined_sessions

            for _session in user_sessions:
                limit = limit + 1

                # logger.debug(_session.session_id)
                # TODO: This will need to support the new state and ready system

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

                if limit >= _limit:
                    break

            return server_pb2.ListReply(status="SUCCESS", sessions=_sessions)
        except exc.SQLAlchemyError:
            self.logger.error("[GetSessionsOfUser] SQLAlchemyError!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="Database error!")
        finally:
            self.conn.close()

    def __del__(self):
        self.logger.info("Socket destroyed closing DB connection...")
        self.conn.close()
