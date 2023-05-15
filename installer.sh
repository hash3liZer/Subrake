#!/bin/bash

homedir=$(pwd)

if ! [ $(id -u) -eq 0 ]; then
    echo "[-] The installer script must be run as root"
    exit -1;
fi

# Check if underlying operating system ir ubuntu or not
if ! [[ "$(cat /etc/os-release | grep "^ID=" | cut -d= -f2)" == "ubuntu" ]]; then
    echo "[-] The installer script is only prepare for ubuntu operating systems"
    exit -1;
fi

cp ./utils/bashrunner.sh /usr/bin/bashrunner
chmod +x /usr/bin/bashrunner

source /etc/os-release

rm -rf /etc/apt/preferences.d/nosnap.pref
apt update
apt install -y xterm python3-dev python3 python3-pip snap unzip git screen tmux
apt install -y -t ${UBUNTU_CODENAME}-backports cockpit

ln -s /usr/bin/python3 /usr/bin/python 2>/dev/null

# Check if a directory doesn't exist
if ! [ -d "/opt/SecLists" ]; then
  wget "https://github.com/danielmiessler/SecLists/archive/refs/tags/2023.1.zip" -O /tmp/SecLists.zip
  unzip /tmp/SecLists.zip -d /opt/
  mv "/opt/SecLists-2023.1" /opt/SecLists
  chmod 777 -R /opt/SecLists
  rm -rf /tmp/SecLists.zip
fi

cd /opt/
git clone https://github.com/aboul3la/Sublist3r.git
cd Sublist3r
pip3 install -r requirements.txt
ln -s /opt/Sublist3r/sublist3r.py /usr/bin/sublist3r.py

cd /opt/
git clone https://github.com/guelfoweb/knock
cd knock
pip3 install -r requirements.txt
chmod +x knockpy.py
ln -s /opt/knock/knockpy.py /usr/bin/knockpy.py

snap install amass

cd "$homedir"
pip3 install -r ./requirements.txt
python3 ./setup.py install

mkdir -p /usr/share/subtakes
chmod 777 -R /usr/share/subtakes

echo "Add folowing entry to your .bashrc: "
echo ""
echo "bashrunner"
echo "exit"