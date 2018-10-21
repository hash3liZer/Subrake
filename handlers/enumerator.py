import socket
import sys
import re

class PULLER:

	CODE = 'ERR'
	SERVER = 'NONE'

	def __init__(self, _dm, _head):
		self.headers = _head
		self.subdomain = _dm
		self.simplify(_head)

	def simplify(self, _hd):
		for ln in _hd.splitlines():
			if ln.startswith("HTTP/"):
				self.CODE = ln.split(" ")[1]
			elif ln.startswith("Server:"):
				_sv = ln.split(": ")[1].strip("\r")
				self.SERVER = _sv.split(" ")[0].split("/")[0]

class GOOGLE:

	LINKS = []
	SUBS = {}
	REQ = "GET /search?q=site:%s&num=50\r\nHost: %s\r\nUser-Agent: %s\r\n\r\n\r\n"
	REG = "([a-z0-9]+[.])*%s"
	RESPONSE = ""

	def __init__(self, _dm, _agent):
		self.domain = _dm
		self.agent = _agent
		self.REQ = self.REQ % (self.domain, "www.google.com", self.agent)
		self.REG = self.REG % (self.domain)

	def send(self):
		_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		_sock.settimeout(20)
		try:
			_sock.connect( ("www.google.com", 80) )
			_sock.send(self.REQ)
			_res = _sock.recv(4048)
			while _res != "":
				self.RESPONSE += _res
				_res = ""
				_res = _sock.recv(4048)
		except socket.error, e:
			print e
			sys.exit()

	def read(self):
		if "\r\n\r\n" in self.RESPONSE:
			_halves = self.RESPONSE.split("\r\n\r\n")
			return (_halves[0], _halves[1])
		return ( str(), str() ) 

	def collect(self, _cite):
		_reg = re.search(self.REG, _cite, re.I)
		if _reg:
			if _reg.group() not in self.LINKS:
				self.LINKS.append( _reg.group() )

	def subdomains(self):
		return self.LINKS

	def request(self, _sb, _port, _agent):
		_req = b"GET / HTTP/1.1\r\nHost: %s.com\r\nUser-Agent: %s\r\n\r\n" % (_sb, _agent)
		_to_push = ( "ERR", "NONE" )
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		s.settimeout(5)
		try:
			s.connect((_sb, _port))
			s.send(_req)
			_res = s.recv(1024)
			while True:
 				if "\r\n\r\n" in _res:
 					s.close()
 					_sold = PULLER( _sb, _res.split("\r\n\r\n")[0] )
 					_to_push = (_sold.CODE, _sold.SERVER)
 					break
 				else:
					_res = s.recv(1024)
		except socket.error:
			s.close()
		return _to_push

class BINGER:

	LINKS = []
	SUBS = {}
	REQ = "GET /search?q=site:%s\r\nHost: %s\r\nUser-Agent: %s\r\n\r\n"
	REG = "([a-z0-9]+[.])*%s"
	RESPONSE = ""

	def __init__(self, _dm, _agent):
		self.domain = _dm
		self.agent = _agent
		self.REQ = self.REQ % (self.domain, "www.bing.com", self.agent)
		self.REG = self.REG % (self.domain)

	def send(self):
		_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		_sock.settimeout(20)
		try:
			_sock.connect( ("www.bing.com", 80) )
			_sock.send(self.REQ)
			_res = _sock.recv(4048)
			while _res != "":
				self.RESPONSE += _res
				_res = ""
				_res = _sock.recv(4048)
		except socket.error, e:
			print e
			sys.exit()

	def read(self):
		if "\r\n\r\n" in self.RESPONSE:
			_halves = self.RESPONSE.split("\r\n\r\n")
			return (_halves[0], _halves[1])
		return ( str(), str() ) 

	def collect(self, _cite):
		_reg = re.search(self.REG, _cite, re.I)
		if _reg:
			if _reg.group() not in self.LINKS:
				self.LINKS.append( _reg.group() )

	def subdomains(self):
		return self.LINKS

	def request(self, _sb, _port, _agent):
		_req = b"GET / HTTP/1.1\r\nHost: %s.com\r\nUser-Agent: %s\r\n\r\n" % (_sb, _agent)
		_to_push = ( "ERR", "NONE" )
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		s.settimeout(5)
		try:
			s.connect((_sb, _port))
			s.send(_req)
			_res = s.recv(1024)
			while True:
 				if "\r\n\r\n" in _res:
 					s.close()
 					_sold = PULLER( _sb, _res.split("\r\n\r\n")[0] )
 					_to_push = (_sold.CODE, _sold.SERVER)
 					break
 				else:
					_res = s.recv(1024)
		except socket.error:
			s.close()
		return _to_push

