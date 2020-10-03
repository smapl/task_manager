import requests


def create_user():
    url = "http://127.0.0.1:5000/create_user"
    data = {"login": "Smapl", "password": "qwerty"}
    res = requests.post(url, json=data)

    return res.text


def create_task():
    url = "http://127.0.0.1:5000/create_task"
    data = {
        "name": "frontend",
        "description": "create front to site",
        "status": "new",
        "planned_completed": "2020-1-12 18:20",
        "authtoken": "b95dda629968cf2293642deb70b6e3eb0882f84c090ffce43108aa73efd23264",
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
        "task_id": "1",
        "new_values": {"status": "completed", "description": "i create this"},
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
    # sts = change_task_status()
    chc = check_history_change()
    print(chc)
