import sys
if sys.version_info[0] != 3:
	sys.exit( "[~] Only Version 3 Supported!" )
import optparse
import re
import os
import socket
import time
import ssl
import csv
import requests
import random
import signal
import threading
import string
from dns import resolver
from subrake.pull import PULLY
from subrake.parser import PARSER
from subrake.round import ROUNDER
from subrake.handlers import GOOGLE
from subrake.handlers import BING
from subrake.handlers import YAHOO
from subrake.handlers import ASK
from subrake.handlers import BAIDU
from subrake.handlers import NETCRAFT
from subrake.handlers import DNSDUMPSTER
from subrake.handlers import VIRUSTOTAL
from subrake.handlers import THREATCROWD
from subrake.handlers import CRTSEARCH
from bs4 import BeautifulSoup as soup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

pull  = PULLY()
roll  = ROUNDER()
eeips = []

class NMHANDLER:

	def __init__(self, dm, eeips):
		self.domain = dm
		self.eeips  = eeips

	def query(self, _dm, _type):
		_ret = []
		try:
			_ret = resolver.query(_dm, _type)
		except:
			pass
		return _ret

	def def_ip(self):
		try:
			_ip = socket.gethostbyname( "%s.%s" % ( roll.rstring( ) , self.domain ) )
			pull.slasher( "Wildcard: * -> Resolving -> %s" % ( pull.YELLOW + _ip + pull.END ), pull.BOLD, pull.YELLOW )
		except:
			pull.slasher( "Wildcard: * -> Resolving -> NONE", pull.BOLD, pull.YELLOW )
			_ip = ""
		return _ip

	def def_cn(self):
		_cn = self.query( "%s.%s" % ( roll.rstring( ) , self.domain ), "CNAME" )
		if _cn:
			pull.slasher( "Redirect: * -> Resolving -> %s" % ( pull.YELLOW + str(_cn[0]) + pull.END ), pull.BOLD, pull.YELLOW )
			return str(_cn[0])
		else:
			pull.slasher( "Redirect: * -> Resolving -> NONE", pull.BOLD, pull.YELLOW )
			return ""

	def def_ps(self):
			pull.slasher( "Exclude : * -> Specified -> %s" % (pull.YELLOW + ",".join(self.eeips) + pull.END) )

class NAMESERVER:

	RECORDS = []

	def __init__(self, _dm, _eeips):
		self.domain = _dm
		self.eeips  = _eeips
		self.nameservers = self.query(_dm, "NS")
		self.mailservers = self.query(_dm, "MX")
		#self.txtrecords = self.query(_dm, "TXT")

	def save(self, _ty, _vals):
		for _rec in _vals:
			self.RECORDS.append( ( _ty, str(_rec) ) )

	def get(self):
		return self.RECORDS

	def query(self, _dm, _type):
		_ret = []
		try:
			_ret = resolver.query(_dm, _type)
		except:
			pass
		self.save( _type, _ret )
		return _ret

	def push(self):
		for (rt, rv) in self.RECORDS:
			pull.slasher( pull.YELLOW + rt + pull.END + " - " + rv, pull.BOLD, pull.YELLOW )

	def def_ip(self):
		try:
			_ip = socket.gethostbyname( "%s.%s" % ( roll.rstring( ) , self.domain ) )
			pull.slasher( "Wildcard: * -> Resolving -> %s" % ( pull.YELLOW + _ip + pull.END ), pull.BOLD, pull.YELLOW )
		except:
			pull.slasher( "Wildcard: * -> Resolving -> NONE", pull.BOLD, pull.YELLOW )
			_ip = ""
		return _ip

	def def_cn(self):
		_cn = self.query( "%s.%s" % ( roll.rstring( ) , self.domain ), "CNAME" )
		if _cn:
			pull.slasher( "Redirect: * -> Resolving -> %s" % ( pull.YELLOW + str(_cn[0]) + pull.END ), pull.BOLD, pull.YELLOW )
			return str(_cn[0])
		else:
			pull.slasher( "Redirect: * -> Resolving -> NONE", pull.BOLD, pull.YELLOW )
			return ""

	def def_ps(self):
			pull.slasher( "Exclude : * -> Specified -> %s" % ",".join(self.eeips) )

