import urllib.parse as up
import psycopg2

"""
    Local environment
"""
# USER_DATABASE = "tyne"
# PASSWORD_DATABASE = "tyne"
# DATABASE_HOST = "localhost"
# DATABASE_PORT = "5432"
# DATABASE_NAME = "tyne_local"

"""
    Prod environment
"""
USER_DATABASE = "tvuvmojgjmztvp"
PASSWORD_DATABASE = "acffb7c029d6205560e994bd4ff4fb5d61b313f7a9cf7464b3391d7862317faa"
DATABASE_HOST = "ec2-3-215-57-87.compute-1.amazonaws.com"
DATABASE_PORT = "5432"
DATABASE_NAME = "deg5v46mdpumk7"

# CLOUD_DATA_BASE_URL = f'postgresql://hdczrnil:DhRwoHUGtdv-KU0m7ErSivOjCKdx58pT@queenie.db.elephantsql.com/hdczrnil'
CLOUD_DATA_BASE_URL = f'postgresql+psycopg2://{USER_DATABASE}:{PASSWORD_DATABASE}@{DATABASE_HOST}/{DATABASE_NAME}'
