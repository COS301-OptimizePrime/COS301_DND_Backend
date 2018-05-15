import calendar
import datetime
import logging
import uuid

import firebase_admin
from firebase_admin import auth, credentials, firestore
from sqlalchemy import and_, desc

import database.db as db
import log
import server_pb2
import server_pb2_grpc

cred = credentials.Certificate(
    "dnd-game-manager-firebase-adminsdk-34ek4-cccabd3dd6.json")
firebase = firebase_admin.initialize_app(cred)


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
        sessionObj.users.extend([])

        for _user in session.users_in_session:
            userInSession = server_pb2.User()
            userInSession.uid = _user.uid
            userInSession.name = _user.name
            sessionObj.users.extend([userInSession])

        sessionObj.status = status

        return sessionObj

    def Create(self, request, context):
        self.logger.debug(context.peer())
        self.logger.info("Create new session called!")

        _session_id = str(uuid.uuid4())
        _name = request.name
        _auth_id_token = request.auth_id_token
        _max_players = request.max_players
        _private = request.private

        _date_created = datetime.datetime.utcnow()

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            self.logger.error("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="[Create] Failed to verify user token!")

        self._connectDatabase()
        user = self.conn.query(db.User).filter(db.User.uid == uid).first()
        if not user:
            user = db.User(uid=uid, name=auth.get_user(uid).email)
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
            private=_private)
        if session.max_players <= len(session.users_in_session):
            session.full = True
        self.conn.add(session)
        self.conn.commit()

        grpcSession = self._convertToGrpcSession(session, "SUCCESS")

        return grpcSession

    def Join(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("Join requested!")
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL", name="NULL", status="FAILED")

        logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

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
            user = db.User(uid=uid, name=auth.get_user(uid).email)
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

    def Leave(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("Leave request called!")
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL", name="NULL", status="FAILED")

        logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        self._connectDatabase()
        session = self.conn.query(db.Session).filter(
            db.Session.session_id == _session_id).first()

        if not session:
            logger.error("Failed to leave session, that ID does not exist!")

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
            logger.info("No users left in this session, deleting the session!")
            self.conn.delete(session)

        self.conn.commit()

        return server_pb2.LeaveReply(status="SUCCESS")

    def Kick(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("Kick player request called!")
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL", name="NULL", status="FAILED")

        logger.debug("Successfully verified token! UID=" + uid)

        _session_id = request.session_id

        self._connectDatabase()
        session = self.conn.query(db.Session).filter(
            db.Session.session_id == _session_id).first()

        if not session:
            logger.error("Failed to leave session, that ID does not exist!")

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

    # This is a Dungeon Master only command.
    def SetMax(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("SetMax called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")

        _session_id = request.session_id

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

    # This is a Dungeon Master only command.
    def SetName(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("SetName called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")

        _session_id = request.session_id

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

    # This is a Dungeon Master only command.
    def SetPrivate(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("SetPrivate called!")

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")

        _session_id = request.session_id

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
                " (Not the dungeon master")

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

    def List(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("List sessions called!")

        _limit = request.limit
        _full = request.full
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.ListReply(status="FAILED")

        logger.debug("Successfully verified token! UID=" + uid)

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

    def GetSessionById(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("GetSessionById called!")

        _session_id = request.session_id
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(
                session_id="NULL",
                name="NULL",
                status="FAILED",
                status_message="[GetSessionById] Failed to verify token!")

        logger.debug("Successfully verified token! UID=" + uid)

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

    def GetSessionsOfUser(self, request, context):
        logger = logging.getLogger("cos301-DND")
        logger.info("GetSessionsOfUser sessions called!")

        _limit = request.limit
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token["uid"]
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.ListReply(status="FAILED")

        logger.debug("Successfully verified token! UID=" + uid)

        self._connectDatabase()

        # this will exclude DM sessions
        # TODO
        _sessions_query = self.conn.query(
            db.User).filter(
            db.User.uid == uid).first()

        _sessions = []

        limit = 0

        # _sessions_query.session_dungeon_masters

        for _session in _sessions_query.joined_sessions:
            limit = limit + 1

            # logger.debug(_session.session_id)

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
