# TP3 INFRA : Premiers pas GNS, Cisco et VLAN

On va utiliser GNS3 dans ce TP pour se rapprocher d'un cas réel. On va focus sur l'aspect switching, avec du matériel Cisco. On va aussi mettre en place des VLANs.

![best memes from cisco doc](./pics/the-best-memes-come-from-cisco-documentation.jpg)

# Sommaire

- [TP3 INFRA : Premiers pas GNS, Cisco et VLAN](#tp3-infra--premiers-pas-gns-cisco-et-vlan)
- [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
- [I. Dumb switch](#i-dumb-switch)
  - [1. Topologie 1](#1-topologie-1)
  - [2. Adressage topologie 1](#2-adressage-topologie-1)
  - [3. Setup topologie 1](#3-setup-topologie-1)
- [II. VLAN](#ii-vlan)
  - [1. Topologie 2](#1-topologie-2)
  - [2. Adressage topologie 2](#2-adressage-topologie-2)
    - [3. Setup topologie 2](#3-setup-topologie-2)
- [III. Ptite VM DHCP](#iii-ptite-vm-dhcp)

# 0. Prérequis

➜ **GNS3 installé et prêt à l'emploi**

- [GNS3VM](https://www.gns3.com/software/download-vm) fonctionnelle
- de quoi faire tourner un switch Cisco
  - [IOU2 L2 dispo ici](http://dl.nextadmin.net/dl/EVE-NG-image/iol/bin/i86bi_linux_l2-adventerprisek9-ms.SSA.high_iron_20180510.bin)
- de quoi faire tourner un routeur Cisco
  - [image d'un 3745 dispo ici](http://dl.nextadmin.net/dl/EVE-NG-image/dynamips/c3725-adventerprisek9-mz.124-15.T14.image)

➜ **Les clients seront des VPCS**

- c'est un truc de GNS pour simuler un client du réseau
- quand on veut juste un truc capable de faire des pings et rien de plus, c'est parfait
- ça consomme R en ressources

# I. Dumb switch

## 1. Topologie 1

![Topologie 1](./pics/topo1.png)

## 2. Adressage topologie 1

| Node  | IP            |
| ----- | ------------- |
| `pc1` | `10.3.1.1/24` |
| `pc2` | `10.3.1.2/24` |

## 3. Setup topologie 1

🌞 **Commençons simple**

- définissez les IPs statiques sur les deux VPCS
- `ping` un VPCS depuis l'autre

```
PC2> ip 10.3.1.2 255.255.255.0
Checking for duplicate address...
PC2 : 10.3.1.2 255.255.255.0

PC2> ping 10.3.1.1

84 bytes from 10.3.1.1 icmp_seq=1 ttl=64 time=0.138 ms
84 bytes from 10.3.1.1 icmp_seq=2 ttl=64 time=0.267 ms
84 bytes from 10.3.1.1 icmp_seq=3 ttl=64 time=0.324 ms
84 bytes from 10.3.1.1 icmp_seq=4 ttl=64 time=0.247 ms
```

# II. VLAN

## 1. Topologie 2

![Topologie 2](./pics/topo2.png)

## 2. Adressage topologie 2

| Node  | IP            | VLAN |
| ----- | ------------- | ---- |
| `pc1` | `10.3.1.1/24` | 10   |
| `pc2` | `10.3.1.2/24` | 10   |
| `pc3` | `10.3.1.3/24` | 20   |

### 3. Setup topologie 2

🌞 **Adressage**

- définissez les IPs statiques sur tous les VPCS
- vérifiez avec des `ping` que tout le monde se ping

```
PC1> ip 10.3.1.1 255.255.255.0
Checking for duplicate address...
PC1 : 10.3.1.1 255.255.255.0

PC1>
PC1> ping 10.3.1.2
84 bytes from 10.3.1.2 icmp_seq=1 ttl=64 time=0.942 ms
84 bytes from 10.3.1.2 icmp_seq=2 ttl=64 time=1.474 ms

PC1> ping 10.3.1.3
84 bytes from 10.3.1.3 icmp_seq=1 ttl=64 time=0.855 ms
84 bytes from 10.3.1.3 icmp_seq=2 ttl=64 time=1.164 ms
84 bytes from 10.3.1.3 icmp_seq=3 ttl=64 time=1.564 ms
```

🌞 **Configuration des VLANs**

- référez-vous [à la section VLAN du mémo Cisco](../../cours/memo/memo_cisco.md#8-vlan)
- déclaration des VLANs sur le switch `sw1`
- ajout des ports du switches dans le bon VLAN (voir [le tableau d'adressage de la topo 2 juste au dessus](#2-adressage-topologie-2))
  - ici, tous les ports sont en mode *access* : ils pointent vers des clients du réseau

🌞 **Vérif**

- `pc1` et `pc2` doivent toujours pouvoir se ping

```
PC1> ping 10.3.1.2
84 bytes from 10.3.1.2 icmp_seq=1 ttl=64 time=0.947 ms
84 bytes from 10.3.1.2 icmp_seq=2 ttl=64 time=1.323 ms
84 bytes from 10.3.1.2 icmp_seq=3 ttl=64 time=1.081 ms

PC1> ping 10.3.1.3
host (10.3.1.3) not reachable
```

- `pc3` ne ping plus personne

```
PC3> ping 10.3.1.1
host (10.3.1.1) not reachable

PC3> ping 10.3.1.2
host (10.3.1.2) not reachable
```

![i know cisco](./pics/i_know.jpeg)

# III. Ptite VM DHCP

On va ajouter une VM dans la topologie, histoire que vous voyiez cette aspect de GNS.

| Node          | IP              | VLAN |
| ------------- | --------------- | ---- |
| `pc1`         | `10.3.1.1/24`   | 10   |
| `pc2`         | `10.3.1.2/24`   | 10   |
| `pc3`         | `10.3.1.3/24`   | 20   |
| `pc4`         | X               | 20   |
| `pc5`         | X               | 10   |
| `dhcp.tp3.b2` | `10.3.1.253/24` | 20   |

🌞 **VM `dhcp.tp3.b2`**

- Rocky Linux, IP statique, nom défini à `dhcp.tp3.b2`, SELinux désactivé, firewall activé, système à jour, NORMAL LA ROUTINE QUOI
- installez un serveur DHCP
  - il doit délivrer des IPs entre `10.3.1.100` et `10.3.1.200`

```
[joris@dhcptp3b2 ~]$ sudo cat /etc/dhcp/dhcpd.conf
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#
default-lease-time 900;
max-lease-time 10800;

authoritative;

subnet 10.3.1.0 netmask 255.255.255.0 {
range 10.3.1.100 10.3.1.200;
option routers 10.3.1.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.1.1.1;
}
```

- vérifier avec le `pc4` que vous pouvez récupérer une IP en DHCP

```
PC4> ip dhcp -r
DDORA IP 10.3.1.100/24 GW 10.3.1.254
```

- vérifier avec le `pc5` que vous ne pouvez PAS récupérer une IP en DHCP

```
PC5> ip dhcp -r
DDD
Can't find dhcp server
```

> Pour rappel, la trame DHCP Discover part en broadcast. Le switch bloque ça aussi, il bloque tout, il s'en fout de la nature de la trame : si ça passe d'un port taggé VLAN X à un port taggé VLAN Y, ça dégage.