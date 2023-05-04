#!/bin/bash

sudo rm /etc/apt/preferences.d/nosnap.pref
apt update
apt install -y xterm python3-dev python3 python3-pip snap

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

pip3 install -r ./requirements.txt