class ONLINE:

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
			pull.slasher( string, pull.BOLD, pull.YELLOW )
			return 0

		for ls in _ls:
			if ls not in self.SUBDOMAINS:
				self.SUBDOMAINS.append( ls )

		return push()

	def pause(self):
		while self.THREADS > 0:
			pass
		return

class ENGINE:

	STOPPRINTER = False
	ENGAGER     = True

	BROOTBRA = False
	BROOTBRE = False
	ERRORCOU = 0
	ERRORSUB = []
	CTHREADS = 0
	SCOUNTER = 0
	LOCK     = threading.Semaphore( value = 1 )
	RECORD   = {
	}
	HEADERS  = {
		"User-Agent": roll.AGENT,
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Accept-Language": "en-US,en;q=0.5",
		"DNT": "1",
		"Connection": "close",
		"Upgrade-Insecure-Requests": "1"
	}

	def __init__( self, _domain, _checklist, _defip, _eeips, _defcn, _osubs, _threads ):
		self.signal     = signal.signal(signal.SIGINT, self.ee_handler_1)
		self.domain     = _domain
		self.mthreads   = _threads
		self.defip      = _defip
		self.eeips      = _eeips
		self.defcn      = _defcn
		self.checklist  = self.parse( _checklist, _osubs )

	def empty_handler(self, sig, fr):
		return

	def ee_handler_1(self, sig, fr):
		self.signal   = signal.signal(signal.SIGINT, self.empty_handler)
		self.BROOTBRA = True

		while self.CTHREADS > 0:
			time.sleep(0.5)

		self.STOPPRINTER = True
		time.sleep(0.5)

		pull.linebreak( 1 )
		ii = input(pull.DARKCYAN + "[<] " + pull.END + "[E]xit / [S]kip / [C]ontinue: ")
		if ii in ('e', 'E'):
			pull.linebreak( 1 )
			pull.brick( pull.BOLD + "Received Interrupt -><- " + pull.END, pull.BOLD, pull.RED )
		elif ii in ('s', 'S'):
			self.BROOTBRA = False
			self.BROOTBRE = True
			self.signal   = signal.signal(signal.SIGINT, self.ee_handler_2)
		else:
			self.BROOTBRA = False
			self.signal     = signal.signal(signal.SIGINT, self.ee_handler_1)
			pass

	def ee_handler_2(self, sig, fr):
		pull.linebreak( 1 )
		pull.brick( pull.BOLD + "Received Interrupt -><- " + pull.END, pull.BOLD, pull.RED )

	def parse(self, _wd, _sb):
		_list = list(_wd) + list(_sb)
		for _ls in _list:
			_list[ _list.index(_ls) ] = (_ls + ".%s" % self.domain) if not _ls.endswith( ".%s"%self.domain ) else _ls
		return list( set( _list ) )

	def fmheaders(self):
		mcount = roll.maxcountp( self.domain, self.checklist, "." )
		roll.fmreplsb( mcount )

		pull.psheada( pull.DARKCYAN, rs=roll.FRESOL, cd=roll.FCODE, sv=roll.FSERVER, sb=roll.FSUBDOM )

	def request(self, _subdomain, _port):
		'''
		_req = "GET / HTTP/1.1\r\nHost: %s\r\nUser-Agent: %s\r\nOrigin: http://%s\r\n\r\n" % (_subdomain, roll.AGENT, _subdomain)

		_s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		_s.settimeout( 10 )

		try:
			if _port == 443:
				_s =  ssl.wrap_socket(_s, ssl_version=ssl.PROTOCOL_TLS)

			_s.connect((_subdomain, _port))
			_s.send( _req )

			resp, toadd, datalength = "", _s.recv( 2048 ), 1

			while datalength:
				datalength = len( toadd )
				resp += toadd
				if (datalength < 2048) or ("\r\n\r\n" in data):
					break
				toadd = _s.recv( 2048 )

			_s.close()
		except:
			resp = ""
		'''
		httpath = ("http://%s" % _subdomain) if _port == 80 else ("https://%s" % _subdomain)
		try:
			r = requests.get(httpath, headers=self.HEADERS, allow_redirects=False, timeout=10, verify=False)
			code = r.status_code
			headers = r.headers
		except:
			code = None
			headers = {}
			if _subdomain not in self.ERRORSUB:
				self.ERRORCOU += 1
				self.ERRORSUB.append(_subdomain)

		return roll.seperator( code, headers )

	def handler(self, _subdomain):
		self.CTHREADS += 1

		self.RECORD[ _subdomain ] = {

					80: {},
					443: {},
					'ip': '',
					'cname': '',
					'ports': []

				}

		rtval = self.request( _subdomain, 80 )
		self.RECORD[ _subdomain ][ 80 ]  = rtval
		rtval = self.request( _subdomain, 443 )
		self.RECORD[ _subdomain ][ 443  ] = rtval
		self.RECORD[ _subdomain ][ 'ip' ] = roll.iplocator( _subdomain, self.defip )

		rsv = roll.formatrsv( self.RECORD[ _subdomain ][ 'ip' ], self.defip, pull.MIXTURE )
		cdv = roll.formatcdv( self.RECORD[ _subdomain ][ 80 ][ 'cd' ], self.RECORD[ _subdomain ][ 443 ][ 'cd' ], pull.MIXTURE )
		svv = roll.formatsvv( self.RECORD[ _subdomain ][ 80 ][ 'sv' ], self.RECORD[ _subdomain ][ 443 ][ 'sv' ], pull.MIXTURE )
		sbv = roll.formatsbv( self.domain, _subdomain )

		self.LOCK.acquire()
		self.STOPPRINTER = True
		time.sleep(0.1)
		if self.RECORD[ _subdomain ][ 'ip' ] != self.defip and self.RECORD[ _subdomain ][ 'ip' ] != '' and self.RECORD[ _subdomain ][ 'ip' ] not in self.eeips:
			pull.psrowa( '', rsv=rsv, cdv=cdv, svv=svv, sbv=sbv )
		self.STOPPRINTER = False
		self.LOCK.release()

		self.SCOUNTER += 1
		self.CTHREADS -= 1

	def printer(self):
		while self.ENGAGER:
			while self.STOPPRINTER:
				time.sleep(0.5)

			if self.ENGAGER and not self.BROOTBRA:
				pull.lflush("STATUS! Remain [%d] Total [%d] ERRORS [%d]          " % ( len(self.checklist) - self.SCOUNTER, len(self.checklist), self.ERRORCOU) , pull.DARKCYAN, pull.BOLD)
			elif self.BROOTBRA:
				pull.lflush("PAUSE! Stopping ... Remain [%d]                     " % self.CTHREADS, pull.DARKCYAN, pull.BOLD)

	def engage(self):
		t = threading.Thread(target=self.printer)
		t.daemon = True
		t.start()

		for tocheck in self.checklist:
			if self.BROOTBRE:
				break

			_t = threading.Thread( target=self.handler, args=( tocheck, ) )
			_t.daemon = True
			_t.start()

			while self.CTHREADS >= self.mthreads or self.BROOTBRA:
				if self.BROOTBRE:
					break
				time.sleep( 0.5 )

		while self.CTHREADS > 0:
			if self.BROOTBRE:
				break
			time.sleep( 0.5 )

		self.ENGAGER = False

	def engrosser(self, _subdomain, _ports):
		self.CTHREADS += 1

		try:
			if self.RECORD[ _subdomain ][ 'ip' ] != self.defip:
				self.RECORD[ _subdomain ][ 'cname' ] = roll.cnlocator( _subdomain, self.defcn )
				if _ports:
					self.RECORD[ _subdomain ][ 'ports' ] = roll.ptlocator( _subdomain, _ports )

			cdv = roll.formatcdv( self.RECORD[ _subdomain ][ 80 ][ 'cd' ], self.RECORD[ _subdomain ][ 443 ][ 'cd' ], pull.MIXTURE )
			sbv = roll.formatsbv( self.domain, _subdomain )
			ptv = roll.formatptv( self.RECORD[ _subdomain ][ 'ports' ], pull.MIXTURE )
			cnv = roll.formatcnv( self.RECORD[ _subdomain ][ 'cname' ], pull.MIXTURE )

			self.LOCK.acquire()
			if self.RECORD[ _subdomain ][ 'ip' ] != self.defip and self.RECORD[ _subdomain ][ 'ip' ] != '' and self.RECORD[ _subdomain ][ 'ip' ] not in self.eeips:
				pull.psrowb( '', cdv=cdv, sbv=sbv, ptv=ptv, cnv=cnv )
			self.LOCK.release()
		except KeyError:
			pass

		self.CTHREADS -= 1

	def engross(self, _ports):
		for tocheck in self.checklist:
			_t = threading.Thread( target=self.engrosser, args=( tocheck, _ports ) )
			_t.daemon = True
			_t.start()

			while self.CTHREADS >= self.mthreads:
				time.sleep( 0.5 )

		while self.CTHREADS > 0:
			time.sleep( 0.5 )

	def get(self):
		return self.RECORD

