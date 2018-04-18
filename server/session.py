import server_pb2
import server_pb2_grpc

import uuid

import logging
import log

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from datetime import datetime
import calendar

cred = credentials.Certificate("dnd-game-manager-firebase-adminsdk-34ek4-cccabd3dd6.json")
firebase = firebase_admin.initialize_app(cred)
firestoreClient = firestore.client()

class Session(server_pb2_grpc.SessionsManagerServicer):

    def Create(self, request, context):
        logger = logging.getLogger('cos301-DND')
        logger.info('Create new session called!')

        _session_id = str(uuid.uuid4())
        _name = request.name
        _auth_id_token = request.auth_id_token

        d = datetime.utcnow()
        _date_created = calendar.timegm(d.utctimetuple())
        
        try:
            decoded_token = auth.verify_id_token(_auth_id_token)
            uid = decoded_token['uid']
        except ValueError:
            logger.error("Failed to verify login!")
            return server_pb2.Session(session_id = 'NULL', name = 'NULL', status='FAILED')

        logger.info('Successfully verified token! UID=' + uid)

        doc_ref = firestoreClient.collection(u'sessions').document(_session_id)
        doc_ref.set({
            u'session_id': _session_id,
            u'name': _name,
            u'date_created': _date_created,
            u'dungeon_master': uid,
            u'users': []
        })

        _dungeon_master = server_pb2.User()
        _dungeon_master.uid = uid

        return server_pb2.Session(session_id = _session_id, name = _name, status="SUCCESS", dungeon_master=_dungeon_master, date_created=_date_created)

    def Join(self, request, context):
        logger = logging.getLogger('cos301-DND')
        logger.info('Join requested!')

        return server_pb2.Session(sessionId='idS!', name=request.name)
    
    def Leave(self, request, context):
        return server_pb2.Session(sessionId='idS!', name=request.name)

    def SetMax(self, request, context):
        return server_pb2.Session(sessionId='idS!', name=request.name)

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
        sessions_ref = firestoreClient.collection(u'sessions')

        _sessions = []

        for _session in sessions_ref.limit(_limit).get():
            logger.debug(_session.get('session_id'))

            sessionObj = server_pb2.Session()
            sessionObj.name = _session.get('name')
            sessionObj.session_id = _session.get('session_id')
            sessionObj.dungeon_master.uid = _session.get('dungeon_master')
            sessionObj.date_created = _session.get('date_created')

            for _user in _session.get('users'):
                userInSession = server_pb2.User()
                userInSession.uid = _user.uid
                sessionObj.users.append(userInSession)

            _sessions.append(sessionObj)


        return server_pb2.ListReply(status='SUCCESS', sessions=_sessions)