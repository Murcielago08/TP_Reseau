# TP4 : Router-on-a-stick

On va utiliser GNS3 dans ce TP pour se rapprocher d'un cas réel. La topologie qu vous mettez en place en fin de TP c'est tellement du classique qu'on lui a donné un nom : Router on a Stick.

Un seul routeur, plein de switches, plein de clients, plein de VLANs. Router on a Stick.

On va donc focus sur l'aspect routing/switching, avec du matériel Cisco. On va aussi mettre en place des VLANs, et du routage.

![Sounds be like](./img/cisco_switch.jpg)

# Sommaire

- [TP4 : Router-on-a-stick](#tp4--router-on-a-stick)
- [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
  - [Checklist VM Linux](#checklist-vm-linux)
- [I. Topo 1 : VLAN et Routing](#i-topo-1--vlan-et-routing)
  - [1. Topologie 1](#1-topologie-1)
  - [2. Adressage topologie 1](#2-adressage-topologie-1)
  - [3. Setup topologie 1](#3-setup-topologie-1)
- [II. NAT](#ii-nat)
  - [1. Topologie 2](#1-topologie-2)
  - [2. Adressage topologie 2](#2-adressage-topologie-2)
  - [3. Setup topologie 2](#3-setup-topologie-2)
- [III. Add a building](#iii-add-a-building)
  - [2. Adressage topologie 3](#2-adressage-topologie-3)
  - [3. Setup topologie 3](#3-setup-topologie-3)

# 0. Prérequis

➜ Les clients seront soit :

- VMs Rocky Linux
- VPCS
  - c'est un truc de GNS pour simuler un client du réseau
  - quand on veut juste un truc capable de faire des pings et rien de plus, c'est parfait
  - ça consomme R en ressources

> Faites bien attention aux logos des machines sur les schémas, et vous verrez clairement quand il faut un VPCS ou une VM.

➜ Les switches Cisco des vIOL2 (IOU)

➜ Les routeurs Cisco des c3640

➜ **Vous ne créerez aucune machine virtuelle au début. Vous les créerez au fur et à mesure que le TP vous le demande.** A chaque fois qu'une nouvelle machine devra être créée, vous trouverez l'emoji 🖥️ avec son nom.

## Checklist VM Linux

A chaque machine déployée, vous **DEVREZ** vérifier la 📝**checklist**📝 :

- [x] IP locale, statique ou dynamique
- [x] hostname défini
- [x] firewall actif, qui ne laisse passer que le strict nécessaire
- [x] on force une host-only, juste pour pouvoir SSH
- [x] SSH fonctionnel
- [x] résolution de nom
  - vers internet, quand vous aurez le routeur en place

**Les éléments de la 📝checklist📝 sont STRICTEMENT OBLIGATOIRES à réaliser mais ne doivent PAS figurer dans le rendu.**

# I. Topo 1 : VLAN et Routing

Dans cette partie, on va donner un peu de sens aux VLANs :

- un pour les serveurs du réseau
  - on simulera ça avec un p'tit serveur web
- un pour les admins du réseau
- un pour les autres random clients du réseau

Cela dit, il faut que tout ce beau monde puisse se ping, au moins joindre le réseau des serveurs, pour accéder au super site-web.

**Bien que bloqué au niveau du switch à cause des VLANs, le trafic pourra passer d'un VLAN à l'autre grâce à un routeur.**

Il assurera son job de routeur traditionnel : router entre deux réseaux. Sauf qu'en plus, il gérera le changement de VLAN à la volée.

## 1. Topologie 1

![Topologie 1](../img/topo1.png)

## 2. Adressage topologie 1

Les réseaux et leurs VLANs associés :

| Réseau    | Adresse        | VLAN associé |
| --------- | -------------- | ------------ |
| `clients` | `10.1.1.0/24`  | 10           |
| `admins`  | `10.1.20.0/24` | 20           |
| `servers` | `10.1.30.0/24` | 30           |

L'adresse des machines au sein de ces réseaux :

| Node               | `clients`       | `admins`         | `servers`        |
| ------------------ | --------------- | ---------------- | ---------------- |
| `pc1.clients.tp4`  | `10.1.1.1/24`   | x                | x                |
| `pc2.clients.tp4`  | `10.1.1.2/24`   | x                | x                |
| `adm1.admins.tp4`  | x               | `10.1.20.1/24`   | x                |
| `web1.servers.tp4` | x               | x                | `10.1.30.1/24`   |
| `r1`               | `10.1.1.254/24` | `10.1.20.254/24` | `10.1.30.254/24` |

## 3. Setup topologie 1

🖥️ VM `web1.servers.tp4`, déroulez la [Checklist VM Linux](#checklist-vm-linux) dessus

🌞 **Adressage**

- définissez les IPs statiques sur toutes les machines **sauf le *routeur***

```
[joris@web1serverstp4 ~]$ ip -c a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:f6:4f:f9 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::a00:27ff:fef6:4ff9/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:49:7d:ae brd ff:ff:ff:ff:ff:ff
    inet 10.1.30.1/24 brd 10.1.30.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe49:7dae/64 scope link
       valid_lft forever preferred_lft forever

PC1 : 10.1.1.1 255.255.255.0
PC2 : 10.1.1.2 255.255.255.0
Adm1 : 10.1.20.1 255.255.255.0
```
---

🌞 **Configuration des VLANs**

- référez-vous au [mémo Cisco](../../../../cours/memo/memo_cisco.md)
- déclaration des VLANs sur le switch `sw1`
- ajout des ports du switches dans le bon VLAN (voir [le tableau d'adressage de la topo 2 juste au dessus](#2-adressage-topologie-2))
- il faudra ajouter le port qui pointe vers le *routeur* comme un *trunk* : c'est un port entre deux équipements réseau (un *switch* et un *routeur*)

```
IOU1#show interface trunk

Port        Mode             Encapsulation  Status        Native vlan
Et0/0       on               802.1q         trunking      1

Port        Vlans allowed on trunk
Et0/0       1-4094

Port        Vlans allowed and active in management domain
Et0/0       1,10,20,30

Port        Vlans in spanning tree forwarding state and not pruned
Et0/0       1,10,20,30

IOU1#s vlan br

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Et1/2, Et1/3, Et2/0, Et2/1
                                                Et2/2, Et2/3, Et3/0, Et3/1
                                                Et3/2, Et3/3
10   clients                          active    Et0/1, Et0/2
20   admins                           active    Et0/3
30   servers                          active    Et1/0, Et1/1
1002 fddi-default                     act/unsup
1003 token-ring-default               act/unsup
1004 fddinet-default                  act/unsup
1005 trnet-default                    act/unsup

IOU1#show mac address-table
          Mac Address Table
-------------------------------------------

Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
   1    c201.054f.0000    DYNAMIC     Et0/0
  30    0800.27f6.4ff9    DYNAMIC     Et1/0
Total Mac Addresses for this criterion: 2

```
---

🌞 **Config du *routeur***

- attribuez ses IPs au *routeur*
  - 3 sous-interfaces, chacune avec son IP et un VLAN associé

```
R1#s ip int br
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            unassigned      YES NVRAM  up                    up
FastEthernet0/0.10         10.1.10.254     YES NVRAM  up                    up
FastEthernet0/0.20         10.1.20.254     YES NVRAM  up                    up
FastEthernet0/0.30         10.1.30.254     YES NVRAM  up                    up
FastEthernet0/1            unassigned      YES NVRAM  administratively down down
FastEthernet1/0            unassigned      YES NVRAM  administratively down down
FastEthernet2/0            unassigned      YES NVRAM  administratively down down
R1#s ip route
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route

Gateway of last resort is not set

     10.0.0.0/24 is subnetted, 3 subnets
C       10.1.10.0 is directly connected, FastEthernet0/0.10
C       10.1.30.0 is directly connected, FastEthernet0/0.30
C       10.1.20.0 is directly connected, FastEthernet0/0.20
```

🌞 **Vérif**

- tout le monde doit pouvoir ping le routeur sur l'IP qui est dans son réseau
- en ajoutant une route vers les réseaux, ils peuvent se ping entre eux
  - ajoutez une route par défaut sur les VPCS
  - ajoutez une route par défaut sur la machine virtuelle
  - testez des `ping` entre les réseaux

```
PC1> ping 10.1.20.1
84 bytes from 10.1.20.1 icmp_seq=1 ttl=63 time=17.316 ms
84 bytes from 10.1.20.1 icmp_seq=2 ttl=63 time=22.881 ms
84 bytes from 10.1.20.1 icmp_seq=3 ttl=63 time=21.685 ms
84 bytes from 10.1.20.1 icmp_seq=4 ttl=63 time=16.704 ms
84 bytes from 10.1.20.1 icmp_seq=5 ttl=63 time=15.441 ms

PC1> ping 10.1.10.2
84 bytes from 10.1.10.2 icmp_seq=1 ttl=64 time=0.924 ms
84 bytes from 10.1.10.2 icmp_seq=2 ttl=64 time=1.250 ms
84 bytes from 10.1.10.2 icmp_seq=3 ttl=64 time=1.366 ms

PC1> ping 10.1.10.254
84 bytes from 10.1.10.254 icmp_seq=1 ttl=255 time=9.295 ms
84 bytes from 10.1.10.254 icmp_seq=2 ttl=255 time=3.323 ms
84 bytes from 10.1.10.254 icmp_seq=3 ttl=255 time=7.181 ms

(pcs test pour voir si la connection est fonctionnel car VM server bug :/)
PC1> ping 10.1.30.2
84 bytes from 10.1.30.2 icmp_seq=1 ttl=63 time=33.246 ms
84 bytes from 10.1.30.2 icmp_seq=2 ttl=63 time=21.898 ms
84 bytes from 10.1.30.2 icmp_seq=3 ttl=63 time=20.977 ms
84 bytes from 10.1.30.2 icmp_seq=4 ttl=63 time=13.151 ms

```

# II. NAT

On va ajouter une fonctionnalité au routeur : le NAT.

On va le connecter à internet (simulation du fait d'avoir une IP publique) et il va faire du NAT pour permettre à toutes les machines du réseau d'avoir un accès internet.

![Yellow cable](../img/yellow-cable.png)

## 1. Topologie 2

![Topologie 2](../img/topo2.png)

## 2. Adressage topologie 2

Les réseaux et leurs VLANs associés :

| Réseau    | Adresse        | VLAN associé |
| --------- | -------------- | ------------ |
| `clients` | `10.1.10.0/24` | 10           |
| `admins`  | `10.1.20.0/24` | 20           |
| `servers` | `10.1.30.0/24` | 30           |

L'adresse des machines au sein de ces réseaux :

| Node               | `clients`       | `admins`         | `servers`        |
| ------------------ | --------------- | ---------------- | ---------------- |
| `pc1.clients.tp4`  | `10.1.1.1/24`   | x                | x                |
| `pc2.clients.tp4`  | `10.1.1.2/24`   | x                | x                |
| `adm1.admins.tp4`  | x               | `10.1.20.1/24`   | x                |
| `web1.servers.tp4` | x               | x                | `10.1.30.1/24`   |
| `r1`               | `10.1.1.254/24` | `10.1.20.254/24` | `10.1.30.254/24` |

## 3. Setup topologie 2

🌞 **Ajoutez le noeud Cloud à la topo**

- branchez à `eth1` côté Cloud
- côté routeur, il faudra récupérer un IP en DHCP
- vous devriez pouvoir `ping 1.1.1.1`

```
R1#sh ip int br
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            unassigned      YES NVRAM  up                    up
FastEthernet0/0.10         10.1.10.254     YES NVRAM  up                    up
FastEthernet0/0.20         10.1.20.254     YES NVRAM  up                    up
FastEthernet0/0.30         10.1.30.254     YES NVRAM  up                    up
FastEthernet0/1            192.168.122.105 YES DHCP   up                    up
FastEthernet1/0            unassigned      YES NVRAM  administratively down down
FastEthernet2/0            unassigned      YES NVRAM  administratively down down

R1#ping 1.1.1.1

Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 1.1.1.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 20/72/176 ms
```

🌞 **Configurez le NAT**

- référez-vous [à la section NAT du mémo Cisco](../../../../cours/memo/memo_cisco.md)

```
R1#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#interface FastEthernet 0/0
R1(config-if)#ip nat inside

*Mar  1 00:07:03.395: %LINEPROTO-5-UPDOWN: Line protocol on Interface NVI0, changed state to up
R1(config-if)#
R1(config-if)#ex
R1(config)#interface FastEthernet 0/1
R1(config-if)#ip nat outside
R1(config-if)#end

*Mar  1 00:07:36.059: %SYS-5-CONFIG_I: Configured from console by console

R1#conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#access-list 1 permit any
R1(config)#ip nat inside source list 1 interface fastEthernet 0/1 overload
R1(config)#end

*Mar  1 00:08:50.003: %SYS-5-CONFIG_I: Configured from console by console

R1#s ip int br
Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            unassigned      YES unset  up                    up
FastEthernet0/0.10         10.1.10.254     YES manual up                    up
FastEthernet0/0.20         10.1.20.254     YES manual up                    up
FastEthernet0/0.30         10.1.30.254     YES manual up                    up
FastEthernet0/1            192.168.94.132  YES DHCP   up                    up
FastEthernet1/0            unassigned      YES unset  administratively down down
FastEthernet2/0            unassigned      YES unset  administratively down down
NVI0                       10.1.10.254     YES unset  up                    up

```

🌞 **Test**

- ajoutez une route par défaut (si c'est pas déjà fait)
  - sur les VPCS
  - sur la machine Linux
- configurez l'utilisation d'un DNS
  - sur les VPCS
  - sur la machine Linux

```
PC1> show ip

NAME        : PC1[1]
IP/MASK     : 10.1.10.1/24 (adapter à chaque machine ^^)
GATEWAY     : 10.1.10.254 (adapter à chaque machine ^^)
DNS         : 8.8.8.8
MAC         : 00:50:79:66:68:00
LPORT       : 10005
RHOST:PORT  : 127.0.0.1:10006
MTU:        : 1500
```

- vérifiez un `ping` vers un nom de domaine

```
PC2> ping ynov.com
ynov.com resolved to 104.26.11.233
84 bytes from 104.26.11.233 icmp_seq=1 ttl=127 time=44.436 ms
84 bytes from 104.26.11.233 icmp_seq=2 ttl=127 time=44.489 ms
84 bytes from 104.26.11.233 icmp_seq=3 ttl=127 time=47.934 ms

(fonctionne sur toute les pcs/vm)
```

# III. Add a building

On a acheté un nouveau bâtiment, faut tirer et configurer un nouveau switch jusque là-bas.

On va en profiter pour setup un serveur DHCP pour les clients qui s'y trouvent.


## 2. Adressage topologie 3

Les réseaux et leurs VLANs associés :

| Réseau    | Adresse        | VLAN associé |
| --------- | -------------- | ------------ |
| `clients` | `10.1.10.0/24`  | 10           |
| `admins`  | `10.1.20.0/24` | 20           |
| `servers` | `10.1.30.0/24` | 30           |

L'adresse des machines au sein de ces réseaux :

| Node                | `clients`       | `admins`         | `servers`        |
| ------------------- | --------------- | ---------------- | ---------------- |
| `pc1.clients.tp4`   | `10.1.10.1/24`   | x                | x                |
| `pc2.clients.tp4`   | `10.1.10.2/24`   | x                | x                |
| `pc3.clients.tp4`   | DHCP            | x                | x                |
| `pc4.clients.tp4`   | DHCP            | x                | x                |
| `pc5.clients.tp4`   | DHCP            | x                | x                |
| `dhcp1.clients.tp4` | `10.1.10.253/24` | x                | x                |
| `adm1.admins.tp4`   | x               | `10.1.20.1/24`   | x                |
| `web1.servers.tp4`  | x               | x                | `10.1.30.1/24`   |
| `r1`                | `10.1.10.254/24` | `10.1.20.254/24` | `10.1.30.254/24` |

## 3. Setup topologie 3

Vous pouvez partir de la topologie 2.

🌞  **Vous devez me rendre le `show running-config` de tous les équipements**

- de tous les équipements réseau
  - le routeur
  - les 3 switches

> N'oubliez pas les VLANs sur tous les switches.

**Toutes les confs sont juste ici ^^ [confs routeur/switchs](/B2_2023/Infra_Tp4/running-config.md)**

🖥️ **VM `dhcp1.client1.tp4`**, déroulez la [Checklist VM Linux](#checklist-vm-linux) dessus

🌞  **Mettre en place un serveur DHCP dans le nouveau bâtiment**

- il doit distribuer des IPs aux clients dans le réseau `clients` qui sont branchés au même switch que lui
- sans aucune action manuelle, les clients doivent...
  - avoir une IP dans le réseau `clients`
  - avoir un accès au réseau `servers`
  - avoir un accès WAN
  - avoir de la résolution DNS

> Réutiliser un serveur DHCP qu'on a monté dans un autre TP si vous avez.

```
[joris@dhcp1client1tp4 ~]$ sudo cat /etc/dhcp/dhcpd.conf
[sudo] password for joris:
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#
default-lease-time 900;
max-lease-time 10800;

authoritative;

subnet 10.1.10.0 netmask 255.255.255.0 {
range 10.1.10.100 10.1.10.200;
option routers 10.1.10.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.1.1.1;
}
```

🌞  **Vérification**

- un client récupère une IP en DHCP
- il peut ping le serveur Web
- il peut ping `1.1.1.1`
- il peut ping `ynov.com`

> Faites ça sur n'importe quel VPCS que vous venez d'ajouter : `pc3` ou `pc4` ou `pc5`.

```
problème entre le switch et le serveur dhcp personne ne peut le ping et il ne peut ping personne conséquence il ne donne pas les adresse en dhcp
```