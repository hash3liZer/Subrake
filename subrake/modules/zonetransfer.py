from subrake.pull import PULLY
import dns.query
import dns.zone
import socket

pull = PULLY()

class ZONETRANSFER:
    
    def __init__(self, domain, records):
        self.domain = domain
        self.records = records

    def filter(self):
        '''
            Filter out NS records from the list of DNS Records
        '''
        for record in self.records:
            if record[0] != "NS":
                self.records.remove(record)

    def check_transfer(self, record):
        try:
            hostname = socket.gethostbyname(record[:-1] if record.endswith(".") else record)
        except:
            return False

        try:
            print(self.domain)
            print(hostname)
            zone = dns.zone.from_xfr(dns.query.xfr(hostname, self.domain))
            if zone:
                pull.gthen(
                    "Zone transfer is enabled for the domain. Enumerating records => ",
                )
                pull.linebreak()
                for name, node in zone.nodes.items():
                    pull.slasher(
                        f"{name} - {node.rdtype} - {node.rddata}",
                    )
                pull.linebreak()
                return True

            else:
                return False
                
        except dns.exception.FormError:
            return False
            
        except dns.query.TransferError:
            return False

    def engage(self):
        self.filter()

        transfer = False
        for record in self.records:
            if transfer := self.check_transfer(record[1]):
                break

        if not transfer:
            pull.gthen("Zone transfer is not enabled for the domain.", pull.BOLD, pull.GREEN)
        
