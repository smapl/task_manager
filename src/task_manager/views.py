from flask import Flask, request
from .create_app import create_app


app = create_app()

@app.route("/", methods=["GET"])
def main_page():
    print(request.method)
    return "aloha"


@app.route("/create_task", methods="POST")
def create_task():
    pass

@app.route("/change_task_status", methods=['POST'])
def change_task_status():
    pass


@app.route("/check_status", methods=["GET"])
def check_status():
    pass

@app.route("/check_history", methods=["GET"])
def check_history():
    pass