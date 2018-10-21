#!/usr/bin/python

import optparse
import re
import os
import sys
import socket
import time
import threading
import signal
import dns.resolver
from pull import PULLY
from utils import USERAGENT
from out import TABULATOR
from handlers import GOOGLE 
from handlers import BINGER
from BeautifulSoup import BeautifulSoup as soup

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
				self.SERVER = _sv.split(" ")[0]

class CNAMES:

	__LIST = {}
	__CNAMES = {}

	def add(self, _lis):
		self.__LIST[_lis[-1]] = _lis[:-1]

	def count(self):
		return len(self.__LIST)

	def push_headers(self):
		print "{:<10}\t{:<22}\t{:<10}".format(pull.DARKCYAN+"[HTTP/HTTPS]", "SUBDOMAIN", "CNAME"+pull.END)

	def cname(self, _sub):
		_cn = ' '
		try:
			_cn = dns.resolver.query(_sub, "CNAME")[0]
		except dns.resolver.NoAnswer, _err:
			pass
		return _cn

	def push(self):
		for _sub, _ls in self.__LIST.items():
			_cn = self.cname(_sub)
			print "{:<10}\t{:<22}\t{:<10}".format(_ls[1], _sub, _cn)
			self.__CNAMES[_sub] = _cn

	def save(self, _fl):
		_file = open(_fl, 'w')
		_file.write( ",".join(["RESOLUTION", "[HTTP/HTTPS]", "SERVER", "SUBDOMAIN", "CNAME\n"]) )
		for _sub, _ls in self.__LIST.items():
			_towrite = ",".join([ _ls[0], _ls[1], _ls[2], _sub, str(self.__CNAMES[_sub])+"\n" ])
			_file.write(_towrite)
		_file.close()

class LISTER:

	__SUBS = {}
	__COUNT = 0
	__DATA = {}
	#STRUCTURE
	#'sub': [ (http, https), ('ERR', 'ERR'), ('NONE', 'NONE') ]

	def __init__(self, _dm, _wd, _th):
		self.domain = _dm
		self.wordlist = _wd
		self.threads = _th
		self.agent = USERAGENT()
		self.bind_thread_lock()
		signal.signal(signal.SIGINT, self.sig_handler)
		self.tab = TABULATOR( [pull.DARKCYAN+'RESOLUTION', '[HTTP/HTTPS]', 'SERVER', 'SUBDOMAIN'+pull.END], pull)

	def bind_thread_lock(self):
		self.lock = threading.Semaphore(value=1)

	def sig_handler(self, sig, frame):
		sys.exit(0)

	def pause(self):
		while self.__COUNT > 0:
			time.sleep(1)

	def passer(self):
		_file = open(self.wordlist)
		_lns = _file.read().splitlines()
		for _ln in _lns:
			if _ln.endswith(self.domain):
				self.__SUBS[ _ln.rstrip(".%s\n" % self.domain) ] = ['ERR', 'NONE']
				self.__DATA[ _ln.rstrip(".%s\n" % self.domain) ] = [ ['ERR', 'NONE'], [ 'ERR', 'ERR' ], [ 'NONE', 'NONE' ] ]
			else:
				self.__SUBS[ _ln.rstrip("\n") ] = ['ERR', 'NONE']
				self.__DATA[ _ln.rstrip("\n") ] = [ ['ERR', 'NONE'], [ 'ERR', 'ERR' ], [ 'NONE', 'NONE' ] ]

	def ip(self, _sb):
		_ip = ''
		try:	
			_ip = socket.gethostbyname(_sb)
			return _ip
		except:
			return _ip

	def brute(self):
		for _sub, _fds in self.__SUBS.items():
			_subdomain = "%s.%s" % (_sub, self.domain)
			_t = threading.Thread(target=self.handler, args=(_sub, self.domain,),)
			_t.daemon = True
			_t.start()

			if self.__COUNT >= self.threads:
				while self.__COUNT >= self.threads:
					pass

	def server(self, _server):
		_ret = 'NONE'
		if _server[0] != 'NONE' and _server[1] == 'NONE':
			_ret = _server[0]
		elif _server[0] == 'NONE' and _server[1] != 'NONE':
			_ret = _server[1]
		elif _server[0] != 'NONE' and _server[1] != 'NONE' and _server[0] == _server[1]:
			_ret = _server[0]
		return _ret

	def putin(self, _subdomain, _codes, _server):
		_tosend = [ self.ip(_subdomain), "[%s/%s]" % (_codes[0], _codes[1]), \
					"%s" % self.server(_server), _subdomain]

		if _codes[0] != 'ERR' or _codes[1] != 'ERR':
			cnames.add(_tosend)

		self.lock.acquire()
		self.tab.addin(_tosend)
		self.tab.push(_tosend)
		self.lock.release()

	def handler(self, _sb, _dm):
		self.__COUNT += 1

		self.__DATA[_sb][0][0] = self.request("%s.%s" % (_sb, _dm), 80, _sb)   #HTTP
		self.__DATA[_sb][0][1] = self.request("%s.%s" % (_sb, _dm), 443, _sb)  #HTTPS

		self.__DATA[_sb][1][0] = self.__DATA[_sb][0][0][0]
		self.__DATA[_sb][1][1] = self.__DATA[_sb][0][1][0]

		self.__DATA[_sb][2][0] = self.__DATA[_sb][0][0][1]
		self.__DATA[_sb][2][1] = self.__DATA[_sb][0][1][1]

		self.putin("%s.%s" % (_sb, _dm), self.__DATA[_sb][1], self.__DATA[_sb][2])

		self.__COUNT -= 1

	def request(self, _sb, _port, _part):
		_req = b"GET / HTTP/1.1\r\nHost: %s.com\r\nUser-Agent: %s\r\n%s\r\n\r\n" % (_sb, self.agent.random(), self.agent.extras)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
		s.settimeout(5)
		try:
			s.connect((_sb, _port))
			s.send(_req)
			_res = s.recv(10000)
			for n in range(0, 4):
 				if "\r\n\r\n" in _res:
 					self.close(s)
 					_sold = PULLER( _sb, _res.split("\r\n\r\n")[0] )
 					self.__SUBS[_part][0], self.__SUBS[_part][1] = _sold.CODE, _sold.SERVER
 					break
 				else:
					_res = s.recv(10000)
		except socket.error:
			self.close(s)
		return ( self.__SUBS[_part][0], self.__SUBS[_part][1] )

	def close(self, _sock):  
		_sock.close()

