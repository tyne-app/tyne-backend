import firebase_admin
import os


class FirebaseConfig:

    def init_firebase(self):
        if len(firebase_admin._apps) == 0:
            cred_obj = firebase_admin.credentials.Certificate(
                os.path.abspath("./configuration/firebase/firebase_credentials.json"))

            firebase_admin.initialize_app(cred_obj, {
                'projectId': "tyne-app",
                'apiKey': "AIzaSyDym-wsAA7O0Z7RkI32A1Og1s8LaJNa5s0"
            })
