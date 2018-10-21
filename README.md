# Subrake
A powerful low-level socket scanner for enumerating subdomains, HTTP/HTTPS codes and CNAME records. 2.x to 3.x times faster.

## Description
Subrake is a powerful tool for enumerating subdomains, HTTP and HTTPS return codes, possible servers returned via headers and
CNAME records. The connection required parts of the script are implemented in low-level sockets which make it 2.x to 3.x times faster
than other commonly used tools.  On initial start, it would locate the name servers of the target domain and then enumerate
subdomains according to a given list. For the purpose, two lists are currently provided, named `small` and `large` and directly be
specified by the names with `-w, --wordlist` option. It is still in beta version and various errors are to be expected. 

## Syntax
Running Your First scan. Clone into the repository and launch the script: 
```
$ git clone https://github.com/hash3liZer/Subrake.git
$ cd Subrake/
$ python subrake.py -d [target.com] -w [small/large] [...options]
```
## Options
```
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
```

## Examples
Here are some of common examples:
```
$ python subrake.py -d shellvoide.com -w small
$ python subrake.py -d google.com -w large -t 30
$ python subrake.py -d starbucks.com -w large -t 30 -o /output.txt
```

## Support
EMAIL: admin@shellvoide.com <br />
Website: https://www.shellvoide.com <br />
Twitter: @hash3liZer <br />
