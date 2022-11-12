from subrake.pull import PULLY

pull = PULLY()

class SUBCAST:

    def __init__(self, prs):
        self.domain = prs.domain

    def engage(self):
        pull.gthen("Running SUBCAST as part of subdomain generation to get more subdomains. ", pull.BOLD, pull.YELLOW)

        if not pull.is_linux():
            pull.lthen("Skipping SUBCAST as the underlying operating system is not Linux!", pull.BOLD, pull.RED)
            return

        if not pull.is_xterm():
            pull.lthen("Skipping SUBCAST as the package xterm is not installed!", pull.BOLD, pull.RED)
            return
