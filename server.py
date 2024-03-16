import http.server
import requests
import urllib.parse

from page import UploadToGoogleDrivePage


class UploadToGoogleDriveServer(http.server.BaseHTTPRequestHandler):

	def get_addr(self, path='/'):
		return 'http://{:s}:{:d}{:s}'.format(self.server.server_name, self.server.server_port, path)

	def get_client(self):
		return self.server.client

	def get_auth_url(self):
		"""
		Set authorization parameters
		https://developers.google.com/identity/protocols/oauth2/web-server#creatingclient
		Redirect to Google's OAuth 2.0 server
		https://developers.google.com/identity/protocols/oauth2/web-server#redirecting
		"""
		return 'https://accounts.google.com/o/oauth2/auth?' + urllib.parse.urlencode({
			'client_id': self.get_client()['client_id'],
			'scope': 'https://www.googleapis.com/auth/drive.file',
			'response_type': 'code',
			'redirect_uri': self.get_addr('/auth'),
		})

	def get_exch_url(self):
		"""
		Exchange authorization code for refresh and access tokens
		https://developers.google.com/identity/protocols/oauth2/web-server#exchange-authorization-code
		"""
		return 'https://oauth2.googleapis.com/token'

	def get_exch_data(self, code):
		"""
		Exchange authorization code for refresh and access tokens
		https://developers.google.com/identity/protocols/oauth2/web-server#exchange-authorization-code
		"""
		return {
			'client_id': self.get_client()['client_id'],
			'client_secret': self.get_client()['client_secret'],
			'code': code,
			'grant_type': 'authorization_code',
			'redirect_uri': self.get_addr('/auth'),
		}

	def redirect(self, url):
		self.send_response(307)
		self.send_header('Location', url)
		self.end_headers()

	def alert(self, message):
		page = UploadToGoogleDrivePage()
		page.add_body_tag('<p>{:s}</p>'.format(message))
		html = page.get_html()
		self.send_response(200)
		self.send_header('Content-Type', 'text/html')
		self.end_headers()
		self.wfile.write(bytes(html, 'utf-8'))

	def do_GET(self):
		path = urllib.parse.urlparse(self.path)
		try:
			if path.path == '/init':
				self.redirect(self.get_auth_url())
			elif path.path == '/auth':
				query = urllib.parse.parse_qs(path.query, True)
				assert 'error' not in query, query['error'][0]
				code = query['code'][0]
				self.log_message('authorization code: ' + code)
				r = requests.post(self.get_exch_url(), data=self.get_exch_data(code))
				r = r.json()
				assert 'error' not in r, r['error_description']
				refresh_token = r['refresh_token']
				self.log_message('refresh token: ' + refresh_token)
				self.server.callback(refresh_token)
				self.redirect(self.get_addr('/over'))
			elif path.path == '/over':
				self.alert('Close this tab. Then return to the application and press Ctrl+C.')
		except Exception as e:
			error = str(e)
			self.log_error(error)
			self.alert('Error: {:s}</p>\n'.format(error))
