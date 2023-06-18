import contextlib
from subrake.pull import PULLY
import subprocess
import time
import json
import os
import getpass

pull = PULLY()

class SUBCAST:

    __RUN = []

    def __init__(self, prs):
        self.domain = prs.domain
        self.sessname = prs.domain.replace(".", "")
        self.onlysublister = prs.onlysublister
        self.is_tmux  = self.is_tmux_func()

        if not os.path.isdir(os.path.join("/home/", getpass.getuser(), ".subrake", self.sessname)):
            os.makedirs(os.path.join("/home/", getpass.getuser(), ".subrake", self.sessname))

        self.dirpath = os.path.join("/home/", getpass.getuser(), ".subrake", self.sessname)

    def is_tmux_func(self):
        if not subprocess.call(f"tmux has-session -t {self.sessname}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
            return True
        return False

    def exec_sublister(self):  # sourcery skip: avoid-builtin-shadow
        def check():
            cc = subprocess.call("sublist3r.py --help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return not cc

        if not check(): pull.lthen("Sublist3r not located on the machine. Skipping Sublist3r", pull.BOLD, pull.RED); return
        _path = os.path.join(self.dirpath, "sublister.subs")
        _subc = f"sublist3r.py -d {self.domain} -o {_path} --verbose"
        _comm = f"tmux split-window -h -d -t {self.sessname}:0 '{_subc}'" if self.is_tmux else _subc
        pull.gthen(f"Launched Sublist3r: {_subc}", pull.BOLD, pull.GREEN)
        exec  = subprocess.call(_comm, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        while not subprocess.call(f"tmux capture-pane -t {self.sessname}:0.1", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE):
            time.sleep(1)
        pull.gthen(f"Caster Sublist3r Finished. Return Code: [{exec}]", pull.BOLD, pull.GREEN)     

        return (
            'sublister',
            f'{self.sessname}:0.1',
            _path
        )

    def exec_knockpy(self):  # sourcery skip: avoid-builtin-shadow
        def check():
            cc = subprocess.call("knockpy.py --help", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return not cc

        if not check(): pull.lthen("Knockpy not located on the machine. Skipping KNOCKpy", pull.BOLD, pull.RED); return
        _path = os.path.join(self.dirpath, "knockpy")
        _subc = f"knockpy.py {self.domain} --no-local -o {_path}"
        _comm = f"tmux split-window -h -d -t {self.sessname}:0 '{_subc}'" if self.is_tmux else _subc
        pull.gthen(f"Launched Knockpy: {_subc}", pull.BOLD, pull.GREEN)
        exec  = subprocess.call(_comm, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        while not subprocess.call(f"tmux capture-pane -t {self.sessname}:0.1", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE):
            time.sleep(1)
        pull.gthen(f"Caster Knockpy Finished. Return Code: [{exec}]", pull.BOLD, pull.GREEN)        

        return (
            'knockpy',
            f'{self.sessname}:0.3',
            _path
        )

    def engage(self):  # sourcery skip: low-code-quality
        if not pull.is_linux():
            pull.lthen("Skipping SUBCAST as the underlying operating system is not Linux!", pull.BOLD, pull.RED)
            return

        _list = (
            [self.exec_sublister]
            if self.onlysublister
            else [self.exec_sublister, self.exec_knockpy]
        )

        _data = []
        for func in _list:
            if _func := func():
                (name, caller, subs) = _func
                _data.append({
                    'name': name,
                    'caller': caller,
                    'subs'  : subs
                })

        # pull.gthen("Waiting for all the subcasters to finish ...", pull.BOLD, pull.YELLOW)
        # calls = 0
        # talls = []
        # while calls != len(_data):
        #     for client in _data:
        #         _fcall = subprocess.call(f"tmux capture-pane -t {client['caller']}", shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        #         if _fcall and client['name'] not in talls:
        #             pull.gthen(f"The caster {client['name']} has finished gathering the subdomains", pull.BOLD, pull.GREEN)
        #             calls += 1
        #             talls.append(client['name'])

        #     time.sleep(1)

        rtval = []
        for client in _data:
            if os.path.isfile(client['subs']):
                with open(client['subs']) as fl:
                    subs = fl.read().splitlines()
                    rtval += subs
                    pull.gthen(f"Gathered a total of {len(subs)} subdomains from {client['name']}", pull.BOLD, pull.YELLOW)
                # os.remove(client['subs'])
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
                        data = [ss for ss in data if ss != "_meta"]
                        pull.gthen(f"Gathered a total of {len(data)} subdomains from {client['name']}", pull.BOLD, pull.YELLOW)
                        rtval += data

                    # with contextlib.suppress(Exception):
                    #     shutil.rmtree(client['subs'])

        rtval = list(set(rtval))
        pull.gthen(f"Gathered a total of {len(rtval) or 1} unique subdomains from subcaster", pull.BOLD, pull.YELLOW)
        return rtval
