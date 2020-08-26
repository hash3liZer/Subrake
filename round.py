import random
import string
import socket
import threading
import dns.resolver as resolver

class ROUNDER:

	PTHREADS = 0
	PORTS = """21-23,25-26,53,81,110-111,113,135,139,143,179,199,445,465,514-515,548,554,587,646,993,995,1025-1027,
			1433,1720,1723,2000-2001,3306,3389,5060,5666,5900,6001,8000,8008,8080,8443,8888,10000,32768,49152,49154"""

	AGENT    = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
	FRESOL   = "{:<18.15}"
	FCODE    = "{:<18.17}"
	FSERVER  = "{:<21.20}"
	FSUBDOM  = "{:<%i.%i}"
	FPORTS   = "{:<21.20}"
	FSIMIL   = "{:<10.9}"
	FCNAME   = "{:<}"

	def rstring( self, strlen = 10 ):
		letters = string.ascii_lowercase
		return ''.join( random.choice(letters) for i in range( strlen ) )

	def maxcountp( self, tocut, tosolve, toadd='', _count = 16 ):
		for _ls in tosolve:
			if len( _ls[: -len( toadd + tocut ) ] ) > _count:
				_count = len( _ls[: -len(  toadd + tocut ) ] )
		return _count + 1

	def fmreplsb( self, toput ):
		self.FSUBDOM = self.FSUBDOM % ( toput, toput + 1 )
		return

	def seperator(self, code, headers):
		_polls = {
			'cd': 'ERR',
			'sv': '',
		}

		if code:
			_polls['cd'] = code

		if headers:
			headers = dict(headers)
			if "Server" in list(headers.keys()):
				_polls['sv'] = headers.get("Server")

		return _polls

	def iplocator(self, hostname, defip):
		_ip = ''
		try:
			toput = socket.gethostbyname( hostname )
			_ip = toput
		except Exception as e:
			pass
		return _ip

	def cnlocator(self, hostname, defcn):
		_cn = ''
		try:
			aa = resolver.query( hostname, "CNAME" )
			if aa:
				return str( aa[ 0 ] )
			return _cn
		except:
			return _cn

	def ptlocator(self, hostname, pts, retlist=[]):
		def connector(pt, sclass):
			sclass.PTHREADS += 1
			try:
				s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
				s.settimeout( 5 )
				s.connect( (hostname, pt) )
				retlist.append( str(pt) )
			except:
				pass
			sclass.PTHREADS -= 1

		for pt in pts:
			_t = threading.Thread( target=connector, args=(pt, self) )
			_t.daemon = True
			_t.start()

			while self.PTHREADS >= 6:
				pass

		while self.PTHREADS > 0:
			pass

		return list(set(retlist))

	def formatrsv(self, ip, defip, cplate):
		if ip == defip:
			return cplate[ 'YELLOW' ] + self.FRESOL.format( ip ) + cplate[ 'END' ]
		else:
			return cplate[ 'RED' ] + cplate[ 'BOLD' ] + self.FRESOL.format( ip ) + cplate[ 'END' ]

	def formatcdv(self, ca, cb, cplate):
		def code( _code ):
			if _code != "ERR":
				_code = int( _code )
				if _code >= 200 and _code < 300:
					return cplate[ 'GREEN' ] + cplate[ 'BOLD' ] + "{:<3.3}".format( str( _code ) ) + cplate[ 'END' ]
				elif _code >= 300 and _code < 400:
					return cplate[ 'YELLOW' ] + cplate[ 'BOLD' ] + "{:<3.3}".format( str( _code ) ) + cplate[ 'END' ]
				elif _code >= 400 and _code < 600:
					return cplate[ 'RED' ] + cplate[ 'BOLD' ] + "{:<3.3}".format( str( _code ) ) + cplate[ 'END' ]
			else:
				return "{:<3.3}".format( str( _code ) )

		return "{:<1.1}".format("[") + code( ca ) + "{:<1.1}".format("/") + code( cb ) + "{:<10.10}".format("]")

	def formatsvv(self, sa, sb, cplate):
		def server( _s1, _s2 ):
			if _s1 != "NONE" and _s2 != "NONE":
				return cplate[ 'BLUE' ] + cplate[ 'BOLD' ] + self.FSERVER.format( _s2 ) + cplate[ 'END' ]
			elif _s1 == "NONE" and _s2 != "NONE":
				return cplate[ 'BLUE' ] + cplate[ 'BOLD' ] + self.FSERVER.format( _s2 ) + cplate[ 'END' ]
			elif _s1 != "NONE" and _s2 == "NONE":
				return cplate[ 'BLUE' ] + cplate[ 'BOLD' ] + self.FSERVER.format( _s1 ) + cplate[ 'END' ]
			else:
				return self.FSERVER.format( _s1 )

		return server( sa, sb )

	def formatsbv( self, domain, subdomain ):
		return self.FSUBDOM.format( subdomain.replace( "." + domain, "" ) )

	def formatptv( self, _ports, cplate, stcount=20):
		tlen = len( ",".join( [str(pt) for pt in _ports] ) )
		if tlen > stcount:
			ff = ",".join( [str(pt) for pt in _ports] )[ :stcount ]
		else:
			ff = ",".join( [str(pt) for pt in _ports] )

		return cplate[ 'YELLOW' ] + self.FPORTS.format( ff ) + cplate[ 'END' ]

	def formatcnv( self, _cname, cplate ):
		return cplate[ 'BOLD' ] + cplate[ 'GREEN' ] + _cname + cplate[ 'END' ]
