import sys
import os
import signal
import re
from subrake.pull import PULLY

pull = PULLY()

class PARSER:

	def __init__(self, _opts, _args):
		#self.signal     = signal.signal( signal.SIGINT, self.sig_handler )
		#self.sigalm     = signal.signal( signal.SIGALRM, self.exp_handler )
		self.help       = _opts.help
		self.domain     = self.parse_domain(    _opts.domain    )
		self.online     = self.parse_online(    _opts.online    )
		self.checklist  = self.parse_wordlists( _opts.wordlists )
		self.threads    = self.parse_threads(   _opts.threads   )
		self.output     = self.parse_output(    _opts.output    )
		self.csv        = self.parse_csv(       _opts.csv       )
		self.ports      = self.parse_ports(     _opts.ports     )
		self.eeips      = self.parse_eeips(     _opts.eeips     )
		self.filter     = _opts.filter
		self.skipdns    = _opts.sdns

	def parse_domain(self, _dm):
		if _dm:
			if re.match("^([a-z0-9|-]+\.)*[a-z0-9|-]+\.[a-z]+$", _dm.lower(), re.I):
				return _dm.lower()
			else:
				pull.brick( "MISCONF! Invalid Domain Received.", pull.BOLD, pull.RED )
		else:
			pull.brick( "MISCONF! Domain not Found. You forgot to specify a domain." )

	def parse_wordlists(self, _wds):
		_list = []

		if not _wds:
			if not self.online:
				pull.brick( "OOPS! You forgot the dictionary.", pull.BOLD, pull.RED)
		else:
			for fl in set( _wds.split(",") ):
				if not os.path.isfile( fl ):
					pull.brick( "Invalid! Not Found: %s" % fl, pull.BOLD, pull.RED )
				else:
					_file = open( fl, 'r' )
					for _ln in _file.read().splitlines():
						_list.append( _ln )

		return list(set(_list))

	def parse_threads(self, _th):
		if type(_th) == int:
			return _th
		else:
			pull.brick( "Invalid! Threads must be an Integer.", pull.BOLD, pull.RED )

	def parse_output(self, _out):
		if _out:
			return _out
		else:
			return False

	def parse_csv(self, _csv):
		if _csv:
			return _csv
		else:
			return False

	def parse_ports(self, _pts):
		_list = []

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
						pull.brick( "Invalid! Not a Valid Port! %s" % pt, pull.BOLD, pull.RED)
				except ValueError:
					pull.error( "Invalid! Not a Valid Port! %s" % pt, pull.BOLD, pull.RED )

		return list(set(_list))

	def parse_online(self, _bool):
		if _bool:
			return True
		return False

	def parse_eeips(self, _ips):
		rtval = []
		if _ips:
			for ip in _ips.split(","):
				rtval.append(ip)

		return rtval

	def sig_handler(self, _sig, _fr):
		pull.linebreak( 1 )
		pull.brick( pull.BOLD + "Received Interrupt -><- " + pull.END, pull.BOLD, pull.RED )

	def exp_handler(self, _sig, _fr):
		raise ValueError( "Random Error Passed!" )