class ROMER:

	POSTED = set()
	DATA = {}
	COUNT = 0

	def __init__(self, _dm, _th):
		self.domain = _dm
		self.threads = _th
		self.agent = USERAGENT()
		self.lock = threading.Semaphore(value=1)

	def lister(self, _subs):
		for sub in _subs:
			if sub not in self.POSTED:
				self.DATA[sub] = [ ['ERR', 'ERR'], ['NONE', 'NONE'] ]

	def googler(self):
		_g = GOOGLE( self.domain , self.agent.random() )
		_g.send()
		_data = _g.read()
		_html = soup(_data[1])
		for cite in _html.findAll('cite'):
			_g.collect(cite.text)
		_subdoers = _g.subdomains()
		self.lister(_subdoers)
		for _sub in _subdoers:
			if _sub not in self.POSTED:
				_t = threading.Thread(target=self.poster, args=(_sub, _g, "GOOGLE"), )
				_t.daemon = True
				_t.start()
				self.POSTED.add( _sub )

			if self.COUNT >= self.threads:
				while self.COUNT >= self.threads:
					time.sleep(1)

	def binger(self):
		_b = BINGER( self.domain, self.agent.random() )
		_b.send()
		_data = _b.read()
		_html = soup(_data[1])
		for cite in _html.findAll('cite'):
			_b.collect(cite.text)
		_subdoers = _b.subdomains()
		self.lister(_subdoers)
		for _sub in _subdoers:
			if _sub not in self.POSTED:
				_t = threading.Thread(target=self.poster, args=(_sub, _b, "BING"), )
				_t.daemon = True
				_t.start()
				self.POSTED.add( _sub )

			if self.COUNT >= self.threads:
				while self.COUNT >= self.threads:
					time.sleep(1)

	def poster(self, _sub, _g, _passer):
		self.COUNT += 1

		self.DATA[_sub][0][0], self.DATA[_sub][1][0] = _g.request(_sub, 80, self.agent.random())
		self.DATA[_sub][0][1], self.DATA[_sub][1][1] = _g.request(_sub, 443, self.agent.random())

		self.push( [self.ip(_sub), "[%s/%s]" % (self.DATA[_sub][0][0], self.DATA[_sub][0][1]), \
					"[%s/%s]" % (self.DATA[_sub][1][0], self.DATA[_sub][1][1]), \
					_passer, _sub] )

		self.COUNT -= 1

	def ip(self, _sb):
		_ip = ''
		try:	
			_ip = socket.gethostbyname(_sb)
			return _ip
		except:
			return _ip

	def push(self, _lis):
		self.lock.acquire()
		_pr = "{:<15}\t{:<10}\t{:<17}\t{:<15}\t{:<15}".format(_lis[0], _lis[1], _lis[2], _lis[3], _lis[4])
		print _pr
		self.lock.release()

	def brute(self):
		self.googler()
		"Starting Bing"
		self.binger()

	def pause(self):
		while self.COUNT > 0:
			time.sleep(1)


