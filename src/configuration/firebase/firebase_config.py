import firebase_admin
import os
from src.configuration.Settings import Settings

class FirebaseConfig:
    _settings_ = Settings()

    def init_firebase(self):
        if len(firebase_admin._apps) == 0:
            cred_obj = firebase_admin.credentials.Certificate(
                os.path.abspath("./src/configuration/firebase/firebase_credentials.json"))

            firebase_admin.initialize_app(cred_obj, {
                'projectId': self._settings_.FIREBASE_PROJECT_ID,
                'apiKey': self._settings_.FIREBASE_API_KEY
            })
