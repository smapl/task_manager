import hashlib
import argparse
import json

from datetime import datetime

import psycopg2

from loguru import logger
from flask import request


def generate_token() -> str:
    now_date = str(datetime.now())
    token = hashlib.sha256(now_date.encode()).hexdigest()

    return token


def give_args() -> tuple:
    parser = argparse.ArgumentParser(description="Ping script")

    parser.add_argument("--login", action="store", dest="login")
    parser.add_argument("--password", action="store", dest="password")

    args = parser.parse_args()

    postgre_login = args.login
    postgre_password = args.password

    return postgre_login, postgre_password


def parse_args(data) -> dict:
    data = request.data
    data = data.decode("utf-8")
    data = json.loads(data)

    return data


def definitions_user_id(authtoken) -> str:
    postgre_login, postgre_password = give_args()

    connection = psycopg2.connect(
        dbname="users", user=postgre_login, password=postgre_password, host="localhost",
    )
    cursor = connection.cursor()
    table_name_user = "users_data"
    cursor.execute(
        f"""
                    SELECT id FROM {table_name_user} 
                    WHERE authtoken = %(authtoken)s;
                """,
        {"authtoken": authtoken},
    )
    user_id = cursor.fetchall()[0][0]
    connection.close()

    return user_id
