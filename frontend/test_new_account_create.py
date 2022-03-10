import requests


def client():
    url = 'http://127.0.0.1:8000/auth/users/'
    payload = {
        "username": "ben",
        "password": "123Divmbuyud",
        "re_password": "123Divmbuyud"
    }

    response = requests.post(url=url, data=payload)
    return response.json()


if __name__ == '__main__':
    print(client())
