# Subrake
A powerful low-level subdomain scanner for reconnaissance purposes. It enumerates HTTP/HTTPS codes and CNAME records and is 2.x to 3.x times faster.

## Description
Subrake is a powerful tool for enumerating subdomains, HTTP and HTTPS return codes, possible servers returned via headers and
CNAME records. The connection required parts of the script are implemented in low-level sockets which make it 2.x to 3.x times faster
than other commonly used tools.  On initial start, it would locate the name servers of the target domain and then enumerate
subdomains according to a given list. You can provide a list using `--wordlist` option like you can provide output of sublister. You can also make it search for subdomains on internet using `--search` option.

## Syntax
Running Your First scan. Clone into the repository and launch the script: 
```
$ git clone https://github.com/hash3liZer/Subrake.git
$ cd Subrake/
$ python subrake.py -d [target.com] [...options]
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
$ python subrake.py -d shellvoide.com -w wordlist/small.lst
$ python subrake.py -d google.com --skip-wordlist -t 30 -o output -f simple,csv,status
$ python subrake.py -d starbucks.com -w wordlist/small.lst --skip-port -t 30 -o /output.txt -s subdomains.txt
```

## Support
EMAIL: admin@shellvoide.com <br />
Website: https://www.shellvoide.com <br />
Twitter: @hash3liZer <br />
