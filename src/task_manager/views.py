import json

from datetime import datetime

from flask import Flask, request, session
from werkzeug.security import generate_password_hash

from .create_app import create_app
from .handler import MainHandler
from .utils import give_args, avoid_sql_injection


app = create_app()

postgre_login, postgre_password, host, db_name = give_args()


@app.route("/create_user", methods=["POST"])
def create_user():

    user_login = request.json.get("login")
    user_login = avoid_sql_injection(user_login)

    user_password = generate_password_hash(request.json.get("password"))
    user_password = avoid_sql_injection(user_password)

    hand = MainHandler(postgre_login, postgre_password, host, db_name)
    result = hand.create_user(user_login, user_password)

    hand._disconnect()
    return {"response": result}


@app.route("/create_task", methods=["POST"])
def create_task():

    task_name = avoid_sql_injection(request.json.get("name"))
    task_description = avoid_sql_injection(request.json.get("description"))
    task_status = avoid_sql_injection(request.json.get("status"))
    task_planned_completed = request.json.get("planned_completed")
    user_token = avoid_sql_injection(request.json.get("authtoken"))

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

    hand._disconnect()
    return {"response": result}


@app.route("/check_tasks_status", methods=["GET"])
def check_tasks_status():

    user_token = avoid_sql_injection(request.json.get("authtoken"))

    try:
        status_filter = request.json.get("status_filter")

    except KeyError:
        status_filter = None

    hand = MainHandler(postgre_login, postgre_password, host, db_name)
    result = hand.check_task_status(user_token, status_filter)

    hand._disconnect()
    return {"response": result}


@app.route("/change_task_rows", methods=["POST"])
def change_task_rows():

    user_token = avoid_sql_injection(request.json.get("authtoken"))
    new_values = request.json.get("new_values")
    task_id = int(request.json.get("task_id"))

    hand = MainHandler(postgre_login, postgre_password, host, db_name)
    result = hand.change_task_rows(task_id, user_token, new_values)

    hand._disconnect()
    return {"response": result}


@app.route("/check_history_change", methods=["GET"])
def check_history():

    user_token = avoid_sql_injection(request.json.get("authtoken"))
    task_id = int(request.json.get("task_id"))

    hand = MainHandler(postgre_login, postgre_password, host, db_name)
    result = hand.check_history_change(user_token, task_id)

    hand._disconnect()
    return {"response": result}

