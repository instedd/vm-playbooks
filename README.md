# InSTEDD Ansible Playbooks

Install InSTEDD Platform applications in a target host.

## Status

This project is work in progress. See `TODO.md` for pending issues. The current goal is to be able to provision a Virtual Machine with InSTEDD applications to be run locally. The currently supported apps (as Docker containers) are:

- guisso
- hub
- nuntium
- verboice
- pollit
- theme
- ask

All applications are run as docker containers. Services are exposed to the host using avahi and proxied via an nginx, and internal discovery is handled with dnsmasq. MySQL and Asterisk are installed directly on the VM and not run as containers.

## Run

To setup and deploy the `main.yml` playbook on a Vagrant machine, run:
```bash
vagrant up
```

The playbook can be re-run on the machine by running:
```bash
ansible-playbook main.yml -i hosts -s
```
