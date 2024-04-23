from siteMonitor.siteMonitor import Url
from credentials import credentials
from os import environ
import argparse
from time import sleep
from datetime import datetime
from urllib.parse import urlparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog = "siteMonitor",
        description = "This script checks for changes to a website.",
    )
    parser.add_argument("Url", help = "The URL(s) you are interested in monitoring", type=str, nargs='+')
    parser.add_argument("-i", "--interval", help="The interval (in minutes) to wait between checks. Default is 30 minutes.", type=int, default=30)
    parser.add_argument("-c", "--capture", action="store_true", help="Include if you would like to save a copy of the website each time it changes.")
    parser.add_argument("-e", "--email", help="Recipient address if you would like to send an email")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    if args.email and credentials['email'] == '':
        try:
            credentials['email'] = environ['siteMonitor_email']
            credentials['password'] = environ['siteMonitor_password']
        except KeyError:
            print('Please input email credentials in the credentials.py file!\n'
                  'Alternatively, add them as environment variables: siteMonitor_email and siteMonitor_password')
            return

    list_of_url_objects = []
    for url in args.Url:
        if url[:4] != "http":
            url = "http://"+url
        name = urlparse(url).netloc
        list_of_url_objects.append(Url(url,output=args.capture, name=name))
    while True:
        for url in list_of_url_objects:
            changed = url.check_changes()
            if changed:
                print(f'{url.name} has changed at {datetime.now()}!')
            else:
                print(f'{url.name} is unchanged')
            if args.email:
                url.send_email(from_email=credentials['email'], from_password=credentials['password'], to_email=args.email)
        sleep(60*args.interval)

if __name__ == '__main__':
    main()
