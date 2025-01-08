import requests, os, time, sys
import configparser, hashlib, hmac, platform
import json as jsond
import concurrent.futures as threading
import win32security
import string
import email.message as email
import ctypes
import smtplib
import re
import base64
from random import *
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from colorama import Fore, Style, Back, init
from uuid import uuid4
from datetime import datetime as waktu
from colorama import init, Fore, Style


init()
ctypes.windll.kernel32.SetConsoleTitleW('ZEROBOUNCER V4.0 | BY @Killo_Trojanz2')

red = Fore.RED
cyan = Fore.CYAN
magenta = Fore.MAGENTA
white = Fore.WHITE
yellow = Fore.YELLOW
blue = Fore.BLUE
green = Fore.GREEN
reset = Fore.RESET
normal = Style.NORMAL
bright = Style.BRIGHT


""" main function """
def clscr():
    os.system("cls") if os.name == "nt" else os.system("clear")

def printRes(mail, isvalid=False):
    if isvalid:
        validity = Fore.GREEN + "VALID LEADS" + Fore.WHITE
    else:
        validity = Fore.RED + "INVALID LEADS" + Fore.WHITE
    bracop = Fore.LIGHTMAGENTA_EX + "["
    braclo = Fore.LIGHTMAGENTA_EX + "]"
    strips = ""
    msg = bracop + Fore.GREEN + waktu.now().strftime("%H:%M:%S") + braclo + "╾┄╼" +bracop + Fore.GREEN + "ZEROBOUNCER V4.2" + braclo + "╾┄╼" + bracop + Fore.LIGHTWHITE_EX + mail + braclo + "╾┄╼" + bracop + validity + braclo + Fore.WHITE
    print("                                              " + msg)

def writeRes(mail, islive=False):
    patha = "ZeroBouncer/"
    today = date.today().strftime("%d-%m-%Y")

    if islive:
        patha += "bouncermail-" + today + ".txt"
        with open(patha, 'a') as fp:
            fp.write(mail + "\n")
    else:
        patha += "deadmail-" + today + ".txt"
        with open(patha, 'a') as fp:
            fp.write(mail + "\n")

    pathb = "Shorted_Bouncer/"
    domail = mail.split('@')[1]
    
    if islive:
        pathb += domail + "_bouncer-" + today + ".txt"
        with open(pathb, 'a') as fp:
            fp.write(mail + "\n")

