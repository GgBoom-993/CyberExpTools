import optparse
import random
import sys

RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
YEL = "\033[93m"

def display_banner():

    print("   ______      __             "+RED+" ______         "+RESET+"______            __    ")
    print("  / ____/_  __/ /_  ___  _____"+RED+"/ ____/  ______"+RESET+"/_  __/___  ____  / /____")
    print(" / /   / / / / __ \\/ _ \\/ ___"+RED+"/ __/ | |/_/ __ \\"+RESET+"/ / / __ \\/ __ \\/ / ___/")
    print("/ /___/ /_/ / /_/ /  __/ /  "+RED+"/ /____>  </ /_/ /  "+RESET+"// /_/ / /_/ / (__  ) ")
    print("\\____/\\__, /_.___/\\___/_/ "+RED+" /_____/_/|_/ .___/"+RESET+"_/  \\____/\\____/_/____/  ")
    print("     /____/            "+RED+"              /_/    "+RESET+"                          ")
    print("                                           CyberExpTools v1.0.0")
    print("                                           by ggboom993\n ")


    print(BLUE+"Vulnerability List:"+RESET+"\n"+YEL+
          "- HTTP Strict Transport Security Not Enforced\n"
          "- Cross-Origin Resource Sharing\n"
          "- Unencrypted Connection\n"
          "- Unnecessary HTTP Methods Enabled on Server\n"
          "- Clickjacking: X-Frame-Options Header Missing\n"
          "- Content-Security-Policy Header Missing\n"
          "- Server Header Disclosure\n"
          "- Server Information Revealed\n"
          "- Server Information Revealed (X-ASP.net-Version)\n"
          "- Weak SSL Version (TLS v1.0/ TLS v1.1/)\n"
          "- Cookie(s) without HttpOnly Flag Set\n"
          "- Cookie(s) without Secure Flag Set\n"+RESET
          )


usage="""
        python %prog -u https://www.target.com
        python %prog -f urls.txt
"""




parser=optparse.OptionParser(usage,
                             description="",
                             version="version: %prog v1.0.0",
                             epilog="-"*60)



parser.add_option('-u','--url', dest='url',help='target url')
parser.add_option('-f','--urls', dest='urls',help='target url file, one in a line')
options,args=parser.parse_args()



def parse_args():
    help_text = parser.format_help()
    colored_help_text = help_text.replace("Options:", f"{BLUE}Options:{RESET}")
    colored_help_text2 = colored_help_text.replace("Usage:", f"{BLUE}Usage:{RESET}")
    if random.randint(1,2)==1:
        display_banner()

    else:
        display_banner()

    if options.url==None and options.urls==None:
        print(colored_help_text2)
        sys.exit()
    return options
