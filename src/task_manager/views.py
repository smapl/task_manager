import json

from datetime import datetime

from flask import Flask, request

from .create_app import create_app
from .handler import MainHandler
from .utils import parse_args, give_args


app = create_app()

postgre_login, postgre_password = give_args()


# TODO: NEED ON ALWAYS RETURN JSON
@app.route("/create_user", methods=["POST"])
def main_page():

    data = parse_args(request.data)

    user_login = data["login"]
    user_password = data["password"]

    hand = MainHandler(postgre_login, postgre_password)
    result = hand.create_user(user_login, user_password)

    if result != "error":
        return result

    else:
        return "error"


@app.route("/create_task", methods=["POST"])
def create_task():

    data = parse_args(request.data)

    task_name = data["name"]
    task_description = data["description"]
    task_status = data["status"]
    task_planned_completed = data["planned_completed"]
    user_token = data["authtoken"]

    task_create_datetime = datetime.now()

    hand = MainHandler(postgre_login, postgre_password)
    result = hand.create_task(
        task_name,
        task_description,
        task_status,
        task_create_datetime,
        task_planned_completed,
        user_token,
    )

    if result == True:
        return "200"

    else:
        return result


@app.route("/check_tasks", methods=["GET"])
def check_tasks():

    data = parse_args(request.data)

    user_token = data["authtoken"]

    try:
        status_filter = data["status_filter"]
    except KeyError:
        status_filter = None

    hand = MainHandler(postgre_login, postgre_password)
    result = hand.check_task_status(user_token, status_filter)

    return str(result)


@app.route("/change_task_rows", methods=["POST"])
def change_task_status():
    data = parse_args(request.data)

    user_token = data["authtoken"]
    new_values = data["new_values"]
    task_id = int(data["task_id"])

    hand = MainHandler(postgre_login, postgre_password)
    result = hand.change_task_rows(task_id, user_token, new_values)

    if result == True:
        return "200"

    else:
        return str(result)


@app.route("/check_history_change", methods=["GET"])
def check_history():
    data = parse_args(request.data)

    user_token = data["authtoken"]
    task_id = int(data["task_id"])

    hand = MainHandler(postgre_login, postgre_password)
    result = hand.check_history_change(user_token, task_id)

    return str(result)
