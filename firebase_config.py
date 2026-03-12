import firebase_admin
from firebase_admin import credentials, firestore
import pyrebase

# ---------------- FIREBASE ADMIN (Firestore) ----------------

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ---------------- FIREBASE AUTH (Pyrebase) ----------------

firebase_config = {
    "apiKey": "AIzaSyCtnuAKgrv2rp8a6sjDhjsmyFbtgyO_Y3g",
    "authDomain": "stocksenseai-9c007.firebaseapp.com",
    "projectId": "stocksenseai-9c007",
    "storageBucket": "stocksenseai-9c007.appspot.com",   # FIXED
    "messagingSenderId": "616874316903",
    "appId": "1:616874316903:web:49a44fcab5d30fe4f9b0c2",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()