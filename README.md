<h1 align="center"> 
    <img src="https://user-images.githubusercontent.com/29171692/57197739-5392b300-6f84-11e9-9191-4e38f3edc583.png" alt="subrake" /> <br>    
    SUBRAKE
</h1>
<h4 align="center"> A Powerful Subdomain Enumeration Tool for Reconnaissance. </h4>
<p align="center">
    <a href="https://www.gnu.org/licenses/gpl-3.0" target="_blank"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="lisence" /></a>
</p>

[![asciicast](https://asciinema.org/a/ccHuIkpEjVIVwpxIqkVASGW0N.svg)](https://asciinema.org/a/ccHuIkpEjVIVwpxIqkVASGW0N)

## Description
A Powerful Subdomain Scanner & Validator Written in sockets which makes it a lot more faster and easier to manage. It works by enumerating subdomains by searching them on web and by using local wordlists. It further identify the assets of a domain based on their ip and `CNAME` records and identify subdomains which are using the same IP addresses. It also scan ports if are given and enumerte possible server engines used on assets using the `SERVER` header returned in the response. It also enumerates possible returned HTTP status codes on port 80 and 443. 

## Key Features
<ul>
    <li> Use built-in low level sockets to connect subdomains and other assets </li>
    <li> Search Subdomains Online on the Web. </li>
    <li> Validate Subdomains Using associated IP address. </li>
    <li> Identify False Positives. </li>
    <li> Internal Filtering using <b>--filter</b> option </li>
    <li> Store data in plain text and CSV formats. </li>
    <li> Built-in Port Scanning </li>
</ul>

## Installation
Subrake is totally based on internal python libraries except for `dnspyhon` module which you will have to install through `pip` or your local package manager. 
```
$ pip install dnspython
```

You can take a start by cloning the source. 
```
$ git clone https://github.com/hash3liZer/Subrake.git
$ cd Subrake/
$ python subrake -d yourdomain.tld -w wordlists/small.lst
```

## Options
```
Syntax: 
    $ python subrake -d shellvoide.com -w [ Sublister Output ]
    $ python subrake -d shellvoide.com -d shellvoide.com --wordlist wordlist/small.lst --filter --csv output.csv

Options:
   Args               Description                      Default
   -h, --help           Show this manual                  NONE
   -d, --domain         Target domain. Possible
                        example: [example.com]            NONE
   -w, --wordlists      Wordlists containing subdomains
                        to test. Multiple wordlists can
                        be specified.                     NONE                      
   -t, --threads        Number of threads to spawn         25
   -o, --output         Store output in a seperate file   NONE
   -c, --csv            Store output in CSV format        NONE
   -p, --ports          Comma-seperated ports to scan.    NONE
                        Depends on --scan-ports. 
   -s, --search         Search for subdomains Online      FALSE
       --filter         Filter subdomains with same IP    FALSE
       --scan-ports     Turns on the port scanning 
                        feature                           FALSE
```

## Examples
Here are some of common examples:
```
$ python subrake.py -d shellvoide.com --wordlist wordlists/small.lst
$ python subrake.py -d google.com -t 30 -o output.txt -f --search -w myrandomlist.txt
$ python subrake.py -d starbucks.com -w wordlists/small.lst -t 30 -o output.txt --csv output.csv --scan-ports
```

## Contribution
You can contribute to the project in many ways:
<ul>
    <li> Report Bugs </li>
    <li> Fork the project and start building on your own. </li>
    <li> Suggestions for making it better </li>
</ul>

Have any further Question? You can hit me up on Twitter and Email: <br>
Email: admin@shellvoide.com <br>
Twitter: [@hash3liZer](https://twitter.com/hash3liZer)
