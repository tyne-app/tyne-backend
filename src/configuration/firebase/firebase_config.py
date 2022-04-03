import firebase_admin
import os
from src.configuration.Settings import Settings

class FirebaseConfig:
    
    def init_firebase(self):
        if len(firebase_admin._apps) == 0:
            cred_obj = firebase_admin.credentials.Certificate(
                os.path.abspath("./src/configuration/firebase/firebase_credentials.json"))

            firebase_admin.initialize_app(cred_obj, {
                'projectId': Settings.FIREBASE_PROJECT_ID,
                'apiKey': Settings.FIREBASE_API_KEY
            })
