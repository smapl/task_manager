import hashlib
import argparse
import json

from datetime import datetime

from flask import request

def generate_token():
    now_date = str(datetime.now())
    token = hashlib.sha256(now_date.encode()).hexdigest()

    return token


def give_args():
    parser = argparse.ArgumentParser(description='Ping script')

    parser.add_argument("--login", action="store", dest="login")
    parser.add_argument("--password", action="store", dest="password")
    
    args = parser.parse_args()

    postgre_login = args.login
    postgre_password = args.password

    return postgre_login, postgre_password

def parse_args(data):
    data = request.data
    data = data.decode("utf-8")
    data = json.loads(data)

    return data

