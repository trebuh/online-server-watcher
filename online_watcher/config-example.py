#!/usr/bin/env python3
# coding: utf-8

import logging

log_params = {
    'line_format': '[%(asctime)s][%(levelname)s] %(message)s',
    'file_path': 'online_watcher.log',
    'file_size': 1000000, # 1 MB
    'level': logging.DEBUG
}

watcher_params = {
    'parsed_url': 'https://console.online.net/fr/order/server',
    'watched_servers': ['Dedibox XC SATA 2016', 'Dedibox XC SSD 2015'],
    'sleep_time': 300,
    'alert_via_text': False
}

request_header = {
    'User-agent': 'Mozilla/5.0'
}

sms_params = {
    'sms_url': 'https://smsapi.free-mobile.fr/sendmsg',
    'payload': {
        'user': '123456',
        'pass': 'ABCDEF',
        'msg': ''
    }
}
email_params = {
    'smtp_address': 'smtp.your_provider.com:25',
    'use_auth': True,
    'login': 'your_login',  # Used only if use_auth is True
    'password': 'secret',   # Used only if use_auth is True
    'from': 'your_email@your_provider.com',
    'to': 'your_email@your_provider.com'
}

