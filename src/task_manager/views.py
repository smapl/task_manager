import json

from datetime import datetime

from werkzeug.security import generate_password_hash
from flask_restplus import Resource, Api, Namespace, fields
from flask import Flask, request
from flask import current_app as app

from loguru import logger

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
        "new_values": fields.Raw(required=True),
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

        hand._disconnect()
        return {"response": result}


@ns_tasks.route("/create_task")
class CreateTask(Resource):
    @ns_tasks.expect(create_task, validate=True)
    def post(self):
        logger.info(request.json)
        task_name = avoid_sql_injection(request.json.get("task_name"))
        task_description = avoid_sql_injection(request.json.get("task_description"))
        task_status = avoid_sql_injection(request.json.get("task_status"))
        task_planned_completed = request.json.get("task_planned_completed")
        user_token = avoid_sql_injection(request.json.get("user_token"))

        logger.info(
            f"{task_name} - {task_description} - {task_status} - {task_planned_completed} - {user_token}"
        )
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


@ns_tasks.route("/check_tasks_status")
class CheckTasksStatus(Resource):
    @ns_tasks.param("authtoken")
    @ns_tasks.param("status_filter")
    def get(self):

        user_token = request.args.get("authtoken")
        status_filter = request.args.get("status_filter")
        logger.info(status_filter)

        hand = MainHandler(postgre_login, postgre_password, host, db_name)
        result = hand.check_task_status(user_token, status_filter)
        logger.info(result)

        hand._disconnect()
        return {"response": result}


@ns_tasks.route("/change_task_rows")
class ChangeTaskRows(Resource):
    @ns_tasks.expect(change_task_rows, validate=True)
    def post(self):

        user_token = avoid_sql_injection(request.json.get("user_token"))
        new_values = request.json.get("new_values")
        task_id = int(request.json.get("task_id"))

        logger.info(f"{user_token}, {new_values}, {task_id}")

        hand = MainHandler(postgre_login, postgre_password, host, db_name)
        result = hand.change_task_rows(task_id, user_token, new_values)

        hand._disconnect()
        return {"response": result}


@ns_tasks.route("/check_history_change")
class CheckTaskHistory(Resource):
    @ns_tasks.param("user_token")
    @ns_tasks.param("task_id")
    def get(self):

        user_token = avoid_sql_injection(request.args.get("user_token"))
        task_id = int(request.args.get("task_id"))

        logger.info(f"{user_token} -- {task_id}")
        hand = MainHandler(postgre_login, postgre_password, host, db_name)
        result = hand.check_history_change(user_token, task_id)

        hand._disconnect()
        return {"response": result}
