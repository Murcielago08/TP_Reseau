# TP3 : On va router des trucs

Au menu de ce TP, on va revoir un peu ARP et IP histoire de **se mettre en jambes dans un environnement avec des VMs**.

Puis on mettra en place **un routage simple, pour permettre à deux LANs de communiquer**.

![Reboot the router](./pics/reboot.jpeg)

## Sommaire

- [TP3 : On va router des trucs](#tp3--on-va-router-des-trucs)
  - [Sommaire](#sommaire)
  - [0. Prérequis](#0-prérequis)
  - [I. ARP](#i-arp)
    - [1. Echange ARP](#1-echange-arp)
    - [2. Analyse de trames](#2-analyse-de-trames)
  - [II. Routage](#ii-routage)
    - [1. Mise en place du routage](#1-mise-en-place-du-routage)
    - [2. Analyse de trames](#2-analyse-de-trames-1)
    - [3. Accès internet](#3-accès-internet)
  - [III. DHCP](#iii-dhcp)
    - [1. Mise en place du serveur DHCP](#1-mise-en-place-du-serveur-dhcp)
    - [2. Analyse de trames](#2-analyse-de-trames-2)

## 0. Prérequis

➜ Pour ce TP, on va se servir de VMs Rocky Linux. 1Go RAM c'est large large. Vous pouvez redescendre la mémoire vidéo aussi.  

➜ Vous aurez besoin de deux réseaux host-only dans VirtualBox :

- un premier réseau `10.3.1.0/24`
- le second `10.3.2.0/24`
- **vous devrez désactiver le DHCP de votre hyperviseur (VirtualBox) et définir les IPs de vos VMs de façon statique**

➜ Les firewalls de vos VMs doivent **toujours** être actifs (et donc correctement configurés).

➜ **Si vous voyez le p'tit pote 🦈 c'est qu'il y a un PCAP à produire et à mettre dans votre dépôt git de rendu.**

## I. ARP

Première partie simple, on va avoir besoin de 2 VMs.

| Machine  | `10.3.1.0/24` |
|----------|---------------|
| `john`   | `10.3.1.11`   |
| `marcel` | `10.3.1.12`   |

```schema
   john               marcel
  ┌─────┐             ┌─────┐
  │     │    ┌───┐    │     │
  │     ├────┤ho1├────┤     │
  └─────┘    └───┘    └─────┘
```

> Référez-vous au [mémo Réseau Rocky](../../cours/memo/rocky_network.md) pour connaître les commandes nécessaire à la réalisation de cette partie.

### 1. Echange ARP

🌞**Générer des requêtes ARP**

- effectuer un `ping` d'une machine à l'autre
- observer les tables ARP des deux machines
- repérer l'adresse MAC de `john` dans la table ARP de `marcel` et vice-versa
- prouvez que l'info est correcte (que l'adresse MAC que vous voyez dans la table est bien celle de la machine correspondante)
  - une commande pour voir la MAC de `marcel` dans la table ARP de `john`
  - et une commande pour afficher la MAC de `marcel`, depuis `marcel`
```
marcel :
[murci@localhost ~]$ ip n s 10.3.1.11
10.3.1.11 dev enp0s8 llaaddr 08:00:27:cd:c3:ae STALE

john:
[murci@localhost ~]$ ip n s 10.3.1.12
10.3.1.12 dev enp0s8 llaaddr 08:00:27:65:01:b9 STALE
```
```
marcel:
[murci@localhost ~]$ ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:cd:c3:ae brd ff:ff:ff:ff:ff:ff

john :
[murci@localhost ~]$ ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:65:01:b9 brd ff:ff:ff:ff:ff:ff
```

### 2. Analyse de trames

🌞**Analyse de trames**

- utilisez la commande `tcpdump` pour réaliser une capture de trame
- videz vos tables ARP, sur les deux machines, puis effectuez un `ping`

```
[murci@localhost ~]$ sudo ip n f all

sudo tcpdump -i enp0s8 -c 10 -w tp3_arp.pcapng
dropped privs to tcpdump
tcpdump: listening on enp0s8, link-type EN10MB (Ethernet), snapshot length 262144 bytes

10 packets captured
10 packets received by filter
0 packets dropped by kernel

ping 10.3.1.11

[murci@localhost ~]$ scp murci@10.3.1.11:/home/murci/tp3_arp.pcapng .
murci@10.3.1.11's password:
tp3_arp.pcapng                                                                        100% 1502     1.5MB/s   00:00
```

[ARP_Lan](./tp3_arp.pcap)

🦈 **Capture réseau `tp3_arp.pcapng`** qui contient un ARP request et un ARP reply

> **Si vous ne savez pas comment récupérer votre fichier `.pcapng`** sur votre hôte afin de l'ouvrir dans Wireshark, et me le livrer en rendu, demandez-moi.

## II. Routage

Vous aurez besoin de 3 VMs pour cette partie. **Réutilisez les deux VMs précédentes.**

| Machine  | `10.3.1.0/24` | `10.3.2.0/24` |
|----------|---------------|---------------|
| `router` | `10.3.1.254`  | `10.3.2.254`  |
| `john`   | `10.3.1.11`   | no            |
| `marcel` | no            | `10.3.2.12`   |

> Je les appelés `marcel` et `john` PASKON EN A MAR des noms nuls en réseau 🌻

```schema
   john                router              marcel
  ┌─────┐             ┌─────┐             ┌─────┐
  │     │    ┌───┐    │     │    ┌───┐    │     │
  │     ├────┤ho1├────┤     ├────┤ho2├────┤     │
  └─────┘    └───┘    └─────┘    └───┘    └─────┘
```

### 1. Mise en place du routage

🌞**Activer le routage sur le noeud `router`**

```
avant:
[murci@localhost ~]$ sudo firewall-cmd --list-all
masquerade: no

après:
[murci@localhost ~]$ sudo firewall-cmd --list-all
masquerade: yes
```

> Cette étape est nécessaire car Rocky Linux c'est pas un OS dédié au routage par défaut. Ce n'est bien évidemment une opération qui n'est pas nécessaire sur un équipement routeur dédié comme du matériel Cisco.

🌞**Ajouter les routes statiques nécessaires pour que `john` et `marcel` puissent se `ping`**

- il faut taper une commande `ip route add` pour cela, voir mémo
- il faut ajouter une seule route des deux côtés
- une fois les routes en place, vérifiez avec un `ping` que les deux machines peuvent se joindre

```
john:
[murci@localhost ~]$ ip route add 10.3.1.0/24 via 10.3.2.254 dev enp0s8

[murci@localhost ~]$ ping 10.3.2.12
PING 10.3.1.11 (10.3.1.11) 56(84) bytes of data.
64 bytes from 10.3.1.11: icmp_seq=1 ttl=63 time=0.606 ms
64 bytes from 10.3.1.11: icmp_seq=2 ttl=63 time=0.779 ms

marcel:
[murci@localhost ~]$ ip route add 10.3.2.0/24 via 10.3.1.254 dev enp0s8

[murci@localhost ~]$ ping 10.3.1.11
PING 10.3.1.11 (10.3.1.11) 56(84) bytes of data.
64 bytes from 10.3.1.11: icmp_seq=1 ttl=63 time=0.606 ms
64 bytes from 10.3.1.11: icmp_seq=2 ttl=63 time=0.779 ms
```

![THE SIZE](./pics/thesize.png)

### 2. Analyse de trames

🌞**Analyse des échanges ARP**

- videz les tables ARP des trois noeuds
- effectuez un `ping` de `john` vers `marcel`
- regardez les tables ARP des trois noeuds
- essayez de déduire un peu les échanges ARP qui ont eu lieu
- répétez l'opération précédente (vider les tables, puis `ping`), en lançant `tcpdump` sur `marcel`

```
john:
[murci@localhost ~]$ ip n f all

[murci@localhost ~]$ ping 10.3.2.12
PING 10.3.2.12 (10.3.2.12) 56(84) bytes of data.
64 bytes from 10.3.2.12: icmp_seq=1 ttl=63 time=0.904 ms
64 bytes from 10.3.2.12: icmp_seq=2 ttl=63 time=0.758 ms

[murci@localhost ~]$ ip n s
10.3.1.254 dev enp0s8 lladdr 08:00:27:c7:88:1b REACHABLE
10.3.1.1 dev enp0s8 lladdr 0a:00:27:00:00:13 REACHABLE

mercel:
[murci@localhost ~]$ ip n f all
[murci@localhost ~]$ ip n s
10.3.2.1 dev enp0s8 lladdr 0a:00:27:00:00:17 REACHABLE
10.3.2.254 dev enp0s8 lladdr 08:00:27:b2:44:bf STALE

routeur:
[root@localhost ~]$ ip n f all
[root@localhost ~]$ ip n s
10.3.2.12 dev enp0s8 lladdr 08:00:27:c7:88:1b REACHABLE
10.3.1.11 dev enp0s8 lladdr 0a:00:27:00:00:13 REACHABLE

John fait un échange ARP avec son reseau et le routeur, le routeur resoit le ping et renvoie le ping dans le reseau 10.3.1.0 et 10.3.2.0, marcel resoit donc le ping
```

- **écrivez, dans l'ordre, les échanges ARP qui ont eu lieu, puis le ping et le pong, je veux TOUTES les trames** utiles pour l'échange

Par exemple (copiez-collez ce tableau ce sera le plus simple) :

| ordre | type trame  | IP source | MAC source              | IP destination | MAC destination            |
|-------|-------------|-----------|-------------------------|----------------|----------------------------|
| 1     | Requête ARP | x         |`Routeur` `08:00:27:B2:44:BF`| x          | Broadcast `FF:FF:FF:FF:FF` |
| 2     | Réponse ARP | x         |`marcel` `08:00:27:65:01:B9`| x           | `Routeur` `08:00:27:B2:44:BF`|
| 3     | Ping        | 10.3.2.254|`Routeur` `08:00:27:B2:44:BF`|10.3.2.12   | Broadcast `FF:FF:FF:FF:FF` |
| 4     | Pong        | 10.3.2.12 |`marcel` `08:00:27:65:01:B9`|10.3.2.254   | `Routeur` `08:00:27:B2:44:BF`|
| 5     | Requête ARP | x         |`marcel` `08:00:27:65:01:B9`| x           | `Routeur` `08:00:27:B2:44:BF`|
| 6     | Réponse ARP | x         |`Routeur` `08:00:27:B2:44:BF`| x          | `marcel` `08:00:27:65:01:B9`|
> Vous pourriez, par curiosité, lancer la capture sur `john` aussi, pour voir l'échange qu'il a effectué de son côté.

[ARP_routage](tp3_routage_marcel.pcap)

🦈 **Capture réseau `tp3_routage_marcel.pcapng`**

### 3. Accès internet

🌞**Donnez un accès internet à vos machines**

- ajoutez une carte NAT en 3ème inteface sur le `router` pour qu'il ait un accès internet
- ajoutez une route par défaut à `john` et `marcel`
  - vérifiez que vous avez accès internet avec un `ping`
  - le `ping` doit être vers une IP, PAS un nom de domaine

```
[murci@localhost ~]$ ping 192.168.1.1
PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=62 time=2.32 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=62 time=1.96 ms
64 bytes from 192.168.1.1: icmp_seq=3 ttl=62 time=2.13 ms
64 bytes from 192.168.1.1: icmp_seq=4 ttl=62 time=2.23 ms
```

- donnez leur aussi l'adresse d'un serveur DNS qu'ils peuvent utiliser
  - vérifiez que vous avez une résolution de noms qui fonctionne avec `dig`
  - puis avec un `ping` vers un nom de domaine

```
[murci@localhost ~]$ dig google.com

; <<>> DiG 9.16.23-RH <<>> google.com
;; SERVER: 8.8.8.8#53(8.8.8.8)

[murci@localhost ~]$ ping google.com
PING google.com (142.250.179.78) 56(84) bytes of data.
64 bytes from par21s19-in-f14.1e100.net (142.250.179.78): icmp_seq=1 ttl=115 time=16.1 ms
64 bytes from par21s19-in-f14.1e100.net (142.250.179.78): icmp_seq=2 ttl=115 time=16.2 ms
```

🌞**Analyse de trames**

- effectuez un `ping 8.8.8.8` depuis `john`

```
[murci@localhost ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=115 time=15.9 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=115 time=15.0 ms
```
- capturez le ping depuis `john` avec `tcpdump`

```
[murci@localhost ~]$ sudo tcpdump -i enp0s8 -c 10 -w tp3_routage_internet.pcapng
dropped privs to tcpdump
tcpdump: listening on enp0s8, link-type EN10MB (Ethernet), snapshot length 262144 bytes
10 packets captured
11 packets received by filter
0 packets dropped by kernel

[murci@localhost ~]$ scp murci@10.3.2.12:/home/murci/tp3_routage_internet.pcapng .
[sudo] password for murci:
murci@10.3.2.12's password:
tp3_routage_internet.pcapng                                                        100%  936     2.6MB/s   00:00
```

- analysez un ping aller et le retour qui correspond et mettez dans un tableau :

| ordre | type trame | IP source          | MAC source              | IP destination | MAC destination |
|-------|------------|--------------------|-------------------------|----------------|-----------------|
| 1     | ping       |`john` `10.3.1.11`  |`john` `08:00:27:63:F7:AF`|`8.8.8.8`      |`08:00:27:27:F6:5A`|
| 2     | pong       |`8.8.8.8`           |`08:00:27:27:F6:5A`      |`john` `10.3.1.11`|`john` `08:00:27:63:F7:AF`|

[Routage internet](./tp3_routage_internet.pcapng)

🦈 **Capture réseau `tp3_routage_internet.pcapng`**

## III. DHCP

On reprend la config précédente, et on ajoutera à la fin de cette partie une 4ème machine pour effectuer des tests.

| Machine  | `10.3.1.0/24`              | `10.3.2.0/24` |
|----------|----------------------------|---------------|
| `router` | `10.3.1.254`               | `10.3.2.254`  |
| `john`   | `10.3.1.11`                | no            |
| `bob`    | oui mais pas d'IP statique | no            |
| `marcel` | no                         | `10.3.2.12`   |

```schema
   john               router              marcel
  ┌─────┐             ┌─────┐             ┌─────┐
  │     │    ┌───┐    │     │    ┌───┐    │     │
  │     ├────┤ho1├────┤     ├────┤ho2├────┤     │
  └─────┘    └─┬─┘    └─────┘    └───┘    └─────┘
   john        │
  ┌─────┐      │
  │     │      │
  │     ├──────┘
  └─────┘
```

### 1. Mise en place du serveur DHCP

🌞**Sur la machine `john`, vous installerez et configurerez un serveur DHCP** (go Google "rocky linux dhcp server").

- installation du serveur sur `john`
  
```
[murci@localhost ~]$ sudo dnf install dhcp-server

[murci@localhost ~]$ sudo nano /etc/dhcp/dhcp.conf
default-lease-time 900;
max-lease-time 10800;

authoritative;

subnet 10.3.1.0 netmask 255.255.255.0 {
range 10.3.1.20 10.3.1.99;
option routeurs 10.3.1.254;
}
```
- créer une machine `bob`
- faites lui récupérer une IP en DHCP à l'aide de votre serveur
```
[murci@localhost ~]$ sudo dnf install dhcp-client

[murci@localhost ~]$ nano /etc/sysconfig/network-scripts/ifcfg-enp0s8
NAME=enp0s8
DEVICE=enp0s8

BOOTPROTO=dhcp
ONBOOT=yes

[murci@localhost ~]$ sudo dhclient

[murci@localhost ~]$ ip a
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:5b:e5:75 brd ff:ff:ff:ff:ff:ff
    inet 10.3.1.2/24 brd 10.3.1.255 scope global dynamic noprefixroute enp0s8
       valid_lft 755sec preferred_lft 755sec
```

> Il est possible d'utilise la commande `dhclient` pour forcer à la main, depuis la ligne de commande, la demande d'une IP en DHCP, ou renouveler complètement l'échange DHCP (voir `dhclient -h` puis call me et/ou Google si besoin d'aide).

🌞**Améliorer la configuration du DHCP**

- ajoutez de la configuration à votre DHCP pour qu'il donne aux clients, en plus de leur IP :
  - une route par défaut
  - un serveur DNS à utiliser
```
option routers 10.3.1.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 8.8.8.8;
```
- récupérez de nouveau une IP en DHCP sur `bob` pour tester :
  - `marcel` doit avoir une IP
    - vérifier avec une commande qu'il a récupéré son IP
    - vérifier qu'il peut `ping` sa passerelle
```
[murci@localhost ~]$ sudo dhclient -r
Killed old client process

[murci@localhost ~]$ sudo dhclient

[murci@localhost ~]$ ip a
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:5b:e5:75 brd ff:ff:ff:ff:ff:ff
    inet 10.3.1.2/24 brd 10.3.1.255 scope global dynamic noprefixroute enp0s8
       valid_lft 872sec preferred_lft 872sec

[murci@localhost ~]$ ping 10.3.1.254
PING 10.3.1.254 (10.3.1.254) 56(84) bytes of data.
64 bytes from 10.3.1.254: icmp_seq=1 ttl=64 time=0.282 ms
```
  - il doit avoir une route par défaut
    - vérifier la présence de la route avec une commande
    - vérifier que la route fonctionne avec un `ping` vers une IP
```
[murci@localhost ~]$ ip r s
default via 10.3.1.254 dev enp0s8 proto dhcp src 10.3.1.2 metric 100
10.3.1.0/24 dev enp0s8 proto kernel scope link src 10.3.1.2 metric 100

[murci@localhost ~]$ ping 10.3.2.12
PING 10.3.2.12 (10.3.2.12) 56(84) bytes of data.
64 bytes from 10.3.2.12: icmp_seq=1 ttl=63 time=0.725 ms
64 bytes from 10.3.2.12: icmp_seq=2 ttl=63 time=0.868 ms
```
  - il doit connaître l'adresse d'un serveur DNS pour avoir de la résolution de noms
    - vérifier avec la commande `dig` que ça fonctionne
    - vérifier un `ping` vers un nom de domaine*
```
[murci@localhost ~]$ dig google.com
;; ANSWER SECTION:
google.com.             300     IN      A       142.250.75.238

[murci@localhost ~]$ ping 142.250.75.238
PING 142.250.75.238 (142.250.75.238) 56(84) bytes of data.
64 bytes from 142.250.75.238: icmp_seq=1 ttl=115 time=17.9 ms
64 bytes from 142.250.75.238: icmp_seq=2 ttl=115 time=15.0 ms
```

### 2. Analyse de trames

🌞**Analyse de trames**

- lancer une capture à l'aide de `tcpdump` afin de capturer un échange DHCP
- demander une nouvelle IP afin de générer un échange DHCP
- exportez le fichier `.pcapng`
```
bob:
[murci@localhost ~]$ dhclient -r
[murci@localhost ~]$ dhclient

john:
[murci@localhost ~]$ sudo tcpdump -i enp0s8 -c 10 -w tp3_dhcp.pcapng
dropped privs to tcpdump
tcpdump: listening on enp0s8, link-type EN10MB (Ethernet), snapshot length 262144 bytes
10 packets captured
11 packets received by filter
0 packets dropped by kernel


C:\Users\darkj> scp murci@10.3.1.11:/home/murci/tp3_dhcp.pcapng .
murci@10.3.1.11's password:
tp3_dhcp.pcapng                                                                       100% 2548     2.5MB/s   00:00
```
[DHCP_client](./tp3_dhcp.pcap)

🦈 **Capture réseau `tp3_dhcp.pcapng`**