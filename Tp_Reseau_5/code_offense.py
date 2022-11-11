#!/usr/bin/env python3

from scapy.all import ARP, Ether, srp

packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.1/24")

# a list of clients, we will fill this in the upcoming loop
clients = []

for sent, received in srp(packet, timeout=3, verbose=0)[0]:
    # for each response, append ip and mac address to `clients` list
    clients.append({'ip': received.psrc, 'mac': received.hwsrc})

# print clients
print("Available devices in the network:")
print("IP" + " "*18+"MAC")
for client in clients:
    print(client['ip'], client['mac'])