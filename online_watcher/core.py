#! /usr/bin/env python3
# coding: utf-8

import sys
import time
import logging
import smtplib
from email.mime.text import MIMEText

try:
    import bs4
    import requests
except ImportError as e:
    requests = None
    bs4 = None
    print("Import error: %s" % str(e))
    sys.exit(129)
from .config import log_params, watcher_params, request_header, sms_params, \
    email_params


class OnlineWatcher:
    """ Checks the availability of a given list of servers at Online.net provider
        Sends an alert when a server is available(using e-mail or text message)
    """

    def __init__(self):

        formatter = logging.Formatter(log_params['line_format'])

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger = logging.getLogger("OnlineWatcherLogger")
        self.logger.setLevel(log_params['level'])
        self.logger.addHandler(console_handler)

    @staticmethod
    def table_row_generator():
        parsing_request = requests.get(watcher_params['parsed_url'],
                                       headers=request_header)
        soup = bs4.BeautifulSoup(parsing_request.text, 'html5lib')
        parsing_result = [[td.text.strip() for td in tr.find_all('td')] for tr
                          in soup.find_all('tr')]

        for element in parsing_result:
            if element:
                yield element

    def send_text(self, msg):
        sms_params['payload']['msg'] = msg
        sending_request = requests.post(sms_params['sms_url'],
                                        json=sms_params['payload'])
        if sending_request.status_code == requests.codes.ok:
            self.logger.info(
                'Sent a notification: ' + sms_params['payload']['msg'])
        elif sending_request.status_code == requests.codes.bad_request:
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
            self.logger.error(
                'Unknown error, return code: ' + sending_request.status_code)
            sys.exit(3)

    def send_email(self, msg):
        email = MIMEText(msg)
        email['Subject'] = 'New servers available at Online.net'
        email['From'] = email_params['from']
        email['To'] = email_params['to']
        smtp_server = None
        try:
            smtp_server = smtplib.SMTP(email_params['smtp_address'])
            if email_params['use_auth'] and smtp_server.has_extn('STARTTLS'):
                smtp_server.starttls()
                smtp_server.login(email_params['login'],
                                  email_params['password'])
            smtp_server.send_message(email)
        except smtplib.socket.gaierror:
            self.logger.error(
                'Could not connect to ' + email_params['smtp_address'])
            sys.exit(4)
        except smtplib.SMTPAuthenticationError:
            self.logger.error(
                'Authentication error, wrong credentials for user ' +
                email_params['login'])
            sys.exit(5)
        except smtplib.SMTPException as err:
            self.logger.error(
                'An error occurred during the sending of the email ' + str(err))
            sys.exit(6)
        finally:
            if smtp_server:
                smtp_server.quit()

    def send_alert(self, msg):
        if watcher_params['alert_via_text']:
            self.send_text(msg)
        else:
            self.send_email(msg)

    def check_availability(self):
        for row in self.table_row_generator():
            if row[0] in watcher_params['watched_servers'] and row[
                5] != 'sur commande' \
                    and row[5] != 'victime de son succès':
                msg = "Some new servers are available at " \
                      + watcher_params['parsed_url'] + ": " + row[5] \
                      + " server(s) " + row[0] + " remaining."
                self.send_alert(msg)

    def start(self):
        while True:
            try:
                self.check_availability()
                time.sleep(watcher_params['sleep_time'])
            except KeyboardInterrupt:
                self.logger.info('Keyboard Interrupt detected, exiting')
                sys.exit(7)
