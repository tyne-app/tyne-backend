import urllib.parse as up
import psycopg2

"""
    Local environment
"""
USER_DATABASE = "tyne"
PASSWORD_DATABASE = "tyne"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"
DATABASE_NAME = "tyne_local"

# CLOUD_DATA_BASE_URL = f'postgresql://hdczrnil:DhRwoHUGtdv-KU0m7ErSivOjCKdx58pT@queenie.db.elephantsql.com/hdczrnil'
CLOUD_DATA_BASE_URL = f'postgresql+psycopg2://{USER_DATABASE}:{PASSWORD_DATABASE}@{DATABASE_HOST}/{DATABASE_NAME}'
