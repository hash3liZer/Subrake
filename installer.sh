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
cp ./utils/get_all_subs.sh /usr/bin/get_all_subs
cp ./utils/get_all_takeovers.sh /usr/bin/get_all_takeovers
cp ./utils/get_all_domains.sh /usr/bin/get_all_domains
cp ./utils/get_active_sessions.sh /usr/bin/get_active_sessions
cp ./utils/get_tables.sh /usr/bin/get_tables
chmod +x /usr/bin/bashrunner
chmod +x /usr/bin/get_all_subs
chmod +x /usr/bin/get_all_takeovers
chmod +x /usr/bin/get_all_domains
chmod +x /usr/bin/get_active_sessions
chmod +x /usr/bin/get_tables

source /etc/os-release

rm -rf /etc/apt/preferences.d/nosnap.pref
apt update
apt install -y xterm python3-dev python3 python3-pip snap unzip git screen tmux
apt install -y -t ${UBUNTU_CODENAME}-backports cockpit

ln -s /usr/bin/python3 /usr/bin/python 2>/dev/null

function add_user(){
  echo "\n\n\n\n\n"
  echo "[-] Setting up cockpit user ..."
  echo -n "[?] Enter username: "
  read cusername
  echo -n "[?] Enter password: "
  read -s cpassword

  getent passwd $cusername >/dev/null

  if [ $? -ne 0 ]; then
    adduser --gecos "" --disabled-password $cusername
    echo "$cusername:$cpassword" | chpasswd
  fi 
}

function setup_cockpit(){
  systemctl enable --now cockpit.socket
  mv /usr/share/cockpit/apps/manifest.json /usr/share/cockpit/apps/manifest.json.bak
  mv /usr/share/cockpit/networkmanager/manifest.json /usr/share/cockpit/networkmanager/manifest.json.bak
  mv /usr/share/cockpit/packagekit/manifest.json /usr/share/cockpit/packagekit/manual/manifest.json.bak
  mv /usr/share/cockpit/storaged/manifest.json /usr/share/cockpit/storaged/manifest.json.bak
  mv /usr/share/cockpit/users/manifest.json /usr/share/cockpit/users/manifest.json.bak
  mv ./plugins/subruns /usr/share/cockpit/

  mkdir -p /usr/share/subtakes
  chmod 777 -R /usr/share/subtakes
  echo "Cockpit is installed and enabled on port 9090"
}

function setup_wordlists(){
  # Check if a directory doesn't exist
  if ! [ -d "/opt/SecLists" ]; then
    wget "https://github.com/danielmiessler/SecLists/archive/refs/tags/2023.1.zip" -O /tmp/SecLists.zip
    unzip /tmp/SecLists.zip -d /opt/
    mv "/opt/SecLists-2023.1" /opt/SecLists
    chmod 777 -R /opt/SecLists
    rm -rf /tmp/SecLists.zip
  fi
}

function setup_plugins(){
  cd /opt/
  git clone https://github.com/aboul3la/Sublist3r.git
  cd Sublist3r
  pip3 install -r requirements.txt
  ln -s /opt/Sublist3r/sublist3r.py /usr/bin/sublist3r.py

  # cd /opt/
  # git clone https://github.com/guelfoweb/knock
  # cd knock
  # pip3 install -r requirements.txt
  # chmod +x knockpy.py
  # ln -s /opt/knock/knockpy.py /usr/bin/knockpy.py

  # snap install amass
}

function final_setup(){
  cd "$homedir"
  pip3 install -r ./requirements.txt
  python3 ./setup.py install
}

add_user
setup_cockpit
setup_wordlists
setup_plugins
final_setup

echo "Add folowing entry to your .bashrc: "
echo ""
echo "bashrunner"
echo "exit"