def _domainer(_dm):
	if _dm != None:
		if re.match("^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$", _dm.lower(), re.I):
			return _dm.lower()
		else:
			pull.error("Invalid Domain Name. Not Valid \"%s\"" % (pull.RED+_dm.lower()+pull.END))
			sys.exit(-1)
	else:
		pull.error("Domain Name not specified. Specify -d, --domain option")
		sys.exit(-1)

def nameservers(_dm):
	ns = []
	try:
		ns = dns.resolver.query(_dm, "NS")
	except:
		pull.error("Error Locating NameServeres. Skipping ... %s[Failed]%s" % (pull.RED, pull.END))
	return ns

def _wordlister(_wd):
	if _wd == '':
		pull.error("Dictionary Not Specified. Specify -w, --wordlist option. Available Dictionaries are: ")
		pull.slash("Large -> large %s[257]%s Entries" % (pull.DARKCYAN, pull.END))
		pull.slash("Small -> small %s[8215]%s Entries" % (pull.DARKCYAN, pull.END))
		sys.exit(-1)

	elif _wd == 'small':
		return os.path.join( os.getcwd(), 'wordlists/small.lst' )

	elif _wd == 'large':
		return os.path.join( os.getcwd(), 'wordlists/large.lst' )

	elif not os.path.isfile(_wd):
		pull.error("No Such File: %s[%s]%s" % (pull.RED, _wd, pull.END))
		sys.exit(-1)

	else:
		return _wd

def count_dict(_wd):
	_file = open(_wd, 'r')
	return len(_file.readlines())

def main():
	parser = optparse.OptionParser(add_help_option=False)

	parser.add_option('-h', '--help', dest='help', action='store_true', default=False)
	parser.add_option('-d', '--domain', dest="domain", type="string", help="Domain Name")
	parser.add_option('-w', '--wordlist', dest="wordlist", default='', type="string", help="Wordlist")
	parser.add_option('-t', '--threads', dest="threads", type="int", default=25, help="Threads")
	parser.add_option('-o', '--output', dest="save", type="string", help="Save")

	(options, args) = parser.parse_args()

	if options.help:
		pull.help()
		sys.exit(0)

	_dm = _domainer(options.domain)
	_wd = _wordlister(options.wordlist)
	pull.right("Identifying NameServers ...\n")
	_nm = nameservers(_dm)
	for nm in _nm:
		pull.slash(nm)

	#_siter = ROMER(_dm, options.threads)
	#_siter.brute()
	#_siter.pause()

	pull.linebreak()
	pull.right("Enumerating Subdomains from Dictionary %s[%d]%s" % (pull.DARKCYAN, count_dict(_wd), pull.END))
	pull.linebreak()

	_orator = LISTER(_dm, _wd, options.threads)
	_orator.passer()
	_orator.brute()
	_orator.pause()

	pull.linebreak()
	pull.right("Enumerating CNAME Records ... %s[%s]%s" % (pull.DARKCYAN, cnames.count(), pull.END))
	pull.linebreak()

	cnames.push_headers()
	cnames.push()

	if options.save != None:
		pull.linebreak()
		pull.right("Saving Output to File ... %s[%s]%s" % (pull.DARKCYAN, options.save, pull.END))
		pull.linebreak()

		cnames.save(options.save)

if __name__ == "__main__":
	pull = PULLY()
	cnames = CNAMES()
	pull.logo()
	main()
