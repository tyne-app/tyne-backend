import os
import base64
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENVIRONMENT = os.getenv("ENVIRONMENT")

    # Database
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    CONNECTION_STRING_DB = os.getenv("DB_CONN")

    # Cloudinary
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    # Khipu
    KHIPU_SECRET_ID = os.getenv("KHIPU_SECRET_ID")
    KHIPU_RECEIVER_ID = os.getenv("KHIPU_RECEIVER_ID")
    KHIPU_NOTIFY_URL = os.getenv("KHIPU_NOTIFY_URL")
    KHIPU_RETURN_URL = os.getenv("KHIPU_RETURN_URL")
    KHIPU_CANCEL_URL = os.getenv("KHIPU_CANCEL_URL")
    KHIPU_PICTURE_URL = os.getenv("KHIPU_PICTURE_URL")

    # Mapbox
    MAPBOX_API = os.getenv("MAPBOX_API")
    MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")

    # Email
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = os.getenv("EMAIL_PORT")
    EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_ENCODING = os.getenv("EMAIL_ENCODING")

    # Others
    ENCRYPTION_KEY = base64.b64decode(bytes(os.getenv("ENCRYPTION_KEY"), "utf-8")) # Sino importada como str
    JWT_KEY = os.getenv("JWT_KEY")
