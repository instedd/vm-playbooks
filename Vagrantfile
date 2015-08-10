# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/trusty64"
  config.vm.hostname = "playbooks.local"
  config.vm.network :private_network, type: :dhcp

  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--memory", "2048"]
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "test.yml"
    ansible.sudo = true
    ansible.extra_vars = { ansible_ssh_user: 'vagrant' }
    ansible.host_key_checking = false
    ansible.verbose = ''
  end

end
