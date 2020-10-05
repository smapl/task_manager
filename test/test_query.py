import requests


def create_user():
    url = "http://127.0.0.1:5000/create_user"
    data = {"login": "Smapl", "password": "qwerty"}
    res = requests.post(url, json=data)

    return res.text


def create_task():
    url = "http://127.0.0.1:5000/create_task"
    data = {
        "name": "backend",
        "description": "create backend to site",
        "status": "new",
        "planned_completed": "2021-7-12 12:30",
        "authtoken": "914fe08d9f8eaadddf5073516ba89976d8023812bc60d474f051f57a8e91eaa3",
    }
    res = requests.post(url, json=data)

    return res.text


def check_tasks():
    url = "http://127.0.0.1:5000/check_task_status"

    data = {
        "authtoken": "914fe08d9f8eaadddf5073516ba89976d8023812bc60d474f051f57a8e91eaa3"
    }

    res = requests.get(url, json=data)
    return res.text


def change_task_rows():
    url = "http://127.0.0.1:5000/change_task_rows"

    data = {
        "authtoken": "914fe08d9f8eaadddf5073516ba89976d8023812bc60d474f051f57a8e91eaa3",
        "task_id": "4",
        "new_values": {"status": "completed"},
    }

    res = requests.post(url, json=data)
    return res.text


def check_history_change():
    url = "http://127.0.0.1:5000/check_history_change"

    data = {
        "authtoken": "914fe08d9f8eaadddf5073516ba89976d8023812bc60d474f051f57a8e91eaa3",
        "task_id": "1",
    }

    res = requests.get(url, json=data)
    return res.text


if __name__ == "__main__":
    # cu = create_user()
    # ct = create_task()
    # cc = check_tasks()
    cts = change_task_rows()
    # chc = check_history_change()
    print(cts)
