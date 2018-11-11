import re
import threading
import requests
import urllib
import hashlib
from BeautifulSoup import BeautifulSoup as soup

class NETCRAFT:

	COOKIES = {}
	SERVICE = "NetCraft"
	LOCK = threading.Semaphore(value=1)
	URL = "https://searchdns.netcraft.com/?restriction=site+ends+with&host=%s"
	REGEXP = "([a-z0-9]+[.])+%s"
	TIMEOUT = 10
	RESPONSE = ""
	SUBDOMAINS = []

	def __init__(self, _class, _dm, _hd, _ag):
		self.session = requests.Session()
		self.baseclass = _class
		self.domain = _dm
		self.URL = self.URL % (self.domain)
		self.REGEXP = self.REGEXP % (self.domain)
		self.headers = self.headerer(_hd, _ag)
		self.agent = _ag

	def headerer(self, headers, _ag):
		headers['User-Agent'] = _ag
		headers['Referer'] = self.URL
		return headers

	def acquire_cookie(self, headers):
		if ("Set-Cookie" in headers) or ("set-cookie" in headers):
			challege = headers['Set-Cookie'].split("=")[1].split(";")[0]
			return urllib.unquote(challege.encode('utf-8'))

	def set_cookie(self, name, value):
		self.COOKIES[name] = hashlib.sha1(urllib.unquote(value.encode('utf-8'))).hexdigest()
		return value

	def execute(self):
		_th = threading.Thread(target=self.request)
		_th.daemon = True
		_th.start()

	def request(self):
		self.baseclass.THREADS += 1

		try:
			req = self.session.get(self.URL, headers=self.headers, cookies=self.COOKIES, timeout=self.TIMEOUT)
			if req.status_code < 400:
				cookie = self.acquire_cookie(req.headers)
				if cookie:
					self.set_cookie('netcraft_js_verification_response', cookie)
					req = self.session.get(self.URL, headers=self.headers, cookies=self.COOKIES, timeout=self.TIMEOUT)
					self.RESPONSE = req.text
					self.extract()
					self.append()

		except Exception, e:
			self.append()

		self.baseclass.THREADS -= 1

	def append(self, error=False):
		self.LOCK.acquire()
		self.baseclass.add( self.SUBDOMAINS, self.SERVICE )
		self.baseclass.pushtoscreen( self.SUBDOMAINS, self.SERVICE, error )
		self.LOCK.release()

	def extract(self):
		_html = soup(self.RESPONSE)
		for cite in _html.findAll("a"):
			sub = re.search(self.REGEXP, cite.text, re.IGNORECASE)
			if sub:
				self.SUBDOMAINS.append(sub.group())