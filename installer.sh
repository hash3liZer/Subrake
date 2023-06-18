#!/bin/bash

homedir=$(pwd)

function init(){
  if ! [ $(id -u) -eq 0 ]; then
      echo "[-] The installer script must be run as root"
      exit -1;
  fi

  # Check if underlying operating system ir ubuntu or not
  if ! [[ "$(cat /etc/os-release | grep "^ID=" | cut -d= -f2)" == "ubuntu" ]]; then
      echo "[-] The installer script is only prepared for ubuntu operating systems"
      exit -1;
  fi
}

function install_dependencies(){
  source /etc/os-release
  rm -rf /etc/apt/preferences.d/nosnap.pref
  apt update
  apt install -y xterm python3-dev python3 python3-pip snap unzip git screen tmux wget
  apt install -y systemd libpam-systemd
  apt install -y -t ${UBUNTU_CODENAME}-backports cockpit
  ln -s /usr/bin/python3 /usr/bin/python 2>/dev/null
}

function copy_scripts(){
  cp ./utils/bashrunner.sh /usr/bin/bashrunner
  cp ./utils/get_all_subs.sh /usr/bin/get_all_subs
  cp ./utils/get_all_takeovers.sh /usr/bin/get_all_takeovers
  cp ./utils/get_all_domains.sh /usr/bin/get_all_domains
  cp ./utils/get_active_sessions.sh /usr/bin/get_active_sessions
  cp ./utils/get_tables.sh /usr/bin/get_tables
  cp ./utils/tmux.conf /opt/.tmux.conf
  chmod +x /usr/bin/bashrunner
  chmod +x /usr/bin/get_all_subs
  chmod +x /usr/bin/get_all_takeovers
  chmod +x /usr/bin/get_all_domains
  chmod +x /usr/bin/get_active_sessions
  chmod +x /usr/bin/get_tables
  chmod -wx /opt/.tmux.conf
  chmod +r /opt/.tmux.conf
}

# check if an environment variable is set
function check_env(){
  if [ -z "${!1}" ]; then
    echo "[-] $1 environment variable is not set"
    exit -1
  fi
}

function add_user(){
  echo -e "\n"
  echo "[-] Setting up cockpit user ..."
  echo -n "[?] Enter username: "
  if [ -z "$CUSERNAME" ]; then
    read cusername
    CUSERNAME=$cusername
  else
    echo $CUSERNAME
    cusername=$CUSERNAME
  fi

  echo -n "[?] Enter password: "
  if [ -z "$CPASSWORD" ]; then
    read cpassword
    CPASSWORD=$cpassword
  else
    echo $CPASSWORD
    cpassword=$CPASSWORD
  fi

  getent passwd $cusername >/dev/null

  if [ $? -ne 0 ]; then
    adduser --gecos "" --disabled-password $cusername
  fi 

  echo "$cusername:$cpassword" | chpasswd
}

function setup_cockpit(){
  systemctl enable --now cockpit.socket
  mv /usr/share/cockpit/apps/manifest.json /usr/share/cockpit/apps/manifest.json.bak
  mv /usr/share/cockpit/networkmanager/manifest.json /usr/share/cockpit/networkmanager/manifest.json.bak
  mv /usr/share/cockpit/packagekit/manifest.json /usr/share/cockpit/packagekit/manifest.json.bak
  mv /usr/share/cockpit/storaged/manifest.json /usr/share/cockpit/storaged/manifest.json.bak
  mv /usr/share/cockpit/users/manifest.json /usr/share/cockpit/users/manifest.json.bak

  # Copy systemd module
  cp ./plugins/systemd/manifest.json /usr/share/cockpit/systemd/

  # Copy subrun module
  cp -r ./plugins/subruns /usr/share/cockpit/

  # Copy static files
  cp ./plugins/static/* /usr/share/cockpit/static/

  # Copy Branding images
  cp ./plugins/branding/logo.png /usr/share/cockpit/branding/ubuntu/
  cp ./plugins/branding/logo.png /usr/share/cockpit/branding/debian/

  mkdir -p /usr/share/cockpit/static/subtakes
  chmod 777 -R /usr/share/cockpit/static/subtakes
  echo "Cockpit is installed and enabled on port 9090"
}

function setup_wordlists(){
  # Check if a directory doesn't exist
  if ! [ -d "/opt/subrake_wordlists" ]; then
    mkdir /opt/subrake_wordlists
    cp ./wordlists/* /opt/subrake_wordlists/
  fi
}

function setup_plugins(){
  cd /opt/
  git clone https://github.com/aboul3la/Sublist3r.git
  cd Sublist3r
  pip3 install -r requirements.txt
  rm -rf /usr/bin/sublist3r.py
  ln -s /opt/Sublist3r/sublist3r.py /usr/bin/sublist3r.py

  cd /opt/
  git clone https://github.com/guelfoweb/knock
  cd knock
  pip3 install -r requirements.txt
  chmod +x knockpy.py
  rm -rf /usr/bin/knockpy.py
  ln -s /opt/knock/knockpy.py /usr/bin/knockpy.py

  # snap install amass
}

function final_setup(){
  cd "$homedir"
  pip3 install -r ./requirements.txt
  python3 ./setup.py install
}

# Add 2 arguments of --install and --deploy
if [ "$1" == "" ]; then
  echo "[-] The script accepts either --install or --deploy arguments"
  echo "[-] The --deploy option is only tested on ubuntu>=20.04. Use it wisely"
  exit -1
fi

if [ "$1" == "--install" ]; then
  apt update
  apt install -y xterm python3-dev python3 python3-pip
  setup_plugins
  final_setup
  echo "[+] Installation completed successfully"
  exit 0
elif [ "$1" == "--deploy" ]; then
  init
  install_dependencies
  copy_scripts
  add_user
  setup_cockpit
  setup_wordlists
  setup_plugins
  final_setup

  grep -qxF 'bashrunner' /home/$CUSERNAME/.bashrc || echo 'bashrunner' >> /home/$CUSERNAME/.bashrc
  echo "[+] Deployment completed successfully"
  exit 0
elif [ "$1" == "--plugins" ]; then
  setup_plugins
  exit 0
fi