#!/usr/bin/python

import optparse
import re
import os
import sys
import socket
import time
import ssl
import random
import threading
import signal
import string
from dns import resolver
from pull import PULLY
from handlers import GOOGLE
from handlers import BING
from handlers import YAHOO
from handlers import ASK
from handlers import BAIDU
from handlers import NETCRAFT
from handlers import DNSDUMPSTER
from handlers import VIRUSTOTAL
from handlers import THREATCROWD
from handlers import CRTSEARCH
from BeautifulSoup import BeautifulSoup as soup

pull = PULLY()

class NameServer:

	RECORDS = []

	def __init__(self, _dm):
		self.domain = _dm
		self.servers = self.query(_dm, "NS")
		self.mailserver = self.query(_dm, "MX")
		self.texts = self.query(_dm, "TXT")

	def query(self, _dm, _type):
		_ret = []
		try:
			_ret = resolver.query(_dm, _type)
		except:
			pass
		return _ret

	def push(self):
		for ns in self.servers:
			self.RECORDS.append( "NS  - " + str(ns) )
			pull.slash( "NS  - " + str(ns) )
		for mx in self.mailserver:
			self.RECORDS.append( "MX  - " + str(mx) )
			pull.slash( "MX  - " + str(mx) )
		for txt in self.texts:
			self.RECORDS.append( "TXT - " + str(txt) )
			pull.slash( "TXT - " + str(txt) )

	def def_ip(self):
		def randomString(stringLength=12):
			letters = string.ascii_lowercase
			return ''.join(random.choice(letters) for i in range(stringLength))

		try:
			_ip = socket.gethostbyname( "%s.%s" % (randomString(), self.domain) )
			pull.slash( "Wildcard Detected - %s" % _ip )
		except:
			_ip = ""
			pull.slash( "No Wildcard Detected." )
		return _ip

	def def_cn(self):
		def randomString(stringLength=12):
			letters = string.ascii_lowercase
			return ''.join(random.choice(letters) for i in range(stringLength))

		_cn = self.query( "%s.%s" % (randomString(), self.domain), "CNAME" )
		if _cn:
			pull.slash( "Subdomain Redirection Found! Omitting Results with CNAMES to %s" % str(_cn[0]) )
			return str(_cn[0])
		else:
			pull.slash( "Subdomain Redirection not Found!" )
			return ""

class Online:

	SUBDOMAINS = []
	THREADS    = 0

	def __init__(self, _dm):
		self.domain = _dm
		self.google = GOOGLE( self, _dm )
		self.bing = BING( self, _dm )
		self.yahoo = YAHOO( self, _dm )
		self.ask = ASK( self, _dm )
		self.baidu = BAIDU( self, _dm )
		self.netcraft = NETCRAFT( self, _dm )
		self.dnsdumpster = DNSDUMPSTER( self, _dm )
		self.virustotal = VIRUSTOTAL( self, _dm )
		self.crt = CRTSEARCH( self, _dm )

	def enumerate(self):
		self.google.execute()
		self.bing.execute()
		self.yahoo.execute()
		self.ask.execute()
		self.baidu.execute()
		self.netcraft.execute()
		#self.dnsdumpster.execute()
		self.virustotal.execute()
		self.crt.execute()

	def acquire(self):
		return self.SUBDOMAINS

	def move(self, _name, _ls):
		def push():
			string = "{:<14}\t{:<28}".format(_name, len(_ls))
			pull.indent( string, spaces=4 )
			return 0

		for ls in _ls:
			if ls not in self.SUBDOMAINS:
				self.SUBDOMAINS.append( ls )

		return push()

	def pause(self):
		while self.THREADS > 0:
			pass
		return

