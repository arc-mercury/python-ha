#!/bin/python

import ConfigParser
import MySQLdb
import base64
import requests

config = ConfigParser.RawConfigParser()
config.read('keys.conf')

db = MySQLdb.connect(host=config.get('DEFAULT','url'),
			user=config.get('DEFAULT','username'),
			passwd=config.get('DEFAULT','password'),
			db=config.get('DEFAULT','db'))

cur = db.cursor()

cur.execute("SELECT code.code FROM code order by creation_time DESC LIMIT 1;")

activekey = 'ERROR'

for row in cur.fetchall():
	activekey = row[0]

db.close()

appkey = config.get('HONEYWELL','apikey')
appsecret = config.get('HONEYWELL','apisecret')
decodedstring = appkey+":"+appsecret
b64key = base64.b64encode(decodedstring)

print b64key

r = requests.get("https://api.honeywell.com/oauth2/token", headers={'Authorization':'Basic '+b64key, 'Content-Type':'application/x-www-form-urlencoded'}, data={'grant_type':'authorization_code','code':activekey})

print(r.text)
