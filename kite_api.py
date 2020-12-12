import requests
import json


def check_email(email):
    headers = {
        'content-type': 'application/json',
    }

    data = json.dumps({"email": email})
    response = requests.post('https://alpha.kite.com/api/account/check-email', headers=headers, data=data)
    if response.status_code == 200:
        return True
    else:
        return response.text


def create_account(email, password):
    import requests

    url = "https://alpha.kite.com/api/account/create-web"

    payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n{email}\r\n" \
              f"-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n{password}" \
              f"\r\n-----011000010111000001101001--\r\n "
    headers = {
        'content-type': "multipart/form-data; boundary=---011000010111000001101001"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    if response.status_code == 200:
        result = response.json()
        result["cookie"] = response.headers["Set-Cookie"].split(";")[0]
        return result
    else:
        return {"status_code": response.status_code, "error": response.text}


def start_trial(cookie):
    import requests

    url = "https://alpha.kite.com/web/account/start-trial"

    payload = ""
    headers = {'cookie': cookie}

    response = requests.request("GET", url, data=payload, headers=headers)

    return {"headers": response.headers, "status_code": response.status_code}


def get_licenses(cookie):
    import requests

    url = "https://alpha.kite.com/api/account/licenses"

    payload = ""
    headers = {'cookie': cookie}

    response = requests.request("GET", url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json()


def login(email, password):
    url = "https://alpha.kite.com/api/account/login"

    payload = f"-----011000010111000001101001\r\nContent-Disposition: form-data; " \
              f"name=\"email\"\r\n\r\n{email}\r\n-----011000010111000001101001\r\nContent-Disposition: " \
              f"form-data; name=\"password\"\r\n\r\n{password}\r\n-----011000010111000001101001--\r\n "
    headers = {
        'content-type': "multipart/form-data; boundary=---011000010111000001101001"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    return response