class Brute:

	THREADS = 0
	AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
	FRESOL = "{:<18.15}"
	FCODE  = "{:<18.17}"
	FSERVER= "{:<21.20}"
	FSUBDOM= "{:<%i.%i}"
	LOCK = threading.Semaphore( value = 1 )
	LIBRARY = {
	}

	def __init__( self, _dm, _wd, _ip, _sb, _th ):
		self.domain = _dm
		self.max = _th
		self.ip = _ip
		self.subdomains = self.parse( _wd, _sb )
		self.format = self.formate()

	def parse(self, _wd, _sb):
		_list = list(_wd) + list(_sb)
		for _ls in _list:
			_list[ _list.index(_ls) ] = (_ls + ".%s" % self.domain) if not _ls.endswith( ".%s"%self.domain ) else _ls  
		return list( set( _list ) )

	def formate(self):
		def count():
			_count = 16
			for _ls in self.subdomains:
				if len( _ls[: -len("."+self.domain) ] ) > _count:
					_count = len( _ls[: -len("."+self.domain) ] )
			return _count

		self.FSUBDOM = self.FSUBDOM % ( count(), count() + 1 )
		print pull.DARKCYAN + self.FRESOL.format( "RESOLUTION" ) + self.FCODE.format( "[HTTP/HTTPS]" ) \
				+ self.FSUBDOM.format( "SUBDOMAIN" ) + self.FSERVER.format( "SERVER" ) + pull.END

	def simplify(self, _resp):
		_polls = {
			'code': 'ERR',
			'server': 'NONE',
		}
		_headers = _resp.split("\r\n\r\n")[0]
		for _ln in _headers.splitlines():
			if _ln.startswith( "HTTP/" ):
				_polls[ 'code' ] = _ln.split( " " )[1].strip( "\r" )
			elif _ln.startswith( "Server:" ):
				_polls[ 'server' ] = _ln.split( ": " )[1]
		return _polls

	def push(self, _subdomain):
		def ip():
			_ip = ''
			try:	
				_ip = socket.gethostbyname(_subdomain)
				self.LIBRARY[_subdomain]['ip'] = _ip
				if _ip != self.ip:
					_ip = pull.GREEN + self.FRESOL.format( _ip ) + pull.END
					return _ip
			except Exception, e:
				pass
			return self.FRESOL.format(_ip)

		def code( _code ):
			if _code != "ERR":
				_code = int( _code )
				if _code >= 200 and _code < 300:
					return pull.GREEN + "{:<3.3}".format( str( _code ) ) + pull.END
				elif _code >= 300 and _code < 400:
					return pull.YELLOW + "{:<3.3}".format( str( _code ) ) + pull.END
				elif _code >= 400 and _code < 600:
					return pull.RED + "{:<3.3}".format( str( _code ) ) + pull.END
			else:
				return "{:<3.3}".format( str( _code ) )

		def server( _s1, _s2 ):
			if _s1 != "NONE" and _s2 != "NONE":
				return pull.CYAN + self.FSERVER.format( _s2 ) + pull.END
			elif _s1 == "NONE" and _s2 != "NONE":
				return pull.CYAN + self.FSERVER.format( _s2 ) + pull.END
			elif _s1 != "NONE" and _s2 == "NONE":
				return pull.CYAN + self.FSERVER.format( _s1 ) + pull.END
			else:
				return self.FSERVER.format( _s1 )

		if self.LIBRARY.has_key( _subdomain ):
			if self.LIBRARY[_subdomain].has_key( 80 ) and self.LIBRARY[_subdomain].has_key( 443 ):
				self.LOCK.acquire( )
				print ip() + "{:<1.1}".format("[") + code( self.LIBRARY[_subdomain][80]['code'] ) + "{:<1.1}".format("/") + code( self.LIBRARY[_subdomain][443]['code'] ) + "{:<10.10}".format("]") \
						+ self.FSUBDOM.format( _subdomain[: -len("."+self.domain) ] ) + server( self.LIBRARY[_subdomain][80]['server'], self.LIBRARY[_subdomain][443]['server'] )
				self.LOCK.release()
			else:
				pull.error( "Some internal parts are being missed. Rerun the script!" ); sys.exit( -1 )

	def handler(self, _subdomain, _baseclass):
		_baseclass.THREADS += 1

		self.LIBRARY[ _subdomain ] = { 80: { 'code': 'ERR', 'server': 'NONE' }, 443: { 'code': 'ERR', 'server': 'NONE' }, 'ip': '' }
		self.request( _subdomain )
		self.push( _subdomain )

		_baseclass.THREADS -= 1

	def request(self, _subdomain):
		_req = "GET / HTTP/1.1\r\nHost: %s\r\nUser-Agent: %s\r\nOrigin: http://%s\r\n\r\n" % (_subdomain, self.AGENT, _subdomain)
		
		def connect(_pt):
			_s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			_s.settimeout( 10 )
			try:
				if _pt == 443:
					_s =  ssl.wrap_socket(_s, ssl_version=ssl.PROTOCOL_TLS)
				_s.connect((_subdomain, _pt))
				_s.send( _req )
				_rec = _s.recv( 1000 )
				while "\r\n\r\n" not in _rec:
					_rec += _s.recv( 1000 )
				self.LIBRARY[ _subdomain ][ _pt ] = self.simplify( _rec )
				_s.close()
			except:
				pass

		connect(80)
		connect(443)

	def brute(self):
		for _ls in self.subdomains:
			_t = threading.Thread( target=self.handler, args=(_ls, self) )
			_t.daemon = True
			_t.start()

			while self.THREADS >= self.max:
				pass

	def pause(self):
		while self.THREADS > 0:
			time.sleep(8)