def getchecksum():
    md5_hash = hashlib.md5()
    file = open(''.join(sys.argv), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest

class api:

    name = ownerid = secret = version = hash_to_check = ""

    def __init__(self, name, ownerid, secret, version, hash_to_check):
        if len(ownerid) != 10 and len(secret) != 64:
            print("Go to Manage Applications on dashboard, copy python code, and replace code in main.py with that")
            time.sleep(3)
            os._exit(1)
    
        self.name = name

        self.ownerid = ownerid

        self.secret = secret

        self.version = version
        self.hash_to_check = hash_to_check
        self.init()

    sessionid = enckey = ""
    initialized = False

    def init(self):
        if self.sessionid != "":
            print("You've already initialized!")
            time.sleep(3)
            os._exit(1)

        sent_key = str(uuid4())[:16]
        
        self.enckey = sent_key + "-" + self.secret
        
        post_data = {
            "type": "init",
            "ver": self.version,
            "hash": self.hash_to_check,
            "enckey": sent_key,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        if response == "KeyAuth_Invalid":
            print("The application doesn't exist")
            time.sleep(3)
            os._exit(1)

        json = jsond.loads(response)

        if json["message"] == "invalidver":
            if json["download"] != "":
                print("New Version Available")
                download_link = json["download"]
                os.system(f"start {download_link}")
                time.sleep(3)
                os._exit(1)
            else:
                print("Invalid Version, Contact owner to add download link to latest app version")
                time.sleep(3)
                os._exit(1)

        if not json["success"]:
            print(json["message"])
            time.sleep(3)
            os._exit(1)

        self.sessionid = json["sessionid"]
        self.initialized = True
        
        if json["newSession"]:
            time.sleep(0.1)

    def register(self, user, password, license, hwid=None):
        self.checkinit()
        if hwid is None:
            hwid = others.get_hwid()

        post_data = {
            "type": "register",
            "username": user,
            "pass": password,
            "key": license,
            "hwid": hwid,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            print(json["message"])
            self.__load_user_data(json["info"])
        else:
            print(json["message"])
            time.sleep(3)
            os._exit(1)

    def upgrade(self, user, license):
        self.checkinit()

        post_data = {
            "type": "upgrade",
            "username": user,
            "key": license,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            print(json["message"])
            print("Please restart program and login")
            time.sleep(3)
            os._exit(1)
        else:
            print(json["message"])
            time.sleep(3)
            os._exit(1)

    def login(self, user, password, hwid=None):
        self.checkinit()
        if hwid is None:
            hwid = others.get_hwid()

        post_data = {
            "type": "login",
            "username": user,
            "pass": password,
            "hwid": hwid,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            self.__load_user_data(json["info"])
            print(json["message"])
        else:
            print(json["message"])
            time.sleep(3)
            os._exit(1)

    def license(self, key, hwid=None):
        self.checkinit()
        if hwid is None:
            hwid = others.get_hwid()

        post_data = {
            "type": "license",
            "key": key,
            "hwid": hwid,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            self.__load_user_data(json["info"])
            #print(json["message"])
        else:
            clscr()
            print(BANNER_ERROR)
            print(f"                                                 {Fore.WHITE}Msg: {Fore.RED}" + json["message"] + f"{Style.RESET_ALL}")
            time.sleep(3)
            os._exit(1)

    def var(self, name):
        self.checkinit()

        post_data = {
            "type": "var",
            "varid": name,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            return json["message"]
        else:
            print(json["message"])
            time.sleep(3)
            os._exit(1)

    def getvar(self, var_name):
        self.checkinit()

        post_data = {
            "type": "getvar",
            "var": var_name,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }
        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            return json["response"]
        else:
            print(f"NOTE: This is commonly misunderstood. This is for user variables, not the normal variables.\nUse keyauthapp.var(\"{var_name}\") for normal variables");
            print(json["message"])
            time.sleep(3)
            os._exit(1)

    def setvar(self, var_name, var_data):
        self.checkinit()

        post_data = {
            "type": "setvar",
            "var": var_name,
            "data": var_data,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }
        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            return True
        else:
            print(json["message"])
            time.sleep(3)
            os._exit(1)

    def ban(self):
        self.checkinit()

        post_data = {
            "type": "ban",
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }
        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            return True
        else:
            print(json["message"])
            time.sleep(3)
            os._exit(1)

    def file(self, fileid):
        self.checkinit()

        post_data = {
            "type": "file",
            "fileid": fileid,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if not json["success"]:
            print(json["message"])
            time.sleep(3)
            os._exit(1)
        return binascii.unhexlify(json["contents"])

    def webhook(self, webid, param, body = "", conttype = ""):
        self.checkinit()

        post_data = {
            "type": "webhook",
            "webid": webid,
            "params": param,
            "body": body,
            "conttype": conttype,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            return json["message"]
        else:
            print(json["message"])
            time.sleep(3)
            os._exit(1)

    def check(self):
        self.checkinit()

        post_data = {
            "type": "check",
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }
        response = self.__do_request(post_data)

        json = jsond.loads(response)
        if json["success"]:
            return True
        else:
            return False

    def checkblacklist(self):
        self.checkinit()
        hwid = others.get_hwid()

        post_data = {
            "type": "checkblacklist",
            "hwid": hwid,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }
        response = self.__do_request(post_data)

        json = jsond.loads(response)
        if json["success"]:
            return True
        else:
            return False

    def log(self, message):
        self.checkinit()

        post_data = {
            "type": "log",
            "pcuser": os.getenv('username'),
            "message": message,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        self.__do_request(post_data)

    def fetchOnline(self):
        self.checkinit()

        post_data = {
            "type": "fetchOnline",
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            if len(json["users"]) == 0:
                return None
            else:
                return json["users"]
        else:
            return None
            
    def fetchStats(self):
        self.checkinit()

        post_data = {
            "type": "fetchStats",
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            self.__load_app_data(json["appinfo"])
            
    def chatGet(self, channel):
        self.checkinit()

        post_data = {
            "type": "chatget",
            "channel": channel,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            return json["messages"]
        else:
            return None

    def chatSend(self, message, channel):
        self.checkinit()

        post_data = {
            "type": "chatsend",
            "message": message,
            "channel": channel,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            return True
        else:
            return False

    def checkinit(self):
        if not self.initialized:
            print("Initialize first, in order to use the functions")
            time.sleep(3)
            os._exit(1)

    def changeUsername(self, username):
        self.checkinit()

        post_data = {
            "type": "changeUsername",
            "newUsername": username,
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            print("Successfully changed username")
        else:
            print(json["message"])
            time.sleep(3)
            os._exit(1)  

    def logout(self):
        self.checkinit()

        post_data = {
            "type": "logout",
            "sessionid": self.sessionid,
            "name": self.name,
            "ownerid": self.ownerid
        }

        response = self.__do_request(post_data)

        json = jsond.loads(response)

        if json["success"]:
            print("Successfully logged out")
            time.sleep(3)
            os._exit(1)
        else:
            print(json["message"])
            time.sleep(3)
            os._exit(1)         
            
    def __do_request(self, post_data):
        try:
            response = requests.post(
                "https://keyauth.win/api/1.2/", data=post_data, timeout=10
            )
            
            key = self.secret if post_data["type"] == "init" else self.enckey
            if post_data["type"] == "log": return response.text
                        
            client_computed = hmac.new(key.encode('utf-8'), response.text.encode('utf-8'), hashlib.sha256).hexdigest()
            
            signature = response.headers["signature"]
            
            if not hmac.compare_digest(client_computed, signature):
                print("Signature checksum failed. Request was tampered with or session ended most likely.")
                print("Response: " + response.text)
                time.sleep(3)
                os._exit(1) 
            
            return response.text
        except requests.exceptions.Timeout:
            print("Request timed out. Server is probably down/slow at the moment")

    class application_data_class:
        numUsers = numKeys = app_ver = customer_panel = onlineUsers = ""

    class user_data_class:
        username = ip = hwid = expires = createdate = lastlogin = subscription = subscriptions = ""

    user_data = user_data_class()
    app_data = application_data_class()

    def __load_app_data(self, data):
        self.app_data.numUsers = data["numUsers"]
        self.app_data.numKeys = data["numKeys"]
        self.app_data.app_ver = data["version"]
        self.app_data.customer_panel = data["customerPanelLink"]
        self.app_data.onlineUsers = data["numOnlineUsers"]

    def __load_user_data(self, data):
        self.user_data.username = data["username"]
        self.user_data.ip = data["ip"]
        self.user_data.hwid = data["hwid"] or "N/A"
        self.user_data.expires = data["subscriptions"][0]["expiry"]
        self.user_data.createdate = data["createdate"]
        self.user_data.lastlogin = data["lastlogin"]
        self.user_data.subscription = data["subscriptions"][0]["subscription"]
        self.user_data.subscriptions = data["subscriptions"]

class others:
    @staticmethod
    def get_hwid():
        if platform.system() == "Linux":
            with open("/etc/machine-id") as f:
                hwid = f.read()
                return hwid
        elif platform.system() == 'Windows':
            winuser = os.getlogin()
            sid = win32security.LookupAccountName(None, winuser)[0]  # You can also use WMIC (better than SID, some users had problems with WMIC)
            hwid = win32security.ConvertSidToStringSid(sid)
            return hwid
            '''
            cmd = subprocess.Popen(
                "wmic useraccount where name='%username%' get sid",
                stdout=subprocess.PIPE,
                shell=True,
            )

            (suppost_sid, error) = cmd.communicate()

            suppost_sid = suppost_sid.split(b"\n")[1].strip()

            return suppost_sid.decode()

            ^^ HOW TO DO IT USING WMIC
            '''
        elif platform.system() == 'Darwin':
            output = subprocess.Popen("ioreg -l | grep IOPlatformSerialNumber", stdout=subprocess.PIPE, shell=True).communicate()[0]
            serial = output.decode().split('=', 1)[1].replace(' ', '')
            hwid = serial[1:-2]
            return hwid

BANNER_ERROR = f"""{Fore.RED}












                                                ███████╗██████╗ ██████╗  ██████╗ ██████╗     ██╗
                                                ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗    ██║
                                                █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝    ██║
                                                ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗    ╚═╝
                                                ███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║    ██╗
                                                ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝    ╚═╝
                                                
"""

""" setup config """
setting = configparser.ConfigParser()
try:
    setting.read('setting.ini')
    userlicense = setting['SETTINGS']['license_key']
except Exception as e:
    sys.exit('Setting file not found or corrupted')

pathsres = ["ZeroBouncer", "Shorted_Bouncer"]
for p in pathsres:
    if not os.path.exists(os.path.abspath(p)):
        os.makedirs(p)


print("""
    """)
time.sleep(0.2)

clscr()
print(f"""                           
{Fore.LIGHTMAGENTA_EX}












                                             ██████╗ ██████╗  ██████╗ ██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗███████╗██████╗ 
                                            ██╔═████╗██╔══██╗██╔═══██╗██║   ██║████╗  ██║██╔════╝██║  ██║██╔════╝██╔══██╗
                                            ██║██╔██║██████╔╝██║   ██║██║   ██║██╔██╗ ██║██║     ███████║█████╗  ██████╔╝
                                            ████╔╝██║██╔══██╗██║   ██║██║   ██║██║╚██╗██║██║     ██╔══██║██╔══╝  ██╔══██╗
                                            ╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║╚██████╗██║  ██║███████╗██║  ██║
                                             ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                                                                                                                                                 
                                               {Fore.LIGHTCYAN_EX}Developed By {Fore.LIGHTRED_EX}@killo_trojanz2 {Fore.LIGHTGREEN_EX}(telegram) {Fore.LIGHTYELLOW_EX}-{Fore.LIGHTMAGENTA_EX} ZEROBOUNCER V4.0 {Fore.LIGHTGREEN_EX}[PREMIUM API]                
                                                   {Fore.LIGHTMAGENTA_EX}Best Private Feature : {Fore.LIGHTYELLOW_EX}Unlimited Check {Fore.LIGHTWHITE_EX}+{Fore.LIGHTCYAN_EX} Leads Spamming Filter


                                                   ┬───────────────────────
                                                   └──╼{Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTCYAN_EX}LIFETIME LICENSE {Fore.LIGHTMAGENTA_EX}+{Fore.LIGHTCYAN_EX} OFFICIAL KEY{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTCYAN_EX}
                                                   ┬───────────────────────
                                                   └──╼{Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTCYAN_EX}Your License Saved On :{Fore.LIGHTGREEN_EX} setting.ini{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTCYAN_EX}
                                                   ┬───────────────────────
                                                   └──╼{Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTCYAN_EX}Your Payload & Headers :{Fore.LIGHTGREEN_EX} payloadheaders.ini{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTCYAN_EX}
                                                   ┬───────────────────────
                                                   └──╼{Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTCYAN_EX}Version Information  :{Fore.LIGHTGREEN_EX} V4.0 FULL UPDATE{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTCYAN_EX}



                                              ───────────────────────{Fore.LIGHTMAGENTA_EX}[CONFIGURATION BOUNCHER]{Fore.LIGHTCYAN_EX}───────────────────────
""")

def checker(maildata):
    datas = {"email": maildata}
    headers1 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
        'Cookie': '__cfduid=d7388b7b2c3df08e9c6dae21fb1ee29581612352407; .AspNetCore.Antiforgery.38G8fUVOpE4=CfDJ8JOdAoeLmM5PtcCdCER4YLc-DP0khUxXzfSsaC2yutkNRWhkAKqLeyl033-ADG943CkBB_fiO6YYhuMl6heGg2yq7TDThZDJNa86aM_VmxzXC2GeKvCjpvA1MsI8Tp5t-tTVGWOWbduaxRGDW4ZZNBc; .EmailHippo.Session=CfDJ8JOdAoeLmM5PtcCdCER4YLeIOlhBXA7evw0hlbusgaG3kCgjxTeT6iNn%2B%2Blwf6NOkqIeq9BEzELGNx8uyZmZWxuZqMmKdVeWnvH64IkoeshP6g97NNAhAfHxZJ0LIViTW%2BlB%2FM5flmvwWE%2FsIhuRAFuFk0UIzSr6bMyizUsPCt7t'}
    
    try:
        response = requests.post("https://tools.verifyemailaddress.io/", headers=headers1, data=datas).text
        if "OK" in response:
            printRes(maildata, True)
            writeRes(maildata, True)
        else:
            printRes(maildata)
            writeRes(maildata)
    except:
        pass

while True:
    try:
        listfile = input(f"""                                                  ╭{Fore.LIGHTMAGENTA_EX}╼{Fore.LIGHTCYAN_EX}{Fore.LIGHTCYAN_EX}{Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTCYAN_EX}ENTER YOUR LEADS - ZEROBOUNCER V4.2 PREMIUM{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTCYAN_EX}
                                                  |
                                                  ╰─────{Fore.LIGHTMAGENTA_EX}╼#{Fore.LIGHTWHITE_EX} """)
        break
    except:
        print("You Are Fool Bro!\n")

combo = []
threads = 100 if setting["SETTINGS"]["turbo_mode"].lower() == "y" else 1

with open(listfile, "r") as file:
    lines = file.readlines()
    for line in lines:
        line = line.rstrip()
        if line not in combo:
            combo.append(line)

keyauthapp = api(
    name = "0BOUNCHER",
    ownerid = "vV54MUrU3U",
    secret = "9213c720896e057464b2b4faf26b940fdffc31f29366338b273c8bdac9c149b1",
    version = "1.0",
    hash_to_check = getchecksum()
)
keyauthapp.license(userlicense)

if True:
    time.sleep(1.5)
    clscr()
    print(f"""                           
{Fore.LIGHTMAGENTA_EX}












                                             ██████╗ ██████╗  ██████╗ ██╗   ██╗███╗   ██╗ ██████╗██╗  ██╗███████╗██████╗ 
                                            ██╔═████╗██╔══██╗██╔═══██╗██║   ██║████╗  ██║██╔════╝██║  ██║██╔════╝██╔══██╗
                                            ██║██╔██║██████╔╝██║   ██║██║   ██║██╔██╗ ██║██║     ███████║█████╗  ██████╔╝
                                            ████╔╝██║██╔══██╗██║   ██║██║   ██║██║╚██╗██║██║     ██╔══██║██╔══╝  ██╔══██╗
                                            ╚██████╔╝██████╔╝╚██████╔╝╚██████╔╝██║ ╚████║╚██████╗██║  ██║███████╗██║  ██║
                                             ╚═════╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                                                                                                                                                                 
                                               {Fore.LIGHTCYAN_EX}Developed By {Fore.LIGHTRED_EX}@killo_trojanz2 {Fore.LIGHTGREEN_EX}(telegram) {Fore.LIGHTYELLOW_EX}-{Fore.LIGHTMAGENTA_EX} ZEROBOUNCER V4.0 {Fore.LIGHTGREEN_EX}[PREMIUM API]                
                                                   {Fore.LIGHTMAGENTA_EX}Best Private Feature : {Fore.LIGHTYELLOW_EX}Unlimited Check {Fore.LIGHTWHITE_EX}+{Fore.LIGHTCYAN_EX} Leads Spamming Filter


                                                   ┬───────────────────────
                                                   └──╼{Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTCYAN_EX}LIFETIME LICENSE {Fore.LIGHTMAGENTA_EX}+{Fore.LIGHTCYAN_EX} OFFICIAL KEY{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTCYAN_EX}
                                                   ┬───────────────────────
                                                   └──╼{Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTCYAN_EX}Your License Saved On :{Fore.LIGHTGREEN_EX} setting.ini{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTCYAN_EX}
                                                   ┬───────────────────────
                                                   └──╼{Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTCYAN_EX}Your Payload & Headers :{Fore.LIGHTGREEN_EX} payloadheaders.ini{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTCYAN_EX}
                                                   ┬───────────────────────
                                                   └──╼{Fore.LIGHTMAGENTA_EX}[{Fore.LIGHTCYAN_EX}Version Information  :{Fore.LIGHTGREEN_EX} V4.0 FULL UPDATE{Fore.LIGHTMAGENTA_EX}]{Fore.LIGHTCYAN_EX}



                                              ───────────────────────{Fore.LIGHTMAGENTA_EX}[STARTING BOUNCHER]{Fore.LIGHTCYAN_EX}───────────────────────
""")
    with threading.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(checker, combo)