class WRITER:

	TRASH   = set()
	BASKETA = {}
	BASKETB = {}
	RECORD  = {}

	def __init__(self, _dom, _out, _csv, _rec, _dip, _eeips, _dcn):
		self.domain = _dom
		self.output = _out
		self.csvout = _csv
		self.record = _rec
		self.defipa = _dip
		self.eeips  = _eeips
		self.defcna = _dcn

	def nmwritetxt(self):
		if self.output:
			fl = open( self.output, 'w' )
			for (subdomain, fdict) in self.record.items():
				if fdict[ 'ip' ] and fdict[ 'ip' ] != self.defipa and fdict['ip'] not in self.eeips:
					fl.write( subdomain + "\n" )

	def nmwritecsv(self):
		if self.csvout:
			fl = csv.writer( open(self.csvout, "w") )
			fl.writerow([
				"RESOLUTION",
				"[HTTP/HTTPS]",
				"SERVER",
				"SUBDOMAIN",
				"CNAME",
				"PORTS"
			])
			roll.FSERVER = "{:<}"
			for (subdomain, fdict) in self.record.items():
				fl.writerow([
					fdict[ 'ip' ],
					"[" + fdict[80]['cd'] + "/" + fdict[443]['cd'] + "]",
					roll.formatsvv( fdict[80]['sv'], fdict[443]['sv'], pull.VACANT ),
					subdomain,
					fdict['cname'],
					",".join( fdict['ports'] )
				])

	def flwritetxt(self):
		if self.output:
			fl = open( self.output, 'w' )
			for (subdomain, fdict) in self.record.items():
				if fdict[ 'ip' ] and fdict[ 'ip' ] != self.defipa and fdict['ip'] not in self.eeips:
					fl.write( subdomain + "\n" )

	def flwritecsv(self):
		if self.csvout:
			fl = csv.writer( open( self.csvout, "w" ) )
			fl.writerow([
				"RESOLUTION",
				"[HTTP/HTTPS]",
				"SERVER",
				"SUBDOMAIN",
				"CNAME",
				"PORTS"
			])
			roll.FCODE   = "{:<}"
			roll.FSERVER = "{:<}"
			for (ip, subdomains) in self.BASKETA.items():
				if ip != self.defipa and ip != '' and ip not in self.eeips:
					for subdomain in subdomains:
						fl.writerow([
							self.record[ subdomain ][ 'ip' ],
							roll.formatcdv( self.record[ subdomain ][80]['cd'], self.record[ subdomain ][443]['cd'], pull.VACANT ),
							roll.formatsvv( self.record[ subdomain ][80]['sv'], self.record[ subdomain ][443]['sv'], pull.VACANT ),
							subdomain,
							self.record[ subdomain ][ 'cname' ],
							",".join( self.record[ subdomain ]['ports'] )
						])
					fl.writerow([ " " ])

	def engage(self):
		for (subdomain, fdict) in self.record.items():
			if fdict[ 'ip' ] and fdict[ 'ip' ] != self.defipa and fdict[ 'ip' ] not in self.eeips:
				self.TRASH.add( fdict[ 'ip' ] )
				self.BASKETA[ fdict[ 'ip' ] ] = set()

		for ip in self.TRASH:
			for (subdomain, fdict) in self.record.items():
				if ip == fdict[ 'ip' ]:
					self.BASKETA[ ip ].add( subdomain )

		self.TRASH = set()

		for (subdomain, fdict) in self.record.items():
			if fdict[ 'cname' ] and fdict[ 'cname' ] != self.defcna:
				self.TRASH.add( fdict[ 'cname' ] )
				self.BASKETB[ fdict[ 'cname' ] ] = set()

		for cn in self.TRASH:
			for (subdomain, fdict) in self.record.items():
				if cn == fdict[ 'cname' ]:
					self.BASKETB[ cn ].add( subdomain )

