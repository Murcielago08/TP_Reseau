# TP2 : Ethernet, IP, et ARP

Dans ce TP on va approfondir trois protocoles, qu'on a survolé jusqu'alors :

- **IPv4** *(Internet Protocol Version 4)* : gestion des adresses IP
  - on va aussi parler d'ICMP, de DHCP, bref de tous les potes d'IP quoi !
- **Ethernet** : gestion des adresses MAC
- **ARP** *(Address Resolution Protocol)* : permet de trouver l'adresse MAC de quelqu'un sur notre réseau dont on connaît l'adresse IP

![Seventh Day](./pics/tcpip.jpg)

# Sommaire

- [TP2 : Ethernet, IP, et ARP](#tp2--ethernet-ip-et-arp)
- [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
- [I. Setup IP](#i-setup-ip)
- [II. ARP my bro](#ii-arp-my-bro)
- [III. DHCP you too my brooo](#iii-dhcp-you-too-my-brooo)

# 0. Prérequis

**Il vous faudra deux machines**, vous êtes libres :

- toujours possible de se connecter à deux avec un câble
- sinon, votre PC + une VM ça fait le taf, c'est pareil
  - je peux aider sur le setup, comme d'hab

> Je conseille à tous les gens qui n'ont pas de port RJ45 de go PC + VM pour faire vous-mêmes les manips, mais on fait au plus simple hein.

---

**Toutes les manipulations devront être effectuées depuis la ligne de commande.** Donc normalement, plus de screens.

**Pour Wireshark, c'est pareil,** NO SCREENS. La marche à suivre :

- vous capturez le trafic que vous avez à capturer
- vous stoppez la capture (bouton carré rouge en haut à gauche)
- vous sélectionnez les paquets/trames intéressants (CTRL + clic)
- File > Export Specified Packets...
- dans le menu qui s'ouvre, cochez en bas "Selected packets only"
- sauvegardez, ça produit un fichier `.pcapng` (qu'on appelle communément "un ptit PCAP frer") que vous livrerez dans le dépôt git

**Si vous voyez le p'tit pote 🦈 c'est qu'il y a un PCAP à produire et à mettre dans votre dépôt git de rendu.**

# I. Setup IP

Le lab, il vous faut deux machines : 

- les deux machines doivent être connectées physiquement
- vous devez choisir vous-mêmes les IPs à attribuer sur les interfaces réseau, les contraintes :
  - IPs privées (évidemment n_n)
  - dans un réseau qui peut contenir au moins 1000 adresses IP (il faut donc choisir un masque adapté)
  - oui c'est random, on s'exerce c'est tout, p'tit jog en se levant c:
  - le masque choisi doit être le plus grand possible (le plus proche de 32 possible) afin que le réseau soit le plus petit possible

🌞 **Mettez en place une configuration réseau fonctionnelle entre les deux machines**

- vous renseignerez dans le compte rendu :
  - les deux IPs choisies, en précisant le masque
  - l'adresse de réseau
  - l'adresse de broadcast
- vous renseignerez aussi les commandes utilisées pour définir les adresses IP *via* la ligne de commande

```
adresse client :
C:\Windows\system32> netsh interface ipv4 set address name="Ethernet" static 192.168.26.51 255.255.252.0 192.168.26.50

adresse serveur :
C:\Windows\system32> netsh interface ipv4 set address name="Ethernet" static 192.168.26.50 255.255.252.0

C:\Windows\system32> ipconfig /all
Carte Ethernet Ethernet :

   Adresse IPv4. . . . . . . . . . . . . .: 192.168.26.50(préféré)
   Masque de sous-réseau. . . . . . . . . : 255.255.252.0
   Passerelle par défaut. . . . . . . . . :

adr : 192.168.24.0
adb : 192.168.27.255
```

> Rappel : tout doit être fait *via* la ligne de commandes. Faites-vous du bien, et utilisez Powershell plutôt que l'antique cmd sous Windows svp.

🌞 **Prouvez que la connexion est fonctionnelle entre les deux machines**

- un `ping` suffit !

```
C:\Windows\system32> ping 192.168.26.51

Envoi d’une requête 'Ping'  192.168.26.51 avec 32 octets de données :
Réponse de 192.168.26.51 : octets=32 temps=2 ms TTL=128
Réponse de 192.168.26.51 : octets=32 temps=2 ms TTL=128
Réponse de 192.168.26.51 : octets=32 temps=2 ms TTL=128
Réponse de 192.168.26.51 : octets=32 temps=2 ms TTL=128

Statistiques Ping pour 192.168.26.51:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
```

🌞 **Wireshark it**

- `ping` ça envoie des paquets de type ICMP (c'est pas de l'IP, c'est un de ses frères)
  - les paquets ICMP sont encapsulés dans des trames Ethernet, comme les paquets IP
  - il existe plusieurs types de paquets ICMP, qui servent à faire des trucs différents

[Ping-Pong Wireshark](./ping_tp2_reseau.pcapng)

- **déterminez, grâce à Wireshark, quel type de paquet ICMP est envoyé par `ping`**
  - pour le ping que vous envoyez
  - et le pong que vous recevez en retour
  - 
```
type du ping request : type 8 echo request
type du ping reply : type 0 echo reply 
```

🦈 **PCAP qui contient les paquets ICMP qui vous ont permis d'identifier les types ICMP**

# II. ARP my bro

ARP permet, pour rappel, de résoudre la situation suivante :

- pour communiquer avec quelqu'un dans un LAN, il **FAUT** connaître son adresse MAC
- on admet un PC1 et un PC2 dans le même LAN :
  - PC1 veut joindre PC2
  - PC1 et PC2 ont une IP correctement définie
  - PC1 a besoin de connaître la MAC de PC2 pour lui envoyer des messages
  - **dans cette situation, PC1 va utilise le protocole ARP pour connaître la MAC de PC2**
  - une fois que PC1 connaît la mac de PC2, il l'enregistre dans sa **table ARP**

🌞 **Check the ARP table**

- utilisez une commande pour afficher votre table ARP
- déterminez la MAC de votre binome depuis votre table ARP
```
C:\Users\darkj> arp -a

Interface : 192.168.26.50 --- 0x5
  Adresse Internet      Adresse physique      Type
  192.168.26.51         b4-45-06-a4-5c-76     dynamique
```

- déterminez la MAC de la *gateway* de votre réseau
  - celle de votre réseau physique, WiFi, genre YNOV, car il n'y en a pas dans votre ptit LAN
  - c'est juste pour vous faire manipuler un peu encore :)
```
C:\Users\darkj> arp -a
Interface : 10.33.16.168 --- 0xd
  Adresse Internet      Adresse physique      Type
  10.33.19.254          00-c0-e7-e0-04-4e     dynamique
```

🌞 **Manipuler la table ARP**

- utilisez une commande pour vider votre table ARP
- prouvez que ça fonctionne en l'affichant et en constatant les changements
```
C:\Windows\system32> arp -d
C:\Windows\system32> arp -a

Interface : 192.168.220.1 --- 0x3
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique

Interface : 192.168.26.50 --- 0x5
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique
  255.255.255.255       ff-ff-ff-ff-ff-ff     statique

Interface : 192.168.94.1 --- 0x6
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.2.60            01-00-5e-00-02-3c     statique

Interface : 10.33.16.168 --- 0xd
  Adresse Internet      Adresse physique      Type
  10.33.19.254          00-c0-e7-e0-04-4e     dynamique
  224.0.0.22            01-00-5e-00-00-16     statique
  255.255.255.255       ff-ff-ff-ff-ff-ff     statique
```
- ré-effectuez des pings, et constatez la ré-apparition des données dans la table ARP
```
C:\Windows\system32> arp -a

Interface : 192.168.26.50 --- 0x5
  Adresse Internet      Adresse physique      Type
  192.168.26.51         b4-45-06-a4-5c-76     dynamique
  224.0.0.22            01-00-5e-00-00-16     statique
  255.255.255.255       ff-ff-ff-ff-ff-ff     statique

Interface : 10.33.16.168 --- 0xd
  Adresse Internet      Adresse physique      Type
  10.33.19.254          00-c0-e7-e0-04-4e     dynamique
  224.0.0.22            01-00-5e-00-00-16     statique
  255.255.255.255       ff-ff-ff-ff-ff-ff     statique
```

🌞 **Wireshark it**

- vous savez maintenant comment forcer un échange ARP : il sufit de vider la table ARP et tenter de contacter quelqu'un, l'échange ARP se fait automatiquement
- mettez en évidence les deux trames ARP échangées lorsque vous essayez de contacter quelqu'un pour la "première" fois
  - déterminez, pour les deux trames, les adresses source et destination
  - déterminez à quoi correspond chacune de ces adresses

[Arp Wireshark](./arp_tp2_reseau.pcapng)

```
ARP broadcast :
Source : b4:45:06:a4:5c:76
Destination : ff:ff:ff:ff:ff:ff

ARP reply :
Source : 54:05:db:d7:f6:e3
Destination : b4:45:06:a4:5c:76

Moi : b4:45:06:a4:5c:76
Mon mate : 54:05:db:d7:f6:e3
Broadcast : ff:ff:ff:ff:ff:ff
```

🦈 **PCAP qui contient les trames ARP**

> L'échange ARP est constitué de deux trames : un ARP broadcast et un ARP reply.


# III. DHCP you too my brooo

![YOU GET AN IP](./pics/dhcp.jpg)

*DHCP* pour *Dynamic Host Configuration Protocol* est notre p'tit pote qui nous file des IPs quand on arrive dans un réseau, parce que c'est chiant de le faire à la main :)

Quand on arrive dans un réseau, notre PC contacte un serveur DHCP, et récupère généralement 3 infos :

- **1.** une IP à utiliser
- **2.** l'adresse IP de la passerelle du réseau
- **3.** l'adresse d'un serveur DNS joignable depuis ce réseau

L'échange DHCP  entre un client et le serveur DHCP consiste en 4 trames : **DORA**, que je vous laisse chercher sur le web vous-mêmes : D

🌞 **Wireshark it**

- identifiez les 4 trames DHCP lors d'un échange DHCP
  - mettez en évidence les adresses source et destination de chaque trame
- identifiez dans ces 4 trames les informations **1**, **2** et **3** dont on a parlé juste au dessus

[DHCP Wireshark](./dhcp_tp2_reseau.pcapng)

**1** : 10.33.16.168

**2** : 10.33.19.254

**3** : 8.8.8.8

Discover src: 80:30:49:b6:da:5d dst: ff:ff:ff:ff:ff:ff

Offer src: 00:c0:e7:e0:04:4e dst: ff:ff:ff:ff:ff:ff

Request src: 80:30:49:b6:da:5d dst: ff:ff:ff:ff:ff:ff

ACK src: 00:c0:e7:e0:04:4e dst: ff:ff:ff:ff:ff:ff


🦈 **PCAP qui contient l'échange DORA**