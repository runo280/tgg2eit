# -*- coding: utf-8 -*-
import os
import configparser
import mutil

account_config = "config.ini"
cfg = configparser.RawConfigParser(allow_no_value=False)
cfg.read(account_config)

phone_number = cfg['one']['phone_number'] if mutil.is_offline() else os.environ['tgPhone']
password = cfg['one']['password'] if mutil.is_offline() else os.environ['tgPass']

api_id = cfg['one']['api_id'] if mutil.is_offline() else os.environ['apiId']
api_hash = cfg['one']['api_hash'] if mutil.is_offline() else os.environ['apiHash']

bot_token = cfg['one']['bot_token'] if mutil.is_offline() else os.environ['botToken']
channel_id = cfg['one']['channel_id'] if mutil.is_offline() else os.environ['peerId']
api_url = cfg['one']['api_url'] if mutil.is_offline() else os.environ['apiUrl']

replace_str = cfg['one']['replace_str'].split('^') if mutil.is_offline() else os.environ['replaceStr'].split('^')
target_peer = cfg['one']['target_peer'] if mutil.is_offline() else os.environ['targetPeer']

db_user = cfg['one']['db_user'] if mutil.is_offline() else os.environ['muser']
db_pass = cfg['one']['db_pass'] if mutil.is_offline() else os.environ['mpass']
db_domain = cfg['one']['db_domain'] if mutil.is_offline() else os.environ['murl']