class Scanner:

	COUNTER = 0
	FCODE  = "{:<18.17}"
	FSUBDOM= "{:<%i.%i}"
	FPORTS = "{:<%i.%i}"
	FCNAME = "{:<}"
	PORTS_COLLECTOR = {}
	PORTS_COUNTER   = {}
	LOCK = threading.Semaphore( value=1 )

	def __init__(self, _dm, _ports, _th, _lib, _ip, _cn):
		self.domain = _dm
		self.ports = _ports
		self.threads = 10
		self.d_ip = _ip
		self.d_cn = _cn
		self.library = self.parse( _lib )
		self.formatter()

	def parse(self, _lib):
		_list = {}
		for (_sub, _values) in _lib.items():
			if _lib[_sub][80]['code'] != 'ERR' or _lib[_sub][443]['code'] != 'ERR' or _lib[_sub]['ip'] != self.d_ip:
				_list[_sub] = _values
		return _list

	def formatter(self):
		def subcount():
			_count = 13
			for (_lib, _val) in self.library.items():
				if len( _lib[: -len("."+self.domain) ] ) > _count:
					_count = len( _lib[: -len("."+self.domain) ] )
			return _count

		def portcount():
			_count = 14
			if len( self.ports ) > _count and len( self.ports ) < 24:
				_count = len( self.ports )
			elif len( self.ports ) > 24:
				_count = 23
			return _count

		self.FSUBDOM = self.FSUBDOM % ( subcount() + 1, subcount() )
		self.FPORTS  = self.FPORTS % ( portcount() + 1, portcount() )
		print pull.DARKCYAN + self.FCODE.format( "[HTTP/HTTPS]" ) + self.FSUBDOM.format( "SUBDOMAIN" ) + self.FPORTS.format( "PORTS" ) \
				+ self.FCNAME.format( "CNAME" ) + pull.END

	def porter_extension(self, _subdomain, _pt):
		self.PORTS_COUNTER[ _subdomain ] += 1

		try:
			_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			_s.settimeout( 4 )
			_s.connect((_subdomain, _pt))
			self.PORTS_COLLECTOR[ _subdomain ].append( str(_pt) )
		except:
			pass

		self.PORTS_COUNTER[ _subdomain ] -= 1

	def porter(self, _subdomain,):

		self.PORTS_COLLECTOR[ _subdomain ] = []
		self.PORTS_COUNTER  [ _subdomain ] = 0

		def wait():
			while self.PORTS_COUNTER[ _subdomain ] > 0:
				time.sleep(2)

		for _pt in self.ports:
			_t = threading.Thread( target=self.porter_extension, args=(_subdomain,_pt,) )
			_t.daemon = True
			_t.start()

			while self.PORTS_COUNTER[ _subdomain ] > 10:
				time.sleep( 2 )

		wait()
		self.library[ _subdomain ][ 'misc' ][ 'ports' ] = ",".join( self.PORTS_COLLECTOR[ _subdomain ] )

	def cnamer(self, _subdomain):
		_cn = ''
		try:
			_cn = resolver.query( _subdomain, "CNAME" )[0]
		except:
			pass
		self.library[_subdomain]['misc']['cname'] = str(_cn)
		return str(_cn)

	def push(self, _subdomain, _c1, _c2):
		def code(_code):
			if _code != "ERR":
				_code = int( _code )
				if _code >= 200 and _code < 300:
					return pull.GREEN + "{:<3.3}".format( str( _code ) ) + pull.END
				elif _code >= 300 and _code < 400:
					return pull.YELLOW + "{:<3.3}".format( str( _code ) ) + pull.END
				elif _code >= 400 and _code < 600:
					return pull.RED + "{:<3.3}".format( str( _code ) ) + pull.END
			else:
				return "{:<3.3}".format( str( _code ) )

		def port( _pts ):
			if _pts:
				return pull.BLUE + self.FPORTS.format( _pts ) + pull.END
			else:
				return self.FPORTS.format( _pts )

		def cname( _cname ):
			if _cname:
				return pull.RED + self.FCNAME.format( str(_cname) ) + pull.END
			else:
				return self.FCNAME.format( _cname )

		self.LOCK.acquire()
		print "{:<1.1}".format('[') + code(_c1) + "{:<1.1}".format('/') + code(_c2) + "{:<10.10}".format(']') + self.FSUBDOM.format( _subdomain[: -len("."+self.domain) ] ) \
				+ port( self.library[_subdomain]['misc']['ports'] ) + cname( self.library[_subdomain]['misc']['cname'] )
		self.LOCK.release()

	def handler(self, _subdomain, _c1, _c2):
		self.COUNTER += 1

		self.library[_subdomain]["misc"] = { 'ports': '', 'cname': '' }
		self.porter( _subdomain )
		_cn = self.cnamer( _subdomain )
		if _cn == self.d_cn:
			del self.library[ _subdomain ]
		else:
			self.push( _subdomain, _c1, _c2 )

		self.COUNTER -= 1

	def scan(self):
		for (_lib, _val) in self.library.items():
			_t = threading.Thread( target=self.handler, args=(_lib, _val[80]['code'], _val[443]['code']) )
			_t.daemon = True
			_t.start()

			while self.COUNTER >= self.threads:
				time.sleep(3)

	def pause(self):
		while self.COUNTER > 0:
			time.sleep(5)

