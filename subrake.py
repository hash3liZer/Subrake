import sys
if sys.version_info[0] != 2:
	sys.exit( "[~] Currently only works with Python Version 2." )
import optparse
import re
import os
import socket
import time
import ssl
import csv
import requests
import random
import threading
import string
from dns import resolver
from pull import PULLY
from parser import PARSER
from round import ROUNDER
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
roll = ROUNDER()

class NMHANDLER:

	def __init__(self, dm):
		self.domain = dm

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

class NAMESERVER:

	RECORDS = []

	def __init__(self, _dm):
		self.domain = _dm
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

	CTHREADS = 0
	LOCK     = threading.Semaphore( value = 1 )
	RECORD  = {
	}

	def __init__( self, _domain, _checklist, _defip, _defcn, _osubs, _threads ):
		self.domain     = _domain
		self.mthreads   = _threads
		self.defip      = _defip
		self.defcn      = _defcn
		self.checklist  = self.parse( _checklist, _osubs )

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

		return roll.seperator( resp )

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
		pull.lflush("STATUS! Remain [%d] Total [%d]" % ( ( len(self.checklist) - (self.checklist.index( _subdomain )+1) ), len(self.checklist) ) , pull.DARKCYAN, pull.BOLD)
		if self.RECORD[ _subdomain ][ 'ip' ] != self.defip:
			pull.psrowa( '', rsv=rsv, cdv=cdv, svv=svv, sbv=sbv )
		self.LOCK.release()

		self.CTHREADS -= 1

	def engage(self):
		for tocheck in self.checklist:
			_t = threading.Thread( target=self.handler, args=( tocheck, ) )
			_t.daemon = True
			_t.start()

			while self.CTHREADS >= self.mthreads:
				time.sleep( 0.5 )

		while self.CTHREADS > 0:
			time.sleep( 0.5 )

	def engrosser(self, _subdomain, _tsc, _ports):
		self.CTHREADS += 1

		if self.RECORD[ _subdomain ][ 'ip' ] != self.defip:
			self.RECORD[ _subdomain ][ 'cname' ] = roll.cnlocator( _subdomain, self.defcn )
			if _tsc:
				self.RECORD[ _subdomain ][ 'ports' ] = roll.ptlocator( _subdomain, _ports )

		cdv = roll.formatcdv( self.RECORD[ _subdomain ][ 80 ][ 'cd' ], self.RECORD[ _subdomain ][ 443 ][ 'cd' ], pull.MIXTURE )
		sbv = roll.formatsbv( self.domain, _subdomain )
		ptv = roll.formatptv( self.RECORD[ _subdomain ][ 'ports' ], pull.MIXTURE )
		cnv = roll.formatcnv( self.RECORD[ _subdomain ][ 'cname' ], pull.MIXTURE )

		self.LOCK.acquire()
		if self.RECORD[ _subdomain ][ 'ip' ] != self.defip:
			pull.psrowb( '', cdv=cdv, sbv=sbv, ptv=ptv, cnv=cnv )
		self.LOCK.release()

		self.CTHREADS -= 1

	def engross(self, _tsc, _ports):
		for tocheck in self.checklist:
			_t = threading.Thread( target=self.engrosser, args=( tocheck, _tsc, _ports ) )
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

	def __init__(self, _dom, _out, _csv, _sub, _rec, _dip, _dcn):
		self.domain = _dom
		self.output = _out
		self.csvout = _csv
		self.subdos = _sub
		self.record = _rec
		self.defipa = _dip
		self.defcna = _dcn

	def nmwritetxt(self):
		if self.output:
			fl = open( self.output, "w" )
			fl.write( "".join([
				roll.FRESOL.format("RESOLUTION"), 
				roll.FCODE.format("[HTTP/HTTPS]"),
				roll.FSERVER.format("SERVER"),
				roll.FSUBDOM.format("SUBDOMAIN"),
				"{:<28.27}".format("CNAME"),
				roll.FPORTS.format("PORTS"),
				"\n"
			]))
			for (subdomain, fdict) in self.record.items():
				fl.write( "".join([
					roll.formatrsv(fdict['ip'], self.defipa, pull.VACANT),
					roll.formatcdv(fdict[80]['cd'], fdict[443]['cd'], pull.VACANT),
					roll.formatsvv(fdict[80]['sv'], fdict[443]['sv'], pull.VACANT),
					roll.formatsbv(self.domain, subdomain),
					"{:<28.27}".format(fdict['cname']),
					roll.formatptv(fdict['ports'], pull.VACANT),
					"\n"
				]))

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
			fl = open( self.output, "w" )
			fl.write( "".join([
				roll.FRESOL.format("RESOLUTION"), 
				roll.FCODE.format("[HTTP/HTTPS]"),
				roll.FSERVER.format("SERVER"),
				roll.FSUBDOM.format("SUBDOMAIN"),
				"{:<28.27}".format("CNAME"),
				roll.FPORTS.format("PORTS"),
				"\n"
			]) )
			for (ip, subdomains) in self.BASKETA.items():
				if ip != self.defipa:
					for subdomain in subdomains:
						fl.write( "".join([
							roll.formatrsv( self.record[ subdomain ]['ip'], self.defipa, pull.VACANT ),
							roll.formatcdv( self.record[ subdomain ][80]['cd'], self.record[ subdomain ][443]['cd'], pull.VACANT ),
							roll.formatsvv( self.record[ subdomain ][80]['sv'], self.record[ subdomain ][443]['sv'], pull.VACANT ),
							roll.formatsbv( self.domain, subdomain ),
							"{:<28.27}".format( self.record[ subdomain ][ 'cname' ] ),
							roll.formatptv( self.record[ subdomain ]['ports'], pull.VACANT ),
							"\n"
						]) )
					fl.write( "\n" )

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
				if ip != self.defipa:
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

	def writesubs(self):
		if self.subdos:
			fl = open( self.subdos, 'w' )
			for (subdomain, fdict) in self.record.items():
				if fdict[ 'ip' ] and fdict[ 'ip' ] != self.defipa:
					fl.write( subdomain + "\n" )

	def engage(self):
		for (subdomain, fdict) in self.record.items():
			if fdict[ 'ip' ] and fdict[ 'ip' ] != self.defipa:
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
	parser.add_option('-p', '--ports', dest="ports", type="string", default=roll.PORTS)
	parser.add_option('-s', '--search', dest="online", action="store_true", default=False)
	parser.add_option(''  , '--filter', dest="filter", action="store_true", default=False)
	parser.add_option(''  , '--subs', dest="subs", type="string", default="")
	parser.add_option(''  , '--scan-ports', dest="scan", action="store_true", default=False)
	parser.add_option(''  , '--skip-dns'  , dest="sdns", action="store_true", default=False)

	(options, args) = parser.parse_args()

	pull.logo()

	if options.help:
		pull.help(); sys.exit(0)
	else:
		parser  = PARSER( options, args )
		pull.gthen( "CREATED ENVIRONMENT. EVERYTHING IN PLACE", pull.BOLD, pull.DARKCYAN )
		if not parser.skipdns:
			pull.gthen( "DNS Records ->", pull.BOLD, pull.DARKCYAN )
			pull.linebreak( 1 )
			dnssec  = NAMESERVER( parser.domain )
			dnssec.push()
			dnsrec  = dnssec.get()
			pull.linebreak( 1 )
		else:
			dnssec  = NMHANDLER( parser.domain )
	
		pull.gthen( "False Positive Detection ->", pull.BOLD, pull.DARKCYAN )
		pull.linebreak( 1 )
		dip     = dnssec.def_ip()
		dcn     = dnssec.def_cn()
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

		pull.gthen( "Starting Brute Engine. Validating sub-domains ->", pull.BOLD, pull.DARKCYAN )
		pull.linebreak()
		eenge = ENGINE( parser.domain, parser.checklist, dip, dcn, osubs, parser.threads )
		eenge.fmheaders()
		eenge.engage()
		pull.linebreak()
		pull.gthen( "Starting Brute Gun. Looking For Specifics ->", pull.BOLD, pull.DARKCYAN )
		pull.linebreak()
		pull.psheadb( pull.DARKCYAN, cdh=roll.FCODE, sbh=roll.FSUBDOM, pth=roll.FPORTS, cnh=roll.FCNAME )
		eenge.engross( parser.scan, parser.ports )
		pull.linebreak( 1 )

		fpush = WRITER(parser.domain, parser.output, parser.csv, parser.subs, eenge.get(), dip, dcn)

		if parser.filter:
			pull.gthen( "Filtering Items for You. Suitable for larger assets -><-", pull.BOLD, pull.DARKCYAN )
			fpush.engage()
			pull.lthen( "Items Filtered. Output Finalized! ", pull.BOLD, pull.GREEN )
			pull.linebreak()

			if parser.output or parser.csv:
				pull.gthen( "Writing Your Desired Output ->", pull.BOLD, pull.DARKCYAN )
				pull.linebreak()
				fpush.flwritetxt()
				fpush.flwritecsv()
		else:
			if parser.output or parser.csv:
				pull.gthen( "Writing Your Desired Output ->", pull.BOLD, pull.DARKCYAN )
				pull.linebreak()
				fpush.nmwritetxt()
				fpush.nmwritecsv()

		if parser.subs:
			fpush.writesubs()

		pull.lthen( "DONE!", pull.BOLD, pull.RED )

if __name__ == "__main__":
	main()