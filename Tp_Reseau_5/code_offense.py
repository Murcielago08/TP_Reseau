from scapy.all import ARP, Ether, srp

packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.1.1/24") # Crée les paquets

victimes = [] # tableau des appareils présents

for sent, received in srp(packet, timeout=3, verbose=0)[0]:
    victimes.append({'ip': received.psrc, 'mac': received.hwsrc})
# Ajoute les infos de chaque nouvel appareil trouvé dans le tableau

print("\n" + "Available devices in the network :" + "\n" + "IP" + " "*18 + "MAC")
for victime in victimes:
    print(victime['ip'])
    print(victime['mac'] + "\n")