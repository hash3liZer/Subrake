#!/bin/bash

apt install -y xterm amass python3-dev python3 python3-pip

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

pip3 install -r ./requirements.txt