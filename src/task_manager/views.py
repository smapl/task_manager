import json

from flask import Flask, request

from .create_app import create_app
from .handler import work_db

app = create_app()

@app.route("/create_user", methods=["POST"])
def main_page():

    data = request.data
    data = data.decode("utf-8")
    data = json.loads(data)

    user_login = data["login"]
    user_password = data["password"]

    hand = work_db()
    result = hand.create_user(user_login, user_password)

    if result != "error":
        hand.disconnect()
        return result

    else:
        return "error"
    


# @app.route("/create_task", methods="POST")
# def create_task():
#     pass

# @app.route("/change_task_status", methods=['POST'])
# def change_task_status():
#     pass


# @app.route("/check_status", methods=["GET"])
# def check_status():
#     pass

# @app.route("/check_history", methods=["GET"])
# def check_history():
#     pass