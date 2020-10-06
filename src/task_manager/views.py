import json

from datetime import datetime

from flask import Flask, request, session
from werkzeug.security import generate_password_hash

from .create_app import create_app
from .handler import MainHandler
from .utils import parse_args, give_args, avoid_sql_injection


app = create_app()

postgre_login, postgre_password, host, db_name = give_args()


@app.route("/create_user", methods=["POST"])
def create_user():

    data = parse_args(request.data)

    user_login = data["login"]
    user_login = avoid_sql_injection(user_login)

    user_password = generate_password_hash(data["password"])
    user_password = avoid_sql_injection(user_password)

    hand = MainHandler(postgre_login, postgre_password, host, db_name)
    result = hand.create_user(user_login, user_password)

    return {"authtoken": result}


@app.route("/create_task", methods=["POST"])
def create_task():

    data = parse_args(request.data)

    task_name = avoid_sql_injection(data["name"])
    task_description = avoid_sql_injection(data["description"])
    task_status = avoid_sql_injection(data["status"])
    task_planned_completed = data["planned_completed"]
    user_token = avoid_sql_injection(data["authtoken"])

    task_create_datetime = datetime.now()

    hand = MainHandler(postgre_login, postgre_password, host, db_name)
    result = hand.create_task(
        task_name,
        task_description,
        task_status,
        task_create_datetime,
        task_planned_completed,
        user_token,
    )

    if result == True:
        return {"respone": 200}

    else:
        return {"error": result}


@app.route("/check_tasks_status", methods=["GET"])
def check_tasks_status():

    data = parse_args(request.data)

    user_token = avoid_sql_injection(data["authtoken"])

    try:
        status_filter = avoid_sql_injection(data["status_filter"])
    except KeyError:
        status_filter = None

    hand = MainHandler(postgre_login, postgre_password, host, db_name)
    result = hand.check_task_status(user_token, status_filter)

    return {"respone": result}


@app.route("/change_task_rows", methods=["POST"])
def change_task_rows():
    data = parse_args(request.data)

    user_token = avoid_sql_injection(data["authtoken"])
    new_values = data["new_values"]
    task_id = int(data["task_id"])

    hand = MainHandler(postgre_login, postgre_password, host, db_name)
    result = hand.change_task_rows(task_id, user_token, new_values)

    if result == True:
        return {"respone": 200}

    else:
        return {"error": result}


@app.route("/check_history_change", methods=["GET"])
def check_history():
    data = parse_args(request.data)

    user_token = avoid_sql_injection(data["authtoken"])
    task_id = int(data["task_id"])

    hand = MainHandler(postgre_login, postgre_password, host, db_name)
    result = hand.check_history_change(user_token, task_id)

    if type(result) == dict:
        return {"tasks": result}
    else:
        return {"error": result}
