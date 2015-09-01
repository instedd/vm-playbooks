#! /usr/bin/python

import netifaces
import netaddr
import os
import re
import textwrap

class Colours:
  GRAY = '\033[37m'
  RED  = '\033[31m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'

class Network:

  ETC_NETWORK_INTERFACES = "/etc/network/interfaces"
  ETC_RESOLV_CONF = "/etc/resolv.conf"
  INTERFACE_NAME = 'eth1'

  def __init__(self):
    with open(Network.ETC_NETWORK_INTERFACES, "r") as f:
      self.interfaces = f.read()
    with open(Network.ETC_RESOLV_CONF, "r") as f:
      self.resolv = f.read()

  def ip(self):
    return netifaces.ifaddresses(Network.INTERFACE_NAME)[2][0]['addr']

  def mask(self):
    return netifaces.ifaddresses(Network.INTERFACE_NAME)[2][0]['netmask']

  def gateway(self):
    return netifaces.gateways()['default'][2][0]

  def dnss(self):
    return re.findall(r'(?m)^\s*nameserver\s*(.+?)\s*$', self.resolv)

  def searches(self):
    return re.findall(r'(?m)^\s*search\s*(.+?)\s*$', self.resolv)

  def method(self):
    try:
      return re.search(r'iface {}[^\n]*?(dhcp|static)'.format(Network.INTERFACE_NAME), self.interfaces).group(1)
    except:
      return None

  def free(self, ip):
    response = os.system("ping -c 1 -t 3 {} > /dev/null".format(ip))
    return response != 0

  def valid(self, ip):
    try:
      netaddr.IPAddress(ip)
    except:
      return False
    else:
      return True

  def in_network(self, ip):
    net = netaddr.IPNetwork("{}/{}".format(self.ip(), self.mask()))
    return netaddr.IPAddress(ip) in net

  def set_static(self, ip):
    config = textwrap.dedent("""\
      iface {} inet static
        address {}
        netmask {}""").format(Network.INTERFACE_NAME, ip, self.mask(), self.gateway())

    config = '\n'.join([config,
      "  dns-nameservers {}".format(' '.join(self.dnss())),
      "  dns-search {}".format(' '.join(self.searches()))])

    interfaces = re.sub(r'(?s)iface {} .*'.format(Network.INTERFACE_NAME), config, self.interfaces)
    with open(Network.ETC_NETWORK_INTERFACES, "w") as f:
      f.write(interfaces)

    print
    print "Contents of new interfaces configuration file", Colours.GRAY
    print interfaces
    print Colours.ENDC

    self.restart_interface()
    self.test_interface(ip)

  def test_interface(self, ip):
    current_ip = self.ip()
    if str(current_ip) == str(ip):
      print "IP", str(Colours.BOLD) + str(ip) + str(Colours.ENDC), "is now the new static address."
    else:
      print Colours.RED + Colours.BOLD + "Error starting interface {} with IP {}.\nCurrent IP is {}.".format(Network.INTERFACE_NAME, ip, current_ip) + Colours.ENDC + Colours.ENDC

  def suggest_ip(self):
    net = netaddr.IPNetwork("{}/{}".format(self.ip(), self.mask()))
    for ip in reversed(list(net[:-5])):
      if self.free(ip):
        return ip

  def restart_interface(self):
    print
    print "Restarting network interface...", Colours.GRAY
    os.system("sudo ifdown {0}".format(Network.INTERFACE_NAME))
    os.system("sudo ifup   {0}".format(Network.INTERFACE_NAME))
    os.system("sudo ifdown {0}".format(Network.INTERFACE_NAME))
    os.system("sudo ifup   {0}".format(Network.INTERFACE_NAME))
    print Colours.ENDC


def menu_static_ip(network):
  print
  while True:
    ip = raw_input("Enter an IP address or leave blank to cancel: ")
    if ip.strip() == "":
      print "No changes will be applied."
      break
    elif not network.valid(ip):
      print "That IP is not valid."
    elif not network.in_network(ip):
      print "That IP is not within the current network."
    elif not network.free(ip):
      choice = raw_input("That IP is currently in use. Are you sure you want to use it? [y/N] ")
      if len(choice) > 0 and choice.strip().lower()[0] == 'y':
        network.set_static(ip)
        break
    else:
      network.set_static(ip)
      break


def main():
  network = Network()
  print
  print Colours.BOLD + "This tool will guide you through the Virtual Machine network configuration\n" + Colours.ENDC
  print "Your current IP address is {} and its config method is {}.".format(network.ip(), network.method().upper())

  if network.method().lower() == 'dhcp':
    print "DHCP method is not recommended, as your IP address may change over time."
    choice = raw_input("Do you want to set a static IP address? [y/N] ")
    if len(choice) > 0 and choice.strip().lower()[0] == 'y':
      menu_static_ip(network)
    else:
      print
      print "IP method will remain DHCP."
      print "Remember to update the IP in your Local Gateway every day if it changes!"
  else:
    choice = raw_input("Do you want to change your static IP? [y/N] ")
    if len(choice) > 0 and choice.strip().lower()[0] == 'y':
      menu_static_ip(network)
    else:
      print "No changes will be applied."
  print


if __name__ == "__main__":
  main()
