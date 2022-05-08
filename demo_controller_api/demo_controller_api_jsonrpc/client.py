import requests
import json

HOST = "http://0.0.0.0:8069"
AUTH_URL = "{}/web/session/authenticate/".format(HOST)

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

session_data = {
    "jsonrpc": "2.0",
    "params": {
        "login": "admin",
        "password": "admin",
        "db": "odoo",
    },
}


def get_session_id():
    res = requests.post(AUTH_URL, data=json.dumps(session_data), headers=headers)
    return res.cookies["session_id"]


def get_users():
    base_url = "{}/api/users/".format(HOST)

    res = requests.get(
        base_url,
        data=json.dumps({}),
        headers=headers,
        cookies={"session_id": get_session_id()},
    )

    print(res.json())


def get_user():
    base_url = "{}/api/users/3/".format(HOST)

    res = requests.get(
        base_url,
        data=json.dumps({}),
        headers=headers,
        cookies={"session_id": get_session_id()},
    )

    print(res.json())


def add_user():
    base_url = "{}/api/users/".format(HOST)
    param = {
        "login": "test_user",
        "name": "test_user",
        "phone": "00000",
        "email": "xxx@test.com",
    }

    res = requests.post(
        base_url,
        data=json.dumps(param),
        headers=headers,
        cookies={"session_id": get_session_id()},
    )

    print(res.json())


def edit_user():
    base_url = "{}/api/users/3/".format(HOST)
    param = {
        "phone": "0000000000",
    }

    res = requests.patch(
        base_url,
        data=json.dumps(param),
        headers=headers,
        cookies={"session_id": get_session_id()},
    )

    print(res.json())


if __name__ == "__main__":
    get_users()
    # get_user()
    # add_user()
    # edit_user()
