#!/usr/bin/env python
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
    'sleep_time': 300
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