def main():
	parser = optparse.OptionParser( add_help_option=False )

	parser.add_option('-h', '--help', dest='help', action='store_true', default=False)
	parser.add_option('-d', '--domain', dest="domain", type="string", default="")
	parser.add_option('-w', '--wordlists', dest="wordlists", type="string", default="")
	parser.add_option('-t', '--threads', dest="threads", type="int", default=20)
	parser.add_option('-o', '--output', dest="output", type="string", default="")
	parser.add_option('-c', '--csv', dest="csv", type="string", default="")
	parser.add_option('-p', '--ports', dest="ports", type="string", default="")
	parser.add_option('-s', '--skip-search', dest="online", action="store_false", default=True)
	parser.add_option(''  , '--filter', dest="filter", action="store_true", default=False)
	parser.add_option(''  , '--skip-dns'  , dest="sdns", action="store_true", default=False)
	parser.add_option(''  , '--exclude-ips', dest="eeips", type=str, default="")

	(options, args) = parser.parse_args()

	pull.logo()

	if options.help:
		pull.help(); sys.exit(0)
	else:
		pull.linebreak()
		parser  = PARSER( options, args )
		pull.gthen( "CREATED ENVIRONMENT. EVERYTHING IN PLACE", pull.BOLD, pull.DARKCYAN )
		if not parser.skipdns:
			pull.gthen( "DNS Records ->", pull.BOLD, pull.DARKCYAN )
			pull.linebreak( 1 )
			dnssec  = NAMESERVER( parser.domain, parser.eeips )
			dnssec.push()
			dnsrec  = dnssec.get()
			pull.linebreak( 1 )
		else:
			dnssec  = NMHANDLER( parser.domain, parser.eeips )

		pull.gthen( "Looking for Possible False Positives ->", pull.BOLD, pull.DARKCYAN )
		pull.linebreak( 1 )
		dip     = dnssec.def_ip()
		dcn     = dnssec.def_cn()
		dnssec.def_ps()
		pull.linebreak( 1 )

		if parser.online:
			pull.gthen( "Looking for Subdomains Online ->", pull.BOLD, pull.DARKCYAN )
			pull.linebreak()
			oenum = ONLINE( parser.domain )
			oenum.enumerate()
			oenum.pause()
			osubs = oenum.acquire()
			pull.linebreak()
		else:
			osubs = list()

		pull.gthen( "Looking for subdomains with finite Resolution", pull.BOLD, pull.DARKCYAN )
		pull.linebreak()
		eenge = ENGINE( parser.domain, parser.checklist, dip, parser.eeips, dcn, osubs, parser.threads )
		eenge.fmheaders()
		eenge.engage()
		pull.linebreak()
		pull.linebreak()
		pull.gthen( "Resolving subdomains to their CNAME", pull.BOLD, pull.DARKCYAN )
		pull.linebreak()
		pull.psheadb( pull.DARKCYAN, cdh=roll.FCODE, sbh=roll.FSUBDOM, pth=roll.FPORTS, cnh=roll.FCNAME )
		eenge.engross( parser.ports )
		pull.linebreak( 1 )

		fpush = WRITER(parser.domain, parser.output, parser.csv, eenge.get(), dip, parser.eeips, dcn)

		if parser.filter:
			pull.gthen( "Filtering domains with Clashing IPs", pull.BOLD, pull.DARKCYAN )
			fpush.engage()
			pull.lthen( "Done!", pull.BOLD, pull.GREEN )
			pull.linebreak()

			if parser.output or parser.csv:
				pull.gthen( "Writing Output", pull.BOLD, pull.DARKCYAN )
				pull.linebreak()
				fpush.flwritetxt()
				fpush.flwritecsv()
		else:
			if parser.output or parser.csv:
				pull.gthen( "Writing Output", pull.BOLD, pull.DARKCYAN )
				pull.linebreak()
				fpush.nmwritetxt()
				fpush.nmwritecsv()

		pull.lthen( "DONE!", pull.BOLD, pull.RED )

if __name__ == "__main__":
	main()
