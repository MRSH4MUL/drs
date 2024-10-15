import argparse
import random
import requests
from bs4 import BeautifulSoup
import os

os.system('clear')
# ASCII Banner
BANNER = r"""
  
   ██████╗ ██████╗ ███████╗██████╗ ██╗   ██╗
   ██╔══██╗██╔══██╗██╔════╝██╔══██╗╚██╗ ██╔╝
   ██║  ██║██████╔╝███████╗██████╔╝ ╚████╔╝
   ██║  ██║██╔══██╗╚════██║██╔═══╝   ╚██╔╝
   ██████╔╝██║  ██║███████║██║        ██║
   ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝        ╚═╝

    DrSpy performs Google Dork searches.
    Dev : MR SH4MUL
    Telegram : t.meDARKCYBER420
    Need help? use python drspy.py -h                                            

usage: drspy.py [-h] [-s SITE] [-int INTEXT] [-inu INURL] [-file FILETYPE]
                [-L LINK] [-us USERNAME] [-ph PHONE] [-loc LOCATION]
                [-desc DESCRIPTION] [-email EMAIL] [-dev DEVELOPER]
                [-devcode DEVCODE] [-key KEY] [-allinurl ALLINURL]
                [-allintitle ALLINTITLE] [-num NUMBER]

Google Dorks Search Script

options:
  -h, --help            show this help message and exit
  -s SITE, --site SITE  Site to search
  -int INTEXT, --intext INTEXT
                        Text to search in the content
  -inu INURL, --inurl INURL
                        Text to search in the URL
  -file FILETYPE, --filetype FILETYPE
                        File type to search
  -L LINK, --link LINK  Links to search
  -us USERNAME, --username USERNAME
                        Username to search
  -ph PHONE, --phone PHONE
                        Phone number to search
  -loc LOCATION, --location LOCATION
                        Location to search
  -desc DESCRIPTION, --description DESCRIPTION
                        Description to search
  -email EMAIL, --email EMAIL
                        Email to search
  -dev DEVELOPER, --developer DEVELOPER
                        Developer to search
  -devcode DEVCODE, --devcode DEVCODE
                        Devcode to search
  -key KEY, --key KEY   Key to search
  -allinurl ALLINURL, --allinurl ALLINURL
                        All in URL search
  -allintitle ALLINTITLE, --allintitle ALLINTITLE
                        All in title search
  -num NUMBER, --number NUMBER
                        Number to search                                               
"""

# Colors
RED = '\033[91m'
WHITE = '\033[97m'
LIGHT_BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# User Agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; Pixel 3 XL Build/PQ2A.190205.002) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36"
]

# Google Dork mappings
DORKS = {
    '-s': 'site:',
    '-int': 'intext:',
    '-inu': 'inurl:',
    '-file': 'filetype:',
    '-L': 'link:',
    '-us': 'username:',
    '-ph': 'phone number:',
    '-loc': 'location:',          # New Dork
    '-desc': 'description:',      # New Dork
    '-email': 'email:',           # New Dork
    '-dev': 'developer:',         # New Dork
    '-devcode': 'devcode:',       # New Dork
    '-key': 'key:',               # New Dork
    '-allinurl': 'allinurl:',     # New Dork
    '-allintitle': 'allintitle:',  # New Dork
    '-num': 'number:',            # New Dork
}

def parse_arguments():
    parser = argparse.ArgumentParser(description="Google Dorks Search Script")
    parser.add_argument('-s', '--site', type=str, help='Site to search')
    parser.add_argument('-int', '--intext', type=str, help='Text to search in the content')
    parser.add_argument('-inu', '--inurl', type=str, help='Text to search in the URL')
    parser.add_argument('-file', '--filetype', type=str, help='File type to search')
    parser.add_argument('-L', '--link', type=str, help='Links to search')
    parser.add_argument('-us', '--username', type=str, help='Username to search')
    parser.add_argument('-ph', '--phone', type=str, help='Phone number to search')
    parser.add_argument('-loc', '--location', type=str, help='Location to search')      # New argument
    parser.add_argument('-desc', '--description', type=str, help='Description to search')# New argument
    parser.add_argument('-email', '--email', type=str, help='Email to search')           # New argument
    parser.add_argument('-dev', '--developer', type=str, help='Developer to search')     # New argument
    parser.add_argument('-devcode', '--devcode', type=str, help='Devcode to search')     # New argument
    parser.add_argument('-key', '--key', type=str, help='Key to search')                 # New argument
    parser.add_argument('-allinurl', '--allinurl', type=str, help='All in URL search')   # New argument
    parser.add_argument('-allintitle', '--allintitle', type=str, help='All in title search') # New argument
    parser.add_argument('-num', '--number', type=str, help='Number to search')            # New argument

    return parser.parse_args()

def construct_search_query(args):
    query_parts = []

    for flag, dork in DORKS.items():
        value = getattr(args, dork.replace(':', ''), None)
        if value:
            if isinstance(value, str):
                query_parts.append(f'{dork} {value}')
            else:
                query_parts.append(dork)

    return ' '.join(query_parts)

def search_google(query):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    url = f'https://www.google.com/search?q={query}'
    
    # Replace with a fake IP address (for illustration, using random IP)
    ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"{RED}Error fetching results: {e}{RESET}")
        return None

def parse_results(html):
    soup = BeautifulSoup(html, 'html.parser')
    results = []
    
    for g in soup.find_all('div', class_='g'):
        title = g.find('h3').text if g.find('h3') else 'No title'
        link = g.find('a')['href'] if g.find('a') else 'No link'
        results.append((title, link))

    return results

def save_results(results):
    with open('results.txt', 'w') as file:
        for title, link in results:
            file.write(f"{title}\n{link}\n\n")
    print(f"{LIGHT_BLUE}Results saved to results.txt{RESET}")

def main():
    print(f"{RED}{WHITE}{BANNER}{RESET}")
    args = parse_arguments()
    query = construct_search_query(args)
    
    if query:
        print(f"{LIGHT_BLUE}Searching for: {query}{RESET}")
        html = search_google(query)
        
        if html:
            results = parse_results(html)
            for title, link in results:
                print(f"{LIGHT_BLUE}{title}{RESET}\n{LIGHT_BLUE}{link}{RESET}\n")

            save = input(f"{GREEN}Do you want to save the results? (y/n): {RESET}")
            if save.lower() == 'y':
                save_results(results)

if __name__ == "__main__":
    main()
