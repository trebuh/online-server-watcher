#! /usr/bin/env python3
# coding: utf-8

import sys
import time
import logging
from logging.handlers import RotatingFileHandler
import bs4
import requests
from config import log_params, watcher_params, request_header, sms_params

class OnlineWatcher:
    """ Checks the availability of a given list of servers at Online.net provider
        Sends a text message when a server is available
    """

    def __init__(self):

        formatter = logging.Formatter(log_params['line_format'])
        
        file_handler = RotatingFileHandler(log_params['file_path'], 'a', log_params['file_size'] , 1)
        file_handler.setFormatter(formatter)
        
        self.logger = logging.getLogger()
        self.logger.setLevel(log_params['level'])
        self.logger.addHandler(file_handler)
        

    def table_row_generator(self):
        parsing_request = requests.get(watcher_params['parsed_url'], headers=request_header)
        soup = bs4.BeautifulSoup(parsing_request.text, 'html5lib')
        parsing_result = [[td.text.strip() for td in tr.find_all('td')] for tr in soup.find_all('tr')]
    
        for element in parsing_result:
            if element:
                yield element
    
    
    def send_alert(self):
        sending_request = requests.post(sms_params['sms_url'], json=sms_params['payload'])
        if sending_request.status_code == requests.codes.ok:
            self.logger.info('Sent a notification: ' + sms_params['payload']['msg'])
        elif sending_request.status_code == requests.codes.bad_request:  # return code 400
            self.logger.error('Some parameters are missing in the request')
            sys.exit(1)
        elif sending_request.status_code == 402:
            self.logger.warning('Too many SMS sent. Will retry in 5 minutes')
        elif sending_request.status_code == requests.codes.forbidden:
            self.logger.error('Service disabled or wrong credentials')
            sys.exit(2)
        elif sending_request.status_code == requests.codes.server_error:
            self.logger.warning('Server error. Will retry in 5 minutes')
        else:
            self.logger.error('Unknown error, return code: ' + sending_request.status_code)
            sys.exit(3)
    
    
    def check_availability(self):
        for row in self.table_row_generator():
            if row[0] in watcher_params['watched_servers'] and row[5] != 'sur commande' \
                    and row[5] != 'victime de son succès':
                sms_params['payload']['msg'] = "Some new servers are available at " + watcher_params['parsed_url'] \
                    + ": " + row[5] + " server(s) " + row[0] + " remaining."
                self.send_alert()

    def start(self):
        while True:
            self.check_availability()
            time.sleep(watcher_params['sleep_time'])

def main():
    online_watcher = OnlineWatcher()
    online_watcher.start()

if __name__ == '__main__':
    main()
