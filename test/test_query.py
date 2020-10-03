import requests


def create_user():
    url = "http://127.0.0.1:5000/create_user"
    data = {"login": "Smapl", "password": "qwerty"}
    res = requests.post(url, json=data)

    return res.text


def create_task():
    url = "http://127.0.0.1:5000/create_task"
    data = {
        "name": "create testing",
        "description": "me need create test for company",
        "status": "New",
        "planned_completed": "2020-10-08 08:30",
        "authtoken": "914fe08d9f8eaadddf5073516ba89976d8023812bc60d474f051f57a8e91eaa3",
    }
    res = requests.post(url, json=data)

    return res.text


def check_tasks():
    url = "http://127.0.0.1:5000/check_tasks"

    data = {
        "authtoken": "914fe08d9f8eaadddf5073516ba89976d8023812bc60d474f051f57a8e91eaa3"
    }

    res = requests.get(url, json=data)
    return res.text


def change_task_status():
    url = "http://127.0.0.1:5000/change_task_rows"

    data = {
        "authtoken": "914fe08d9f8eaadddf5073516ba89976d8023812bc60d474f051f57a8e91eaa3",
        "task_id": "2",
        "new_values": {"status": "asdqwe"},
    }

    res = requests.post(url, json=data)
    return res.text


if __name__ == "__main__":
    # cu = create_user()
    # ct = create_task()
    cc = check_tasks()
    # sts = change_task_status()
    print(cc)
