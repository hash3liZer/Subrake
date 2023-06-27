<h1 align="center">
    <img src="https://user-images.githubusercontent.com/29171692/57197739-5392b300-6f84-11e9-9191-4e38f3edc583.png" alt="subrake" /> <br>    
    Subrake
</h1>
<h4 align="center">A Subdomain Enumeration & Takeover toolkit for Bug Bounty and Infosec.</h4>
<p align="center">
    <a href="https://github.com/hash3liZer/Subrake/actions"><img src="https://github.com/hash3liZer/subrake/actions/workflows/demo.yml/badge.svg" alt="..."></a>
    <a href="https://www.linux.org/" target="_blank"><img src="https://img.shields.io/badge/platform-linux-important" alt="platform: linux" /></a>
    <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-3-yellow.svg?logo=python" alt="Python: 3" /></a>
    <a href="https://www.gnu.org/licenses/gpl-3.0" target="_blank"><img src="https://img.shields.io/badge/License-GPLv3-blue.svg" alt="lisence" /></a>
</p>

<!--<img align="center" src="https://github.com/hash3liZer/Subrake/assets/29171692/956c0174-b8ee-4817-ac56-370bb517c991" alt="subrake" /><hr>
<img align="center" src="https://github.com/hash3liZer/Subrake/assets/29171692/41790ef9-3a46-48de-9d34-2728242716fd" alt="subrake" />-->

<img align="center" src="https://user-images.githubusercontent.com/29171692/206875533-0ac3ca1c-e183-4c4a-9bb2-b7206d1cfc50.png" alt="subrake" />
<img align="center" src="https://user-images.githubusercontent.com/29171692/206875554-1f09c82a-d82d-4285-b30f-d84c67d99a9d.png" alt="subrake" />

# Background 📈
A subdomain takeover unlike it sounds is basically the acquisition of the service that the subdomain is pointing to. For example taking over an Amazon S3 Bucket that `marketing.target.com` was point to a while ago. Since, the subdomain was pointing to the service which is now owned by me aka the attacker in this scenario, we can say that i've taken over the subdomain now. 

```bash
marketing.vulnerable.com -> AMAZON S3 Bucket
hr.vulnerable.com -> Elastic Beanstalk
```

# About Subrake 💰
Subrake, initially designed for subdomain gathering using public sources and brute forcing through wordlists is a toolkit for subdomain gathering and takeover assessment.

Designed primarily for bug bounty and infosec industry, it can be leveraged for blue teaming and internal pentests as well. It supports both a CLI and Web Based GUI Interface as well and supports multiple installation modes. We will cover the key features a little later after the Installation step. 

# Features ⚖️
* ⚙️ All in one automated solution. Its working cycle is:
    * 🪙 DNS Enumeration
    * 💴 False Positive Detection (Wildcard subdomains)
    * 💶 Getting results from other tools (Sublist3r, Knock.py)
    * 💷 Bruteforce using wordlists (Can work with multiple wordlists)
    * 💵 Get 5 parameters for each subdomain (HTTP Codes, Resolution, Headers, CNAME, Ports)
    * 💰 **Detect Takeover**
* 🛒 Support for external tools. You can add your own functions.
* 🛍️ Automated and Manual Mode.
* 🗄️ Can run concurrent sessions.
* 🖼️ UI for Reports and results available in `csv` format.
* 🛎️ Flexible and Fast. 

# Installation
You can setup subrake by an automated mode or by manually cloning the repo and install through `setuptools`. The first provides more control and is flexible with a UI. But if you prefer a simple CLI mode or on `windows`, go through the `manual` section. 

Clone the repo and jump into it: 
```bash
$ git clone https://github.com/hash3liZer/Subrake.git
$ cd ./Subrake
```

## Automated Setup:
You can setup `subrake` through vagrant (with KVM) where a machine will be spawned and everything will be automatically setup. Install the requirements first: 
```python
$ apt update
$ apt install -y qemu qemu-kvm libvirt-daemon libvirt-clients bridge-utils virt-manager vagrant vagrant-libvirt
```

Then inside the repo, run `vagrant` up:
```python
$ vagrant up
```

This will take a while to provision the server. After done, you will receive the URL: `http://127.0.0.1:9090`

<img width="1162" alt="image" src="https://github.com/hash3liZer/Subrake/assets/29171692/a03f9b61-6842-49b2-8015-202c20d6104f">