class Output:

	FRESOL = "{:<18.15}"
	FCODE  = "{:<18.17}"
	FSERVER= "{:<%i.%i}"
	FPORTS = "{:<%i.%i}"
	FSUBDOM= "{:<%i.%i}"
	FCNAME = "{:<}"

	def __init__(self, _dm, _output, _fms, _library):
		self.domain = _dm
		self.file   = _output
		self.formats= _fms
		self.library = _library
		self.formatter()

	def opener(self, _out):
		 _fl = open( _out, 'w' )
		 return _fl

	def formatter(self):
		def porter():
			_count = 8
			for ( _lib, _values ) in self.library.items():
				if len(_values[ 'misc' ][ 'ports' ]) > _count:
					_count = len(_values[ 'misc' ][ 'ports' ])
			return _count

		def server():
			_count = 10
			for ( _lib, _values ) in self.library.items():
				if len( _values[ 80 ][ 'server' ]) > _count:
					_count = len( _values[ 80 ][ 'server' ])
				if len( _values[ 443 ][ 'server' ]) > _count:
					_count = len( _values[ 443 ][ 'server' ])
			return _count

		def subdomain():
			_count = 14
			for ( _lib, _values ) in self.library.items():
				if len( _lib[: -len("."+self.domain) ] ) > _count:
					_count = len( _lib[: -len("."+self.domain) ] )
			return _count

		self.FSERVER = self.FSERVER % ( server() + 1, server() )
		self.FPORTS  = self.FPORTS  % ( porter() + 1, porter() )
		self.FSUBDOM = self.FSUBDOM % ( subdomain() + 1, subdomain() )

	def o_simple(self):
		def server(_s1, _s2):
			if _s1 != "NONE" and _s2 != "NONE":
				return self.FSERVER.format( _s2 )
			elif _s1 == "NONE" and _s2 != "NONE":
				return self.FSERVER.format( _s2 )
			elif _s1 != "NONE" and _s2 == "NONE":
				return self.FSERVER.format( _s1 )
			else:
				return self.FSERVER.format( _s1 )

		_file = self.opener( self.file + "-simple.txt" )
		_line = self.FRESOL.format( "RESOLUTION" ) + self.FCODE.format( "[HTTP/HTTPS]" ) + self.FSERVER.format( "SERVER" ) + self.FPORTS.format( "PORTS" ) + self.FSUBDOM.format( "SUBDOMAIN" ) + \
				self.FCNAME.format( "CNAME" )
		_file.write( _line )
		_file.write( "\n\n" )
		for (_lib, _values) in self.library.items():
			_line = self.FRESOL.format( _values[ 'ip' ] ) + "{:<1.1}".format( "[" ) + "{:<3.3}".format( _values[ 80 ][ 'code' ] ) + "{:<1.1}".format( "/" ) + "{:<3.3}".format( _values[ 443 ][ 'code' ] ) + \
					"{:<10.10}".format( "]" ) + self.FSERVER.format( server( _values[ 80 ][ 'server' ], _values[ 443 ][ 'server' ] ) ) + self.FPORTS.format( _values[ 'misc' ][ 'ports' ] ) + \
					self.FSUBDOM.format( _lib[: -len("."+self.domain) ] ) + self.FCNAME.format( _values[ 'misc' ][ 'cname' ] )
			_file.write( _line )
			_file.write("\n")
		self.push( self.file + "-subdomains.txt", "SIMPLE" )

	def o_csv(self):
		_file = self.opener( self.file + "-csv.csv" )
		for ( _lib, _values ) in self.library.items():
			_line = _values['ip'] + "," + "[" + _values[ 80 ][ 'code' ] + "/" + _values[ 443 ][ 'code' ] + "]" + "," + "[" + _values[ 80 ][ 'server' ] + "/" + _values[ 443 ][ 'server' ] + "]" \
					+ "," + _values[ 'misc' ][ 'ports' ].replace( ",", "." ) + "," + str(_values[ 'misc' ][ 'cname' ]) + "," + _lib
			_file.write( _line )
			_file.write( "\n" )
		self.push( self.file + ".csv", "CSV" )

	def o_codes(self):
		_file = self.opener( self.file + "-codes.txt" )
		for ( _lib, _values ) in self.library.items():
			_line = _lib + "," + "[" + _values[ 80 ][ 'code' ] + "/" + _values[ 443 ][ 'code' ] + "]"
			_file.write( _line )
			_file.write( "\n" )
		self.push( self.file + "-codes.txt", "STATUS" )

	def o_subdomains(self):
		_file = self.opener( self.file + "-subdomains.txt" )
		for ( _lib, _values ) in self.library.items():
			_file.write( _lib )
			_file.write( "\n" )
		self.push( self.file + "-subdomains.txt", "SUBDOMAINS" )

	def output(self):
		for _fm in self.formats:
			if _fm == "simple":
				self.o_simple()
			elif _fm == "csv":
				self.o_csv()
			elif _fm == "status":
				self.o_codes()
			elif _fm == "subdomains":
				self.o_subdomains()

	def push(self, _name, _type):
		pull.indent( "%s%s%s - Written Output to %s" % (pull.GREEN, _type, pull.END, _name), spaces=4 )

