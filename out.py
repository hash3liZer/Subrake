import curses
import time

class TABULATOR:

	__TABS = []

	def __init__(self, _hd, _pull, verbosity=True):
		self.hd = _hd
		self.pull = _pull
		self.verbose = verbosity
		self.get_headers()

	def get_headers(self):
		_headers = "{:<15}\t{:<10}\t{:<14}\t{:<18}\t{:<22}".format( self.hd[0], self.hd[1], self.hd[2], self.hd[3], self.hd[4] )
		self.pull.normal( _headers )

	def exit(self):
		pass

	def addin(self, _list):
		self.__TABS.append(_list)

	def push(self, _list):
		_str = "{:<15}\t{:<10}\t{:<14}\t{:<18}\t{:<22}".format( _list[0], _list[1], _list[2], _list[3], _list[4] )
		self.pull.normal(_str)
		