The default credentials are: `subrake/password`. You can change them during provisioning as well: 
```python
$ SUBRAKE_USERNAME="username" SUBRAKE_PASSWORD="password" vagrant up
```

After done, you can manage the state of your newly created machine through these commands: 
```python
# See the machine status
$ vagrant status

# Suspend the machine
$ vagrant suspend

# Resume machine
$ vagrant resume

# Shutdown machine
$ vagrant halt

# Start back
$ vagrant up

# Delete the machine
$ vagrant destroy
```

## Manual Setup
With the manual setup, you can directly jump into directory and the `setuptools` for installation

Install the requirements and run `setup.py`:
```bash
$ pip3 install -r requirements.txt
$ python3 setup.py install
```

Verify if subrake is installed or not: 
```bash
subrake --help
```

## Docker
You can also build the docker image from `Dockerfile`:
```bash
$ docker build -t subrake:latest .
```

Verify the docker container:
```bash
$ docker run --rm subrake --help
```

# Deployment
You can deploy the script on a baremetal server as well. To do so, get a fresh `ubuntu 20.04` server up and running and run the following command:
```python
$ chmod +x ./installer.sh
$ ./installer.sh --deploy
```

The server is then accessible at: `0.0.0.0:9090`. You can setup an `nginx` service and use it s a reverse proxy. 

# Usage
## User Interface
With the UI, you can directly jump to the `Subtap a Domain` page and run a scan. Expect a couple questions for the scan: 

<img width="1198" alt="image" src="https://github.com/hash3liZer/Subrake/assets/29171692/ebf2a0b7-b02e-425a-8dbf-922d68ca886c">

The scan is launched inside a `tmux` session. You can press `CTRL+E => d` to exit the running screen and launch a new scan. Also, to pause the screen and move up and down, you can press `CTRL+E => [`. Its just TMUX shortcuts with the global bind key changed to `CTRL+E`.  

You can also jump back to a running screen by entering its name again: 

<img width="1198" alt="image" src="https://github.com/hash3liZer/Subrake/assets/29171692/a48e3fa3-08fe-4f7a-86df-c73418b4dbe2">

### Reports

<img width="1240" alt="image" src="https://github.com/hash3liZer/Subrake/assets/29171692/03f90a82-54a9-4e5c-857b-128665f11756">

### Scan Results

<img width="1240" alt="image" src="https://github.com/hash3liZer/Subrake/assets/29171692/b1344469-85c5-406e-8152-176b45cdfc41">

## Command line
On command line, you an directly access the tool by typing `subrake`. Here are a couple example of using subrake: 

A simple run with default options:
```python
$ subrake -d google.com
```

Subrake with Multiple Threads:
```python
$ subtake -d google.com -t 50
```

Subrake with modules and a wordlist:
```python
$ subrake -d google.com --wordlists SecLists/Discovery/DNS/namelist.txt
```

Subrake with OSINT results + Multiple SecLists subdomains list: 

**Note: Subdomains with similar names will automatically be filtered and counted as 1**

```python
$ subrake -d google.com --wordlists SecLists/Discovery/DNS/namelist.txt,SecLists/Discovery/DNS/dns-Jhaddix.txt
```

Subrake without search engine + Output from multiple tools combined + IP Filtering (Note that you can integrate your tools into subrake):
```python
$ domain="google.com"
$ subfinder -d $domain -nW -o $domain/1.txt && sublist3r -d $domain -o $domain/2.txt && cat $domain/* >> /tmp/output.txt
$ subrake -d $domain -w tmp/output.txt --filter --skip-search
```

Subrake with Port Scanning: <br>
**NOTE: The port 80,443 will be scanned by default for every host under HTTP/HTTPS banner. So, there's no need to specify them here**
```python
$ subrake -d google.com --ports 8080,8443,8000,23,445
```

## Manual
<img width="899" alt="image" src="https://github.com/hash3liZer/Subrake/assets/29171692/a34c6783-b5ef-4fdc-ba63-d6cabdb02d73">

# ToDo LIST
Feel free to open pull requests and a feature. You can contribute by:

- [ ] Add more vulnerable services. Currently 10
- [ ] Improve Insatllation script.
- [x] Add GUI Mode
- [x] Add Docker support. 

## Get me at
* Email: <a href="mailto:me@shameerkashif.me">me@shameerkashif.me</a>
* Discord: <a href="#">hash3liZer#5786</a>
* Blog: <a href="https://blog.shameerkashif.me">https://blog.shameerkashif.me</a>
