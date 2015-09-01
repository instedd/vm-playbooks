# InSTEDD Ansible Playbooks

Install InSTEDD Platform applications in a target host.

## Status

This project is work in progress. See `TODO.md` for pending issues. The current goal is to be able to provision a Virtual Machine with InSTEDD applications to be run locally, starting with Pollit plus the required stack (Hub, Guisso and Nuntium).

All applications are run as docker containers. Services are exposed to the host using avahi and proxied via an nginx, and internal discovery is handled with dnsmasq.

## Run

To deploy the `main.yml` playbook on a Vagrant machine, run:

```bash
vagrant up
```

