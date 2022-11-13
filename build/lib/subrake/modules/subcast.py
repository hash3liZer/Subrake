from subrake.pull import PULLY
import tempfile
import subprocess
import time
import os

pull = PULLY()

class SUBCAST:

    def __init__(self, prs):
        self.domain = prs.domain

    def exec_amass(self):
        def check():
            cc = subprocess.call("amass -help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if not cc: return True
            return False

        if not check(): pull.lthen("Amass not located on the machine. Skipping AMASS", pull.BOLD, pull.RED)
        _path = os.path.join(tempfile.gettempdir(), "amass.subs")
        _comm = f"xterm -title amass -e 'amass enum -d {self.domain} -o {_path}'"
        exec  = subprocess.Popen(_comm, shell=True)
        pull.gthen(f"Launched AMASS: {_comm}", pull.BOLD, pull.GREEN)

        return (
            'amass',
            exec,
            _path
        )

    def exec_sublister(self):
        def check():
            cc = subprocess.call("sublist3r.py --help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if not cc: return True
            return False

        if not check(): pull.lthen("Sublist3r not located on the machine. Skipping Sublist3r", pull.BOLD, pull.RED)
        _path = os.path.join(tempfile.gettempdir(), "sublister.subs")
        _comm = f"xterm -title sublister -e 'sublist3r.py -d {self.domain} -o {_path} --verbose'"
        exec  = subprocess.Popen(_comm, shell=True)
        pull.gthen(f"Launched Sublist3r: {_comm}", pull.BOLD, pull.GREEN)

        return (
            'sublister',
            exec,
            _path
        )

    def engage(self):
        if not pull.is_linux():
            pull.lthen("Skipping SUBCAST as the underlying operating system is not Linux!", pull.BOLD, pull.RED)
            return

        if not pull.is_xterm():
            pull.lthen("Skipping SUBCAST as the package xterm is not installed!", pull.BOLD, pull.RED)
            return

        _list = [
            self.exec_amass,
            self.exec_sublister
        ]

        print(_list)

        _data = []
        for func in _list:
            (name, caller, subs) = func()
            _data.append({
                'name': name,
                'caller': caller,
                'subs'  : subs
            })

        pull.gthen("Waiting for all the subcasters to finish ...", pull.BOLD, pull.YELLOW)
        calls = 0
        talls = []
        while calls != len(_data):
            for client in _data:
                if client['caller'].poll() == 0 and client['name'] not in talls:
                    pull.gthen(f"The caster {client['name']} has finished gathering the subdomains", pull.BOLD, pull.GREEN)
                    calls += 1
                    talls.append(client['name'])

            time.sleep(1)

        rtval = []
        for client in _data:
            with open(client['subs']) as fl:
                rtval += fl.read().splitlines()

        rtval = list(set(rtval))
        pull.gthen(f"Gathered a total of {len(rtval)} unique subdomains from subcaster", pull.BOLD, pull.YELLOW)
        return rtval
