import json

from datetime import datetime

from flask import Flask, request

from .create_app import create_app
from .handler import work_db
from .utils import parse_args


app = create_app()

@app.route("/create_user", methods=["POST"])
def main_page():

    data = parse_args(request.data)

    user_login = data["login"]
    user_password = data["password"]

    hand = work_db()
    result = hand.create_user(user_login, user_password)

    if result != "error":
        return result

    else:
        return "error"
    


@app.route("/create_task", methods="POST")
def create_task():

    data = parse_args(request.data)

    task_name = data["name"]
    task_description = data["description"]
    task_status = data["status"]
    task_planned_completed = data["planned_completed"]
    user_token = data["authtoken"]
    
    task_create_datetime = datetime.now()

    hand = work_db()
    result = hand.create_task(task_name, task_description, task_status, task_create_datetime, task_planned_completed, user_token)

    if result == True:
        return 200
    
    else:
        return result

    pass

# @app.route("/change_task_status", methods=['POST'])
# def change_task_status():
#     pass


# @app.route("/check_status", methods=["GET"])
# def check_status():
#     pass

# @app.route("/check_history", methods=["GET"])
# def check_history():
#     pass