class Parser:

	def __init__(self, _opts, _args):
		self.signal = signal.signal( signal.SIGINT, self.sig_handler )
		self.options = _opts
		self.arguments = _args
		self.help = _opts.help
		self.domain = self.parse_domain(_opts.domain)
		self.b_wordlist = self.parse_b_wordlist(_opts.bruteforce)
		self.wordlist = self.parse_wordlist(_opts.wordlist)
		self.threads = self.parse_threads(_opts.threads)
		self.output = self.parse_output(_opts.output)
		self.format = self.parse_format(_opts.format)
		self.b_ports = _opts.portscan
		self.ports = self.parse_ports(_opts.ports)
		self.online = self.parse_online(_opts.online)

	def parse_domain(self, _dm):
		if _dm != None:
			if re.match("^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$", _dm.lower(), re.I):
				return _dm.lower()
			else:
				pull.error("Invalid Domain Name. Not Valid \"%s\"" % (pull.RED + _dm.lower() + pull.END)); sys.exit(-1)
		else:
			pull.error("Domain Name not specified. Specify -d, --domain option"); sys.exit(-1)

	def parse_b_wordlist(self, _b):
		return _b

	def parse_wordlist(self, _wd):
		_list = []
		if not self.b_wordlist:
			if not _wd:
				pull.error("Dictionary Not Specified. Specify -w, --wordlist option"); sys.exit(-1)
			else:
				for _ls in set(_wd.split(",")):
					if not os.path.isfile(_ls):
						pull.error("No Such File: %s[%s]%s" % (pull.RED, _ls, pull.END)); sys.exit(-1)
					else:
						_file = open(_ls, 'r')
						for _ln in _file.read().splitlines():
							_list.append(_ln)
		return list(set(_list))

	def parse_threads(self, _th):
		if type(_th) == int:
			return _th
		else:
			pull.error("Not a Valid Value. Specify a valid integer for -t, --threads."); sys.exit(-1)

	def parse_output(self, _out):
		if _out:
			return _out
		else:
			return False

	def parse_format(self, _fmss):
		_fms = ['simple', 'csv', 'status', 'subdomains']
		_lis = []
		for _fm in _fmss.split(","):
			if _fm not in _fms:
				pull.error( "Format not supported: %s" % _fm ); sys.exit( -1 )
			else:
				_lis.append( _fm )
		return _lis

	def parse_ports(self, _pts):
		_list = []
		if not self.b_ports:
			if _pts:
				for pt in _pts.split(","):
					try:
						if len(pt.split("-")) > 1:
							(_s, _e) = pt.split( "-" )
							for n in range( int(_s), int(_e) ):
								_list.append( n )
						elif int(pt) > 0 and int(pt) < 65536:
							_list.append( int(pt) )
						else:
							pull.error("Not a Valid Port! %s" % pt); sys.exit(-1)
					except ValueError:
						pull.error("Not a Valid Port! %s" % pt); sys.exit(-1)
		return list(set(_list))

	def parse_online(self, _bool):
		if _bool:
			return True
		return False

	def sig_handler(self, _sig, _fr):
		sys.exit(0)

