#!/usr/bin/python3

import json
import requests
import urllib.parse

client = None
with open('client_secret.json', 'r') as f:
	client = json.load(f)
assert client is not None and 'installed' in client
client = client['installed']

assert 'client_id' in client
print('=== client id ===')
print(client['client_id'])
print()

assert 'client_secret' in client
print('=== client secret ===')
print(client['client_secret'])
print()

print('=== url ===')
print('https://accounts.google.com/o/oauth2/auth?' + urllib.parse.urlencode({
	'client_id': client['client_id'],
	'scope': 'https://www.googleapis.com/auth/drive.file',
	'response_type': 'code',
	'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
}))
print()

code = input('code: ')
print()
print('=== code ===')
print(code)
print()

r = requests.post('https://oauth2.googleapis.com/token', data={
	'client_id': client['client_id'],
	'client_secret': client['client_secret'],
	'code': code,
	'grant_type': 'authorization_code',
	'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
})
r = r.json()
assert 'error' not in r, r['error_description']

refresh_token = r['refresh_token']
print('=== refresh token ===')
print(refresh_token)
print()

refresh_path = 'refresh_token.txt'
with open(refresh_path, mode='w') as f:
	f.write(refresh_token + '\n')