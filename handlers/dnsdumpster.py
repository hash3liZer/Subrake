import re
import threading
import requests
import hashlib
import urllib

class DNSDUMPSTER:

	COOKIES = {'csrftoken' : ''}
	DATA = {'csrfmiddlewaretoken' : '', 'targettip': ''}
	SERVICE = "DNSDumpster"
	LOCK = threading.Semaphore(value=1)
	URL = "https://dnsdumpster.com"
	REGEXP = "([a-z0-9]+[.])+%s"
	TIMEOUT = 10
	RESPONSE = ""
	SUBDOMAINS = []
	AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
	HEADERS = {
		'User-Agent' : '',
		'Referer' : '',
	}

	def __init__(self, _class, _dm):
		self.session = requests.Session()
		self.baseclass = _class
		self.domain = _dm
		self.DATA['targettip'] = self.domain
		self.regexp = self.REGEXP % (self.domain)
		self.headers = self.headerer( self.HEADERS, self.AGENT )

	def headerer(self, headers, _ag):
		headers['User-Agent'] = _ag
		headers['Referer'] = "https://dnsdumpster.com"
		headers['Origin'] = "https://dnsdumpster.com"
		return headers

	def acquire_csrf(self, html):
		obj = re.search(r"<input type='hidden' name='csrfmiddlewaretoken' value='(.*?)' />", html, re.IGNORECASE)
		if obj:
			return obj.groups()[0]

	def execute(self):
		_th = threading.Thread(target=self.request)
		_th.daemon = True
		_th.start()

	def request(self):
		self.baseclass.THREADS += 1

		try:
			req = self.session.get(self.URL, headers=self.headers, timeout=self.TIMEOUT)
			if req.status_code < 400:
				csrf = self.acquire_csrf(req.text)
				self.COOKIES['csrftoken'] = csrf
				self.DATA['csrfmiddlewaretoken'] = csrf
				req = self.session.post(self.URL, data=self.DATA, cookies=self.COOKIES, headers=self.headers, timeout=self.TIMEOUT)
				self.RESPONSE = req.text
				self.extract()
				self.append()

		except Exception as e:
			self.append()

		self.baseclass.THREADS -= 1

	def append(self, error=False):
		self.LOCK.acquire()
		self.baseclass.move( self.SERVICE, self.SUBDOMAINS )
		self.LOCK.release()

	def extract(self):
		links = re.findall(r"<td class=\"col-md-4\">(.*?)<br>", self.RESPONSE)
		for link in links:
			if link.endswith(self.domain):
				if link not in self.SUBDOMAINS:
					self.SUBDOMAINS.append(link)
