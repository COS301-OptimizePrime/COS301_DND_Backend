import server_pb2
import server_pb2_grpc

import uuid

import logging
import log

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

cred = credentials.Certificate("dnd-game-manager-firebase-adminsdk-34ek4-cccabd3dd6.json")
firebase = firebase_admin.initialize_app(cred)
firestoreClient = firestore.client()

class Session(server_pb2_grpc.SessionsManagerServicer):

    def Create(self, request, context):
        logger = logging.getLogger('cos301-DND')
        logger.info('Created new session called!')

        _session_id = str(uuid.uuid4())
        _name = request.name
        _auth_id_token = request.auth_id_token
        
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
        })

        return server_pb2.Session(session_id = _session_id, name = _name, status="SUCCESS")

    def Join(self, request, context):
        logger = logging.getLogger('cos301-DND')
        logger.info('Join requested!')

        return server_pb2.Session(sessionId='idS!', name=request.name)
    
    def Leave(self, request, context):
        return server_pb2.Session(sessionId='idS!', name=request.name)

    def SetMax(self, request, context):
        return server_pb2.Session(sessionId='idS!', name=request.name)

    def List(self, request, context):
        return server_pb2.Session(sessionId='idS!', name=request.name)