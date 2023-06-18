# -*- mode: ruby -*-
# vi: set ft=ruby :

cusername = ENV['SUBRAKE_USERNAME'] || 'subrake'
cpassword = ENV['SUBRAKE_PASSWORD'] || 'password'

# https://docs.vagrantup.com.
Vagrant.configure("2") do |config|

  config.vm.box = "generic/ubuntu2004"    # boxes at https://vagrantcloud.com/search
  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  config.vm.box_check_update = false
  
  config.vm.define "subrake" do |subrake| # Give the VM a name
    # Port Forwarding. Format is [host_port, guest_port]. List host_ip for public access
    subrake.vm.network "forwarded_port", guest: 9090, host: 9090, host_ip: "127.0.0.1"
    
    # For private network. More like NAT in VirtualBox
    subrake.vm.network "private_network", ip: "10.1.2.3"
    subrake.vm.network "public_network", auto_config: false

    # For bridged network. More like bridged in VirtualBox
    # subrake.vm.network "public_network"

    # For mounting folders. Format is [host_path, guest_path]
    subrake.vm.synced_folder ".", "/subraked", type: "nfs", mount_options: ["vers=3,tcp"]
  end

  # Provider-specific configuration so you can fine-tune various
  # We are using libvirt
  config.vm.provider :libvirt do |vm|
    vm.cpus = 2
    vm.memory = 1024
    vm.nested = false
    vm.machine_virtual_size = 10
  end

  # There are additional providers available like ansible or puppet. Please see the documentation
  config.vm.provision "shell", env: {"CUSERNAME"=>cusername, "CPASSWORD"=>cpassword}, inline: <<-SHELL
    cd /subraked/
    ls -al
    chmod +x ./installer.sh
    ./installer.sh --deploy
    echo ""
    echo ""
    echo "[+] You can now access Subrake Portal at: http://127.0.0.1:9090"
    echo "[+] Default username: $CUSERNAME"
    echo "[+] Default password: $CPASSWORD"
  SHELL
end
