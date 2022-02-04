import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ENVIRONMENT = os.getenv("ENVIRONMENT")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    CONNECTION_STRING_DB = os.getenv("DB_CONN")
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
    KHIPU_SECRET_ID = os.getenv("KHIPU_SECRET_ID")
    KHIPU_RECEIVER_ID = os.getenv("KHIPU_RECEIVER_ID")
    KHIPU_NOTIFY_URL = os.getenv("KHIPU_NOTIFY_URL")
    KHIPU_RETURN_URL = os.getenv("KHIPU_RETURN_URL")
    KHIPU_CANCEL_URL = os.getenv("KHIPU_CANCEL_URL")
    KHIPU_PICTURE_URL = os.getenv("KHIPU_PICTURE_URL")
    JWT_KEY = os.getenv("JWT_KEY")
    MAPBOX_API = os.getenv("MAPBOX_API")
    MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    PASSWORD_EMAIL = os.getenv("PASSWORD_EMAIL")
    PORT_EMAIL = os.getenv("PORT_EMAIL")
    ENCODING_EMAIL = os.getenv("ENCODING_EMAIL")

