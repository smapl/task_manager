import requests


def create_user():
    url = "http://127.0.0.1:5000/create_user"
    data = {"login": "Andrey", "password": "qwerty"}
    res = requests.post(url, json=data)

    return res.json()


def create_task():
    url = "http://127.0.0.1:5000/create_task"
    data = {
        "name": "delivery of the project",
        "description": "it is necessary to test the project",
        "status": "new",
        "planned_completed": "2021-7-12 12:30",
        "authtoken": "0592da0c178b1b2cb8291e8a8103b7f1414bedb49df0a301cdf2b0f00e886639",
    }
    res = requests.post(url, json=data)

    return res.json()


def check_tasks():
    url = "http://127.0.0.1:5000/check_tasks_status"

    data = {
        "authtoken": "0592da0c178b1b2cb8291e8a8103b7f1414bedb49df0a301cdf2b0f00e886639"
    }

    res = requests.get(url, json=data)
    return res.json()


def change_task_rows():
    url = "http://127.0.0.1:5000/change_task_rows"

    data = {
        "authtoken": "0592da0c178b1b2cb8291e8a8103b7f1414bedb49df0a301cdf2b0f00e886639",
        "task_id": "5",
        "new_values": {"status": "completed", "name": "backed"},
    }

    res = requests.post(url, json=data)
    return res.json()


def check_history_change():
    url = "http://127.0.0.1:5000/check_history_change"

    data = {
        "authtoken": "0592da0c178b1b2cb8291e8a8103b7f1414bedb49df0a301cdf2b0f00e886639",
        "task_id": "5",
    }

    res = requests.get(url, json=data)
    return res.json()


if __name__ == "__main__":
    # cu = create_user()
    # ct = create_task()
    # cc = check_tasks()
    # cts = change_task_rows()
    chc = check_history_change()
    print(chc)
