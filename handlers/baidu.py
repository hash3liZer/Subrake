import re
import threading
import requests
from bs4 import BeautifulSoup as soup

class BAIDU:

	COOKIES = None
	SERVICE = "Baidu"
	LOCK = threading.Semaphore(value=1)
	URL = "https://www.baidu.com/s?wd=site:%s&oq=site:%s"
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
		self.url = self.URL % (self.domain, self.domain)
		self.regexp = self.REGEXP % (self.domain)
		self.headers = self.headerer( self.HEADERS, self.AGENT )

	def headerer(self, headers, _ag):
		headers['User-Agent'] = _ag
		headers['Referer'] = self.url
		return headers

	def execute(self):
		_th = threading.Thread(target=self.request)
		_th.daemon = True
		_th.start()

	def request(self):
		self.baseclass.THREADS += 1

		try:
			req = self.session.get(self.url, headers=self.headers, cookies=self.COOKIES, timeout=self.TIMEOUT)
			if req.status_code < 400:
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
		_html = soup(self.RESPONSE, "lxml")
		for cite in _html.findAll("a", attrs={'class': 'c-showurl'}):
			sub = re.search(self.regexp, cite.text, re.IGNORECASE)
			if sub:
				_sub = sub.group()
				if _sub not in self.SUBDOMAINS:
					self.SUBDOMAINS.append(_sub)
