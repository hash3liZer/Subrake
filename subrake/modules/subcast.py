from subrake.pull import PULLY
import tempfile
import subprocess
import time
import json
import os
import shutil

pull = PULLY()

class SUBCAST:

    __RUN = []

    def __init__(self, prs):
        self.domain = prs.domain
        self.sessname = prs.domain.replace(".", "")
        self.onlysublister = prs.onlysublister

    def exec_amass(self):  # sourcery skip: avoid-builtin-shadow
        def check():
            cc = subprocess.call("/snap/bin/amass -help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return not cc
        
        if not check(): pull.lthen("Amass not located on the machine. Skipping AMASS", pull.BOLD, pull.RED); return
        _path = os.path.join(tempfile.gettempdir(), "amass.subs")
        _subc = f"/snap/bin/amass enum -v -d {self.domain} -o {_path}"
        _comm = f"tmux split-window -h -t {self.sessname}:0 '{_subc}'"
        exec  = subprocess.Popen(_comm, shell=True)
        pull.gthen(f"Launched AMASS: {_subc}", pull.BOLD, pull.GREEN)

        return (
            'amass',
            f'{self.sessname}:0.1',
            _path
        )

    def exec_sublister(self):  # sourcery skip: avoid-builtin-shadow
        def check():
            cc = subprocess.call("sublist3r.py --help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return not cc

        if not check(): pull.lthen("Sublist3r not located on the machine. Skipping Sublist3r", pull.BOLD, pull.RED); return
        _path = os.path.join(tempfile.gettempdir(), "sublister.subs")
        _subc = f"sublist3r.py -d {self.domain} -o {_path} --verbose"
        _comm = f"tmux split-window -t {self.sessname}:0.1 '{_subc}'"
        exec  = subprocess.Popen(_comm, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        pull.gthen(f"Launched Sublist3r: {_subc}", pull.BOLD, pull.GREEN)

        return (
            'sublister',
            f'{self.sessname}:0.2',
            _path
        )

    def exec_knockpy(self):  # sourcery skip: avoid-builtin-shadow
        def check():
            cc = subprocess.call("knockpy.py --help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return not cc

        if not check(): pull.lthen("Knockpy not located on the machine. Skipping KNOCKpy", pull.BOLD, pull.RED); return
        _path = os.path.join(tempfile.gettempdir())
        _subc = f"knockpy.py {self.domain} --no-http -o {_path}"
        _comm = f"tmux split-window -t {self.sessname}.0.1 '{_subc}'"
        exec  = subprocess.Popen(_comm, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        pull.gthen(f"Launched Knockpy: {_subc}", pull.BOLD, pull.GREEN)

        return (
            'knockpy',
            f'{self.sessname}:0.3',
            _path
        )

    def engage(self):  # sourcery skip: low-code-quality
        if not pull.is_linux():
            pull.lthen("Skipping SUBCAST as the underlying operating system is not Linux!", pull.BOLD, pull.RED)
            return

        if not pull.is_xterm():
            pull.lthen("Skipping SUBCAST as the package xterm is not installed!", pull.BOLD, pull.RED)
            return

        _list = (
            [self.exec_sublister]
            if self.onlysublister
            else [self.exec_amass, self.exec_sublister, self.exec_knockpy]
        )

        self.__RUN = []
        _data = []
        for func in _list:
            if _func := func():
                (name, caller, subs) = _func
                if name not in self.__RUN:
                    self.__RUN.append(name)                    
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
                _fcall = subprocess.call(f"tmux capture-pane -t {client['caller']}", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                if _fcall and client['name'] not in talls:
                    pull.gthen(f"The caster {client['name']} has finished gathering the subdomains", pull.BOLD, pull.GREEN)
                    calls += 1
                    talls.append(client['name'])

            time.sleep(1)

        rtval = []
        for client in _data:
            if os.path.isfile(client['subs']):
                with open(client['subs']) as fl:
                    rtval += fl.read().splitlines()
                os.remove(client['subs'])
            elif os.path.isdir(client['subs']):
                if client['name'] == 'knockpy':
                    if gfile := next(
                        (
                            filename
                            for filename in os.listdir(client['subs'])
                            if filename.startswith(self.domain)
                            and filename.endswith(".json")
                        ),
                        None,
                    ):
                        data = json.loads(open(os.path.join(client['subs'], gfile)).read())
                        data = data.keys()
                        rtval += [ss for ss in data if ss != "_meta"]

                    shutil.rmtree(client['subs'])

        rtval = list(set(rtval))
        pull.gthen(f"Gathered a total of {len(rtval)} unique subdomains from subcaster", pull.BOLD, pull.YELLOW)
        return rtval
