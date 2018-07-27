import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate(
    "dnd-game-manager-firebase-adminsdk-34ek4-cccabd3dd6.json")
firebase = firebase_admin.initialize_app(cred)