def main():
	parser = optparse.OptionParser( add_help_option=False )

	parser.add_option('-h', '--help', dest='help', action='store_true', default=False)
	parser.add_option('-d', '--domain', dest="domain", type="string", help="Domain Name")
	parser.add_option('-w', '--wordlist', dest="wordlist", default='', type="string", help="Wordlist")
	parser.add_option('-t', '--threads', dest="threads", type="int", default=25, help="Threads")
	parser.add_option('-o', '--output', dest="output", type="string", default=False, help="Save")
	parser.add_option('-s', '--output-subs', dest="outputsubs", type="string", default=False, help="Output Subdomains")
	parser.add_option('-f', '--format', dest="format", default="simple", type="string", help="Format")
	parser.add_option('-p', '--ports', dest="ports", type="string", default=dports, help="ports")
	parser.add_option(''  , '--skip-online', dest="online", action="store_true", default=False, help="Online")
	parser.add_option(''  , '--skip-wordlist', dest="bruteforce", action="store_true", default=False, help="Wordlist")
	parser.add_option(''  , '--skip-ports', dest="portscan", action="store_true", default=False, help="Port Scan")

	(options, args) = parser.parse_args()

	pull.logo()

	if options.help:
		pull.help(); sys.exit(0)
	else:
		parser, subs = Parser(options, args), []
		pull.right("Enumerating DNS Records ..."); pull.linebreak()
		nservers = NameServer( parser.domain )
		nservers.push()

		pull.linebreak(); pull.right("Identifying Redirection for Preventing False Positives"); pull.linebreak()
		ip = nservers.def_ip()
		cn = nservers.def_cn()

		if not parser.online:
			pull.linebreak(); pull.right("Enumerating Subdomains Online ..."); pull.linebreak()
			online = Online( parser.domain )
			online.enumerate()
			online.pause()
			subs = online.acquire()

		pull.linebreak(); pull.right("Enumerating Subdomains ..."); pull.linebreak()
		bruteforcer = Brute( parser.domain, parser.wordlist, ip, subs, parser.threads )
		bruteforcer.brute()
		bruteforcer.pause()

		time.sleep(1)

		pull.linebreak(); pull.right("Identifying Services ..."); pull.linebreak()
		scanner = Scanner( parser.domain, parser.ports, parser.threads, bruteforcer.LIBRARY, ip, cn )
		scanner.scan()
		scanner.pause()

		if parser.output:
			pull.linebreak(); pull.right("Output..."); pull.linebreak()
			output = Output( parser.domain, parser.output, parser.format, scanner.library )
			output.output()
			pull.linebreak()


if __name__ == "__main__":
	dports = """21-23,25-26,53,81,110-111,113,135,139,143,179,199,445,465,514-515,548,554,587,646,993,995,1025-1027,
			1433,1720,1723,2000-2001,3306,3389,5060,5666,5900,6001,8000,8008,8080,8443,8888,10000,32768,49152,49154"""
	main()