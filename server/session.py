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
#firestoreClient = firestore.client()

import database.db as db

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

        return server_pb2.Session(sessionId='idS!', name=request.name)
    
    def Leave(self, request, context):
        return server_pb2.Session(sessionId='idS!', name=request.name)

    def SetMax(self, request, context):
        logger = logging.getLogger('cos301-DND')
        logger.info('SetMax called!')

        _auth_id_token = request.auth_id_token

        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token['uid']
        except ValueError:
            logger.error("Failed to verify login!")

        session = request.session

        _number = request.number
        session.max_players = _number

        return session


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

        # Query firebase
        #sessions_ref = firestoreClient.collection(u'sessions')

        conn = db.connect()
        _sessions_query = conn.query(db.Session).limit(_limit)

        _sessions = []

        for _session in _sessions_query:
            logger.debug(_session.session_id)

            sessionObj = server_pb2.Session()
            sessionObj.name = _session.name
            sessionObj.session_id = _session.session_id
            sessionObj.dungeon_master.uid = _session.dungeon_master.uid
            sessionObj.date_created = str(_session.date_created)

            for _user in _session.users_in_session:
                userInSession = server_pb2.User()
                userInSession.uid = _user.uid
                sessionObj.users.append(userInSession)

            _sessions.append(sessionObj)

        conn.remove()
        return server_pb2.ListReply(status='SUCCESS', sessions=_sessions)