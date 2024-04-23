import requests
from time import sleep
import os
from datetime import datetime
from fake_headers import Headers
import smtplib
from email.mime.text import MIMEText

class Url:
    '''
    Defines a URL to be monitored
    Parameters:
        output (bool): Flag whether to save each web capture
        name (str): Name of output folder

    Methods -> Bool:
        check_changes: Captures & hashes URL. Adds to a set of hashes.
            If new hash not in set, returns True.
            tAscii(text):
    f = Figlet(font='slant')
    print(f.renderText(First run always returns False
        send_email: Sends an email when

    '''
    def __init__(self, target_url, output=True, name='Default') -> None:
        self.url = target_url
        self.name = name
        self.hash = None
        self.oldhashes = []
        self.changed = False
        self.current_site = None
        self.output = output

    def check_changes(self) -> bool:
        header_generator = Headers(os="win", browser='chrome', headers=True)
        # headers = header_generator.generate()
        headers = {'Accept-Language': 'en-US,en;q=0.5','User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0'}
        self.current_site = requests.get(self.url, headers = headers)
        self.hash = self.current_site.text.__hash__()

        if self.hash in self.oldhashes:
            self.changed = False
        elif self.oldhashes == []:
            self.changed = False
        else:
            self.changed = True

        if self.hash not in self.oldhashes:
            self.oldhashes.append(self.hash)

        if self.output == True:
            if self.changed == True or self.oldhashes == []:
                if os.path.exists("web output") == False:
                    os.mkdir('web output')
                if os.path.exists(f'web output/{self.name}') == False:
                    os.mkdir(f'web output/{self.name}')
                open(f'web output/{self.name}/{datetime.now()}.html', 'w').write(self.current_site.text)

        if self.changed == True:
            return True
        else:
            return False
        
    def send_email(self, on_change = True, from_email = 'example@gmail.com', from_password = 'example', to_email='example@example.com'):
        if on_change == True and self.changed == False:
            return
        email_content = \
        f'''
        The content on {self.name} has changed!\n
        \n
        To view the changes, please click here: {self.url}\n
        \n
        Time of change: {datetime.now()}
        '''
        email = MIMEText(email_content)
        email['From'] = from_email
        email['To'] = to_email
        email['Subject'] = \
        f'''
        siteMonitor Alert: {self.name}
        '''
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com',465)
            server.ehlo()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, email.as_string())
            server.close()
            # print(f'Email sent at {datetime.now()}')
        except:
            print(f'Email failed to send at {datetime.now()}')

# Test script
# abc_news = Url('https://www.abc.net.au/news', name='abc news')
# abc_news.check_changes()
# sleep(30)
# abc_news.check_changes()
