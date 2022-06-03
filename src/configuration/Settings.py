import os
import base64
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENVIRONMENT = os.getenv("ENVIRONMENT")

    # Cloudinary
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
    
    # Database
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    # Email
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_ENCODING = os.getenv("EMAIL_ENCODING")
    
    ENCRYPTION_KEY = base64.b64decode(bytes(os.getenv("ENCRYPTION_KEY"), "utf-8")) # Sino importada como str
    
    # Firebase
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    
    JWT_KEY = os.getenv("JWT_KEY")
    
    # Mapbox
    MAPBOX_API = os.getenv("MAPBOX_API")
    MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")

    # Mercado Pago
    MP_PUBLIC_KEY = os.getenv("MP_PUBLIC_KEY")
    MP_ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN")
    MP_SUCCESS_URL = os.getenv("MP_SUCCESS_URL")
    MP_REJECTED_URL = os.getenv("MP_REJECTED_URL")
    MP_CANCEL_URL = os.getenv("MP_CANCEL_URL")

    # AWS
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")