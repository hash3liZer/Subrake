<h1 align="center">
    <img src="https://user-images.githubusercontent.com/29171692/57197739-5392b300-6f84-11e9-9191-4e38f3edc583.png" alt="subrake" /> <br>    
    SUBRAKE
</h1>
<h4 align="center">A Subdomain Enumeration and Validation tool for Bug Bounty and Pentesters.</h4>
<p align="center">
    <a href="https://www.linux.org/" target="_blank"><img src="https://img.shields.io/badge/platform-linux-important" alt="platform: linux" /></a>
    <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-3-yellow.svg?logo=python" alt="Python: 3" /></a>
    <a href="https://pypi.org/" target="_blank"><img src="https://img.shields.io/badge/PYPI-%40subrake-green.svg?logo=pypi" alt="PYPI: @subrake" /></a>
    <a href="https://github.com/hash3liZer/Subrake/releases" target="_blank"><img src="https://img.shields.io/badge/version-v3.3-blue.svg?logo=moo" alt="Release: v3.1" /></a>
    <a href="https://www.gnu.org/licenses/gpl-3.0" target="_blank"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="lisence" /></a>
</p>

<img align="center" src="https://user-images.githubusercontent.com/29171692/91291801-3609de00-e7b3-11ea-88f5-9f3dcceb451d.png" alt="subrake" />

## Key Features
<ul>
    <li>OSINT + Subdomain Bruteforcing</li>
    <li>Capable of handling outputs from multiple tools</li>
    <li>Handling False Positives and Filters subdomains with same resolutions.</li>
    <li>Checking for Server Banners and Ports</li>
    <li>Incredibly Fast</li>
    <li>Handling domains with larger scopes</li>
    <li>Port Scanning</li>
</ul>

## Documentation
### Installation
Installing stable version directly from PYPI:
```
$ pip3 install subrake
```

Installing latest build:
```
$ git clone https://github.com/hash3liZer/Subrake.git
$ cd Subrake/
$ python3 setup.py install
```

Run after installation:
```
$ subrake --help
```

### Usage
Subrake is highly flexible and is made to work under different situations. It can parse output files from multiple tools collectively. It does OSINT search alongside wordlist bruteforcing and before actual bruteforcing, it removes similar subdomains and false positives. It does also support a filter which when supplied allows you to seperate subdomains with same IP addresses in the final CSV result. Let's see some of the Subrake uses:

A simple run with OSINT results from search engines:
```
$ subrake -d google.com
```

Subrake with Multiple Threads:
```
$ subtake -d google.com -t 50
```

Subrake with OSINT results + SecLists subdomains list:
```
$ subrake -d google.com --wordlists SecLists/Discovery/DNS/namelist.txt
```

Subrake with OSINT results + Multiple SecLists subdomains list: <br>
**Note: Subdomains with similar names will automatically be filtered and counted as 1**
```
$ subrake -d google.com --wordlists SecLists/Discovery/DNS/namelist.txt,SecLists/Discovery/DNS/dns-Jhaddix.txt
```

Subrake without OSINT + Output from multiple tools combined + IP Filtering:
```
$ domain="google.com"
$ subfinder -d $domain -nW -o $domain/1.txt && sublist3r -d $domain -o $domain/2.txt && cat $domain/* >> /tmp/output.txt
$ subrake -d $domain -w tmp/output.txt --filter --skip-search
```

Subrake without DNS + OSINT:
```
$ subrake -d google.com --skip-dns
```

Subrake with Port Scanning: <br>
**NOTE: The port 80,443 will be scanned by default for every host under HTTP/HTTPS banner. So, there's no need to specify them here**
```
$ subrake -d google.com --ports 8080,8443,8000,23,445
```

### Manual

```
   Args               Description                                    Default
   -h, --help           Show this manual                             NONE
   -d, --domain         Target domain. Possible
                        example: [example.com]                       NONE
   -w, --wordlists      Wordlists containing subdomains
                        to test. Multiple wordlists can
                        be specified.                                NONE
   -t, --threads        Number of threads to spawn                    25
   -o, --output         Store final subdomains in a specified file   NONE
   -c, --csv            Store output results in CSV format           NONE
   -p, --ports          Comma-seperated list of ports to scan.       NONE
   -s, --skip-search    Search for subdomains Online from various
                        sites.                                       FALSE
       --filter         Filter subdomains with same IP in CSV output FALSE
                        Helpful with larger scopes.
       --skip-dns       Skip initial DNS enumeration phase           FALSE
       --exclude-ips    Exclude specified IPs from the final results
                        Helpful in removing False Positives          NONE
```

## Contribution
You can contribute to the project in many ways:
<ul>
    <li> Report Bugs </li>
    <li> Suggestions for making it better </li>
</ul>

Have any further Question? You can hit me up on Twitter and Email: <br>
Twitter: [@hash3liZer](https://twitter.com/hash3liZer)
