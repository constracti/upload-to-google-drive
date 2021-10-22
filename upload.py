#!/usr/bin/python3

import argparse
import json
import mimetypes
import os.path
import requests

parser = argparse.ArgumentParser()
parser.add_argument('file', metavar='FILE')
parser.add_argument('folder', metavar='FOLDER_ID')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

file_path = args.file
file_obj = open(file_path, mode='rb')
file_name = os.path.basename(file_path)
file_mime_type = mimetypes.guess_type(file_path)[0]


### client secret ###

client = None
with open('client_secret.json', 'r') as f:
	client = json.load(f)
assert client is not None and 'installed' in client
client = client['installed']

assert 'client_id' in client
if args.verbose:
	print('=== client id ===')
	print(client['client_id'])
	print()

assert 'client_secret' in client
if args.verbose:
	print('=== client secret ===')
	print(client['client_secret'])
	print()


### refresh token ###

refresh_token = None
refresh_path = 'refresh_token.txt'
with open(refresh_path, mode='r') as f:
	refresh_token = f.read().rstrip()

if args.verbose:
	print('=== refresh token ===')
	print(refresh_token)
	print()


### access token ###

r = requests.post('https://accounts.google.com/o/oauth2/token', data={
	'client_id': client['client_id'],
	'client_secret': client['client_secret'],
	'refresh_token': refresh_token,
	'grant_type': 'refresh_token',
})
r = r.json()
assert 'error' not in r, r['error_description']

access_token = r['access_token']
if args.verbose:
	print('=== access token ===')
	print(access_token)
	print()


### upload file ###

r = requests.post('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', files={
	'metadata': (
		None,
		json.dumps({
			'name': file_name,
			'parents': [
				args.folder,
			],
		}),
		'application/json; charset=UTF-8'
	),
	'file': (
		file_name,
		file_obj,
		file_mime_type,
	),
}, headers={
	'Authorization': 'Bearer ' + access_token,
})
r = r.json()
assert 'error' not in r, '{} - {}'.format(r['error']['code'], r['error']['message'])

if args.verbose:
	print('=== file id ===')
	print(r['id'])
	print()
