class UploadToDrivePage:

	def __init__(self):
		self.body_tags = []

	def add_body_tag(self, tag):
		self.body_tags.append(tag)

	def get_html(self):
		html = '<html>\n'
		html += '<head>\n'
		html += '<title>Upload to Drive</title>\n'
		html += '</head>\n'
		html += '<body>\n'
		html += '<h1>Upload to Drive</h1>\n'
		for tag in self.body_tags:
			html += tag
		html += '</body>\n'
		html += '</html>\n'
		return html
