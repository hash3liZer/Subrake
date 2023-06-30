from subrake.pull import PULLY
import dns.resolver
import threading
import time
import socket
import re

pull = PULLY()

class ZONETAKEOVER:

    __NOT_RESPONSIVE = []
    __GUESSED_SIGNATURES = set()

    # https://github.com/indianajson/can-i-take-over-dns
    __SIGNATURES = {
        "AWS": {
            "status": f"{pull.RED}Not Vulnerable{pull.END}",
            "regex": r"ns-.*\.awsdns-.*\.(org|co\.uk|com|net)",
            "records": [
                "ns-****.awsdns-*.org",
                "ns-****.awsdns-*.co.uk",
                "ns-****.awsdns-*.com",
                "ns-****.awsdns-*.net"
            ]
        },
        "000Domains": {
            "status": f"{pull.GREEN}Vulnerable{pull.END}",
            "regex": r".*ns\d\.000domains\.com",
            "records": [
                "ns1.000domains.com",
                "ns2.000domains.com",
                "fwns1.000domains.com",
                "fwns2.000domains.com"
            ]
        },
        "Azure": {
            "status": f"{pull.YELLOW}Edge Case{pull.END}",
            "regex": r"ns(\d)+\-(.*)\.azure-dns\.(com|net|org|info)",
            "records": [
                "ns1-**.azure-dns.com",
                "ns2-**.azure-dns.net",
                "ns3-**.azure-dns.org",
                "ns4-**.azure-dns.info"
            ]
        },
        "Bizland": {
            "status": f"{pull.YELLOW}No New Accounts{pull.END}",
            "regex": r"(ns1|ns2|clickme|clickme2)\.(bizland|click2site)\.com",
            "records": [
                "ns1.bizland.com",
                "ns2.bizland.com",
                "clickme.click2site.com",
                "clickme2.click2site.com"
            ]
        },
        "Cloudflare": {
            "status": f"{pull.YELLOW}Edge Case{pull.END}",
            "regex": r"(.*)\.ns\.cloudflare\.com",
            "records": [
                "*.ns.cloudflare.com"
            ]
        },
        "DigitalOcean": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"ns\d\.digitalocean\.com",
            "records": [
                "ns1.digitalocean.com",
                "ns2.digitalocean.com",
                "ns3.digitalocean.com"
            ]
        },
        "DNSimple": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"ns\d\.dnsimple\.com",
            "records": [
                "ns1.dnsimple.com",
                "ns2.dnsimple.com",
                "ns3.dnsimple.com",
                "ns4.dnsimple.com"
            ]
        },
        "DNSMadeEasy": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"ns(\d)+\.dnsmadeeasy\.com",
            "records": [
                "ns**.dnsmadeeasy.com",
            ]
        },
        "Domain.com": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"ns(\d)+\.domain\.com",
            "records": [
                "ns1.domain.com",
                "ns2.domain.com",
            ]
        },
        "DomainPeople": {
            "status": f"{pull.GREEN}Not Vulnerable{pull.END}",
            "regex": r"ns(\d)+\.domainpeople\.com",
            "records": [
                "ns1.domainpeople.com",
                "ns2.domainpeople.com",
            ]
        },
        "Dotster": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"(ns1|ns2)\.(dotster|nameresolve)\.com",
            "records": [
                "ns1.dotster.com",
                "ns2.dotster.com",
                "ns1.nameresolve.com",
                "ns2.nameresolve.com"
            ]
        },
        "EasyDNS": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"dns\d\.easydns\.(com|net|org|info)",
            "records": [
                "dns1.easydns.com",
                "dns2.easydns.net",
                "dns3.easydns.org",
                "dns4.easydns.info"
            ]
        },
        "Gandi.net": {
            "status": f"{pull.GREEN}Not Vulnerable{pull.END}",
            "regex": r"(a|b|c)\.dns\.gandi\.net",
            "records": [
                "a.dns.gandi.net",
                "b.dns.gandi.net",
                "c.dns.gandi.net"
            ]
        },
        "Google Cloud": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"ns-cloud-(\d)+\.googledomains\.com",
            "records": [
                "ns-cloud-**.googledomains.com",
            ]
        },
        "Hostinger": {
            "status": f"{pull.GREEN}Not Vulnerable{pull.END}",
            "regex": r"ns(\d)+\.hostinger\.com",
            "records": [
                "ns1.hostinger.com",
                "ns2.hostinger.com",
            ]
        },
        "Hover": {
            "status": f"{pull.RED}Not Vulnerable{pull.END}",
            "regex": r"ns(\d)+\.hover\.com",
            "records": [
                "ns1.hover.com",
                "ns2.hover.com",
            ]
        },
        "Hurricane Electric": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"ns(\d)+\.he\.net",
            "records": [
                "ns1.he.net",
                "ns2.he.net",
                "ns3.he.net",
                "ns4.he.net",
                "ns5.he.net",
                "ns6.he.net"
            ]
        },
        "Linode": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"ns(\d)+\.linode\.com",
            "records": [
                "ns1.linode.com",
                "ns2.linode.com",
            ]
        },
        "MediaTemple": {
            "status": f"{pull.GREEN}Not Vulnerable{pull.END}",
            "regex": r"ns(\d)+\.mediatemple\.net",
            "records": [
                "ns1.mediatemple.net",
                "ns2.mediatemple.net",
            ]
        },
        "MyDomain": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"ns(\d)+\.mydomain\.com",
            "records": [
                "ns1.mydomain.com",
                "ns2.mydomain.com",
            ]
        },
        "Name.com": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"ns(.*)\.name\.com",
            "records": [
                "ns*.name.com",
            ]
        },
        "Namecheap": {
            "status": f"{pull.GREEN}Not Vulnerable{pull.END}",
            "regex": r"(.+)\.(namecheaphosting|registrar-servers)\.com",
            "records": [
                "*.namecheaphosting.com",
                "*.registrar-servers.com",
            ]
        },
        "Network Solutions": {
            "status": f"{pull.GREEN}Not Vulnerable{pull.END}",
            "regex": r"ns(.*)\.worldnic\.com",
            "records": [
                "ns*.worldnic.com",
            ]
        },
        "NS1": {
            "status": f"{pull.YELLOW}No Open Registration{pull.END}",
            "regex": r"dns\d\.p(.*)\.nsone\.net",
            "records": [
                "dns*.p*.nsone.net",
            ]
        },
        "TierraNet": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"ns(\d)+\.domaindiscover\.net",
            "records": [
                "ns1.domaindiscover.com",
                "ns2.domaindiscover.com",
            ]
        },
        "Reg.ru": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"ns(\d)+\.reg\.ru",
            "records": [
                "ns1.reg.ru",
                "ns2.reg.ru",
            ]
        },
        "UltraDNS": {
            "status": f"{pull.GREEN}Not Vulnerable{pull.END}",
            "regex": r"[pus]dns(.*)\.ultradns\.(com|net)",
            "records": [
                "pdns*.ultradns.com",
                "sdns*.ultradns.net",
                "udns*.ultradns.net",
            ]
        },
        "Yahoo Small Business": {
            "status": f"{pull.RED}Vulnerable{pull.END}",
            "regex": r"yns(\d)+\.yahoo\.com",
            "records": [
                "yns1.yahoo.com",
                "yns2.yahoo.com",
            ]
        }
    }

    def __init__(self, domain, records, threads=25):
        self.domain = domain
        self.records = records
        self.threads = threads

    def filter(self):
        '''
            Filter out NS records from the list of DNS Records
        '''
        for record in self.records:
            if record[0] != "NS":
                self.records.remove(record)

    def check_signature(self, record):
        '''
            Validate against given signatures defined in __SIGNATURES
        '''
        for (signature, _base) in self.__SIGNATURES.items():
            if re.search(_base["regex"], record):
                self.__GUESSED_SIGNATURES.add(signature)

    def check_dns_takeover(self, record):
        '''
            Check DNS Zone Takeover by checking for SOA record in each DNS Server of the domain
        '''
        for n in range(3):
            try:
                _resolved = socket.gethostbyname(record[:-1] if record[-1] == '.' else record)
                break
            except:
                if n == 2:
                    return

        resolver = dns.resolver.Resolver(configure=False)
        resolver.timeout = 10
        resolver.lifetime = 10
        resolver.nameservers = [
            _resolved
        ]
        
        result = False
        try:
            answers = resolver.query(self.domain, 'SOA')
            if answers:
                result = True
        except:
            pass

        if not result:
            pull.slasher(
                f"Not Responsive: {pull.RED}[{record}]{pull.END}",
                pull.BOLD,
                pull.YELLOW
            )
            self.__NOT_RESPONSIVE.append(record)

    def engage(self):
        self.filter()

        pull.gthen(
            f"Checking resolve status for NS {pull.RED}[{len(self.records)}]{pull.END} | Concurrency: {pull.RED}[{self.threads}]{pull.END}",
            pull.BOLD,
            pull.GREEN
        )
        pull.linebreak()

        for record in self.records:
            t = threading.Thread(target=self.check_dns_takeover, args=(record[1],))
            t.daemon = True
            t.start()

            while threading.active_count() >= self.threads:
                time.sleep(1)

        while threading.active_count() > 1:
            time.sleep(1)

        if not self.__NOT_RESPONSIVE:
            pull.gthen(
                f"No DNS Zone Takeover Discovered. All Seems good. Moving on...",
                pull.BOLD,
                pull.GREEN
            )
            pull.linebreak()
    
    def guess_signature(self):
        if self.__NOT_RESPONSIVE:
            pull.linebreak()
            pull.gthen(
                f"Guessing Signatures for unresponsive DNS Servers",
                pull.BOLD,
                pull.DARKCYAN
            )

            for record in self.__NOT_RESPONSIVE:
                self.check_signature(record)

            if not self.__GUESSED_SIGNATURES:
                pull.gthen(
                    f"No signatures were matched for the records. Try searching them on Internet",
                    pull.BOLD,
                    pull.YELLOW
                )
                pull.linebreak()
                return

            pull.gthen(
                "Signatures Matched. Following are the possible DNS Providers",
                pull.BOLD,
                pull.GREEN
            )
            pull.linebreak()

            for signature in self.__GUESSED_SIGNATURES:
                pull.slasher(
                    f"{signature} => {self.__SIGNATURES[signature]['status']}",
                    pull.BOLD,
                    pull.YELLOW
                )
            
            pull.linebreak()