import server_pb2
import server_pb2_grpc

import uuid

import logging
import log

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

import datetime
import calendar

cred = credentials.Certificate("dnd-game-manager-firebase-adminsdk-34ek4-cccabd3dd6.json")
firebase = firebase_admin.initialize_app(cred)

import database.db as db
from sqlalchemy import and_

class Session(server_pb2_grpc.SessionsManagerServicer):

    def Create(self, request, context):
        logger = logging.getLogger('cos301-DND')
        logger.info('Create new session called!')

        _session_id = str(uuid.uuid4())
        _name = request.name
        _auth_id_token = request.auth_id_token

        _date_created = datetime.datetime.utcnow()

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token['uid']
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(session_id = 'NULL', name = 'NULL', status='FAILED')

        logger.info('Successfully verified token! UID=' + uid)

        conn = db.connect()
        user = conn.query(db.User).filter(db.User.uid == uid).first()
        if not user:
            user = db.User(uid=uid, name=auth.get_user(uid).email)
            conn.add(user)
            conn.commit()

        session = db.Session(session_id=_session_id, name=_name, dungeon_master_id=user.id, max_players=7) 
        conn.add(session)
        conn.commit()
        conn.remove()

        _dungeon_master = server_pb2.User()
        _dungeon_master.uid = uid

        return server_pb2.Session(session_id = _session_id, name = _name, status="SUCCESS", dungeon_master=_dungeon_master, date_created=str(_date_created))

    def Join(self, request, context):
        logger = logging.getLogger('cos301-DND')
        logger.info('Join requested!')
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token['uid']
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(session_id = 'NULL', name = 'NULL', status='FAILED')

        logger.info('Successfully verified token! UID=' + uid)

        _session_id = request.session_id

        conn = db.connect()
        session = conn.query(db.Session).filter(db.Session.session_id == _session_id).first()

        if not session:
            logger.error("Failed to join session, that ID does not exist!")
            return server_pb2.Session(session_id = 'NULL', name = 'NULL', status='FAILED', status_message='[JOIN] No session with that ID exists!')

        if len(session.users_in_session) >= session.max_players:
            logger.error("Failed to join session, this session is full!")
            return server_pb2.Session(session_id = 'NULL', name = 'NULL', status='FAILED', status_message='[JOIN] This session is full!')

        user = conn.query(db.User).filter(db.User.uid == uid).first()
        if not user:
            user = db.User(uid=uid, name=auth.get_user(uid).email)
            conn.add(user)
            conn.commit()
        
        session.users_in_session.append(user)
        conn.commit()

        sessionObj = server_pb2.Session()
        sessionObj.session_id = session.session_id
        sessionObj.name = session.name
        sessionObj.dungeon_master.uid = session.dungeon_master.uid
        sessionObj.date_created = str(session.date_created)
        sessionObj.max_players = session.max_players
        sessionObj.users.extend([])

        for _user in session.users_in_session:
            userInSession = server_pb2.User()
            userInSession.uid = _user.uid
            userInSession.name = _user.name
            sessionObj.users.extend([userInSession])

        conn.remove()
        return server_pb2.Session(session_id = sessionObj.session_id,
                                        name = sessionObj.name,
                                        status="SUCCESS", 
                                        dungeon_master=sessionObj.dungeon_master, 
                                        date_created=sessionObj.date_created, 
                                        users=sessionObj.users, 
                                        max_players=sessionObj.max_players)
    
    def Leave(self, request, context):
        logger = logging.getLogger('cos301-DND')
        logger.info('Leave request called!')
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token['uid']
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(session_id = 'NULL', name = 'NULL', status='FAILED')

        logger.info('Successfully verified token! UID=' + uid)

        _session_id = request.session_id

        conn = db.connect()
        session = conn.query(db.Session).filter(db.Session.session_id == _session_id).first()

        if not session:
            logger.error("Failed to leave session, that ID does not exist!")
            return server_pb2.Session(status='FAILED', status_message='[Leave] No session with that ID exists!')
        
        user = conn.query(db.User).filter(and_(db.Session.session_id == _session_id, db.Session.users_in_session.any(db.User.uid == uid))).first()

        if not user:
            logger.error("User does not exist. This could mean that the user is not in the session")
            return server_pb2.Session(status='FAILED', status_message='[Leave] User is not in the session!')

        #logger.debug(user)

        session.users_in_session.remove(user)
        conn.commit()
        conn.remove()

        return server_pb2.LeaveReply(status='SUCCESS')

    # This is a Dungeon Master only command.
    def SetMax(self, request, context):
        logger = logging.getLogger('cos301-DND')
        logger.info('SetMax called!')

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token['uid']
        except ValueError:
            logger.error("Failed to verify login!")

        _session_id = request.session_id

        conn = db.connect()
        session = conn.query(db.Session).filter(db.Session.session_id == _session_id).first()

        if not session:
            logger.error("[SetMax] Failed to update max players of session, that ID does not exist!")
            return server_pb2.Session(session_id = 'NULL', name = 'NULL', status='FAILED', status_message='[SetMax] No session with that ID exists!')

        if session.dungeon_master.uid != uid:
            logger.error("[SetMax] Unauthorised user tried to modify (Not the dungeon master")
            return server_pb2.Session(session_id = 'NULL', name = 'NULL', status='FAILED', status_message='[SetMax] You must be the dungeon master to use this command!')

        session.max_players = request.number
        conn.commit()

        sessionObj = server_pb2.Session()
        sessionObj.session_id = session.session_id
        sessionObj.name = session.name
        sessionObj.dungeon_master.uid = session.dungeon_master.uid
        sessionObj.date_created = str(session.date_created)
        sessionObj.max_players = session.max_players
        sessionObj.users.extend([])

        for _user in session.users_in_session:
            userInSession = server_pb2.User()
            userInSession.uid = _user.uid
            userInSession.name = _user.name
            sessionObj.users.extend([userInSession])

        conn.remove()

        return server_pb2.Session(session_id = sessionObj.session_id,
                                        name = sessionObj.name,
                                        status="SUCCESS", 
                                        dungeon_master=sessionObj.dungeon_master, 
                                        date_created=sessionObj.date_created, 
                                        users=sessionObj.users, 
                                        max_players=sessionObj.max_players)


    def List(self, request, context):
        logger = logging.getLogger('cos301-DND')
        logger.info('List sessions called!')

        _limit = request.limit
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token['uid']
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.ListReply(status='FAILED')

        logger.info('Successfully verified token! UID=' + uid)

        conn = db.connect()
        _sessions_query = conn.query(db.Session).limit(_limit)

        _sessions = []

        for _session in _sessions_query:
            logger.debug(_session.session_id)

            sessionObj = server_pb2.Session()
            sessionObj.session_id = _session.session_id
            sessionObj.name = _session.name
            sessionObj.dungeon_master.uid = _session.dungeon_master.uid
            sessionObj.date_created = str(_session.date_created)
            sessionObj.max_players = _session.max_players
            sessionObj.users.extend([])

            for _user in _session.users_in_session:
                userInSession = server_pb2.User()
                userInSession.uid = _user.uid
                userInSession.name = _user.name
                sessionObj.users.extend([userInSession])

            _sessions.append(sessionObj)

        conn.remove()
        return server_pb2.ListReply(status='SUCCESS', sessions=_sessions)

    def GetSessionById(self, request, context):
        logger = logging.getLogger('cos301-DND')
        logger.info('GetSessionById called!')

        _session_id = request.session_id
        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token['uid']
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(session_id = 'NULL', name = 'NULL', status='FAILED', status_message='[GetSessionById] Failed to verify token!')

        logger.info('Successfully verified token! UID=' + uid)

        conn = db.connect()
        session = conn.query(db.Session).filter(db.Session.session_id == _session_id).first()

        if not session:
            logger.error("[GetSessionById] Failed to get session, that ID does not exist!")
            return server_pb2.Session(session_id = 'NULL', name = 'NULL', status='FAILED', status_message='[GetSessionById] No session with that ID exists!')

        sessionObj = server_pb2.Session()
        sessionObj.session_id = session.session_id
        sessionObj.name = session.name
        sessionObj.dungeon_master.uid = session.dungeon_master.uid
        sessionObj.date_created = str(session.date_created)
        sessionObj.max_players = session.max_players
        sessionObj.users.extend([])

        for _user in session.users_in_session:
            userInSession = server_pb2.User()
            userInSession.uid = _user.uid
            userInSession.name = _user.name
            sessionObj.users.extend([userInSession])

        conn.remove()

        return server_pb2.Session(session_id = sessionObj.session_id,
                                        name = sessionObj.name,
                                        status="SUCCESS", 
                                        dungeon_master=sessionObj.dungeon_master, 
                                        date_created=sessionObj.date_created, 
                                        users=sessionObj.users, 
                                        max_players=sessionObj.max_players)