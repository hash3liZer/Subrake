import sys
import os
import random

__logo__ = """%s
  ______            _____              ______
 /_/_/__/      |    | \\  \       |     | |  /
 \______       |___ |__\\_/  __   |  /  |____\\
   _____\ |  | |\\  ||   /  /\\ \  | /   |    /
  /_/_/_/ |__| |_\\_||   \_ \_\\/_/| \\_/\\|_|__\\
%s      
                               %sv1.0. @hash3liZer%s
"""

__help__ = """
Description:
            A subdomain Enumeration tool for identifying subdomains, their response codes on HTTP and HTTPS, Possible used server using headers and CNAMES of identified subdomains.

Syntax: 
    $ python subrake -d shellvoide.com -w small     // SMALL wordlist scan
    $ python subrake -d shellvoide.com -w large --threads 30

Options:
   Args               Description                      Default
   -h, --help         Show this manual                  NONE
   -d, --domain       Target domain. Possible
                      example: [example.com]            NONE
   -w, --wordlist     Wordlist for subdomains
                      to test. Two internal wordlists
                      can be specified as `small` and
                      `large`.                          NONE
   -t, --threads      Number of threads to spawn         25
   -o, --output       Push discovered subdomains to
                      an output file in csv format      NONE
"""

class PULLY:

	WHITE = '\033[0m'
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'
	LINEUP = '\033[F'

	def __init__(self):
		if not self.support_colors:
			self.win_colors()

	def support_colors(self):
		plat = sys.platform
		supported_platform = plat != 'Pocket PC' and (plat != 'win32' or \
														'ANSICON' in os.environ)
		is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
		if not supported_platform or not is_a_tty:
			return False
		return True


	def win_colors(self):
		self.WHITE = ''
		self.PURPLE = ''
		self.CYAN = ''
		self.DARKCYAN = ''
		self.BLUE = ''
		self.GREEN = ''
		self.YELLOW = ''
		self.RED = ''
		self.BOLD = ''
		self.UNDERLINE = ''
		self.END = ''

	def error(self, statement, *args, **kwargs):
		print "%s[!]%s %s" % (self.BOLD+self.RED, self.END, statement)
		return

	def up(self, statement, *args, **kwargs):
		print "%s[^]%s %s" % (self.BOLD+self.BLUE, self.END, statement)
		return

	def normal(self, statement, *args, **kwargs):
		print statement

	def right(self, statement, *args, **kwargs):
		print "%s[>]%s %s" % (self.DARKCYAN, self.END, statement)

	def slash(self, statement, *args, **kwargs):
		print "%s - %s %s" % (self.YELLOW, self.END, statement)

	def info(self, statement, *args, **kwargs):
		print "%s[*]%s %s" % (self.BOLD+self.YELLOW, self.END, statement)
		return

	def indent(self, statement, *args, **kwargs):
		if kwargs.has_key("spaces"):
			print (" "*kwargs["spaces"]) + "%s-%s %s" % (self.YELLOW, self.END, statement)
		else:
			self.error("Spaces not specified...")

	def linebreak(self):
		sys.stdout.write("\n")

	def lineup(self, time=0):
		if time != 0:
			for n in range(0, time):
				sys.stdout.write(self.LINEUP)
		else:
			sys.stdout.write(self.LINEUP)

	def logo(self):
		_tochoose = [self.BLUE, self.YELLOW, self.RED, self.DARKCYAN, self.GREEN]
		print __logo__ % (self.BOLD+random.choice(_tochoose), self.END, self.BOLD, self.END)

	def help(self):
		print __help__