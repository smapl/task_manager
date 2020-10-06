import json

from datetime import datetime

from werkzeug.security import generate_password_hash
from flask_restplus import Resource, Api, Namespace, fields
from flask import Flask, request
from flask import current_app as app


from .handler import MainHandler
from .utils import parse_args, give_args, avoid_sql_injection

ns_tasks = Namespace("tasks")
ns_users = Namespace("users")

create_user = ns_tasks.model(
    "create_user",
    {
        "user_name": fields.String(required=True),
        "password": fields.String(required=True),
    },
)

create_task = ns_tasks.model(
    "create_task",
    {
        "task_name": fields.String(required=True),
        "task_description": fields.String(required=True),
        "task_status": fields.String(required=True),
        "task_planned_completed": fields.String(required=True),
        "user_token": fields.String(required=True),
    },
)

check_tasks_status = ns_tasks.model(
    "check_tasks_status",
    {
        "user_token": fields.String(required=True),
        "status_filter": fields.String(required=False),
    },
)

change_task_rows = ns_tasks.model(
    "change_task_rows",
    {
        "user_token": fields.String(required=True),
        "task_id": fields.Integer(required=True),
        "new_values": fields.Arbitrary(required=True),
    },
)

check_history_change = ns_tasks.model(
    "check_history_change",
    {
        "user_token": fields.String(required=True),
        "task_id": fields.Integer(required=True),
    },
)
postgre_login, postgre_password, host, db_name = give_args()


@ns_users.route("/create_user")
class CreateUser(Resource):
    @ns_users.expect(create_user, validate=True)
    def post(self):

        user_login = request.json.get("user_name")
        user_login = avoid_sql_injection(user_login)

        user_password = generate_password_hash(request.json.get("password"))
        user_password = avoid_sql_injection(user_password)

        hand = MainHandler(postgre_login, postgre_password, host, db_name)
        result = hand.create_user(user_login, user_password)

        return {"authtoken": result}


@ns_tasks.route("/create_task")
class CreateTask(Resource):
    @ns_tasks.expect(create_task, validate=True)
    def post(self):

        task_name = avoid_sql_injection(request.json.get("task_name"))
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

        if result == True:
            return {"respone": 200}

        else:
            return {"error": result}


@ns_tasks.route("/check_tasks_status")
class CheckTasksStatus(Resource):
    @ns_tasks.expect(check_tasks_status, validate=True)
    def get(self):

        data = parse_args(request.data)

        user_token = avoid_sql_injection(request.josn.get("authtoken"))

        try:
            status_filter = avoid_sql_injection(data["status_filter"])
        except KeyError:
            status_filter = None

        hand = MainHandler(postgre_login, postgre_password, host, db_name)
        result = hand.check_task_status(user_token, status_filter)

        return {"respone": result}


@ns_tasks.route("/change_task_rows")
class ChangeTaskRows(Resource):
    @ns_tasks.expect(change_task_rows, validate=True)
    def post(self):

        user_token = avoid_sql_injection(request.json.get("authtoken"))
        new_values = request.json.get("new_values")
        task_id = int(request.json.get("task_id"))

        hand = MainHandler(postgre_login, postgre_password, host, db_name)
        result = hand.change_task_rows(task_id, user_token, new_values)

        if result == True:
            return {"respone": 200}

        else:
            return {"error": result}


@ns_tasks.route("/check_history_change")
class CheckTaskHistory(Resource):
    @ns_tasks.expect(check_history_change, validate=True)
    def get(self):

        user_token = avoid_sql_injection(request.json.get("authtoken"))
        task_id = int(request.json.get("task_id"))

        hand = MainHandler(postgre_login, postgre_password, host, db_name)
        result = hand.check_history_change(user_token, task_id)

        if type(result) == dict:
            return {"tasks": result}
        else:
            return {"error": result}
