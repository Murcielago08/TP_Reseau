# TP4 : TCP, UDP et services réseau

Dans ce TP on va explorer un peu les protocoles TCP et UDP. 

**La première partie est détente**, vous explorez TCP et UDP un peu, en vous servant de votre PC.

La seconde partie se déroule en environnement virtuel, avec des VMs. Les VMs vont nous permettre en place des services réseau, qui reposent sur TCP et UDP.  
**Le but est donc de commencer à mettre les mains de plus en plus du côté administration, et pas simple client.**

Dans cette seconde partie, vous étudierez donc :

- le protocole SSH (contrôle de machine à distance)
- le protocole DNS (résolution de noms)
  - essentiel au fonctionnement des réseaux modernes

![TCP UDP](./pics/tcp_udp.jpg)

# Sommaire

- [TP4 : TCP, UDP et services réseau](#tp4--tcp-udp-et-services-réseau)
- [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
- [I. First steps](#i-first-steps)
  - [Battle.net](#battlenet)
  - [Discord](#discord)
  - [Minecraft](#minecraft)
  - [Soundcloud](#soundcloud)
  - [PokeMMO](#pokemmo)
- [II. Mise en place](#ii-mise-en-place)
  - [1. SSH](#1-ssh)
- [III. DNS](#iii-dns)
  - [2. Setup](#2-setup)
  - [3. Test](#3-test)

# 0. Prérequis

➜ Pour ce TP, on va se servir de VMs Rocky Linux. On va en faire plusieurs, n'hésitez pas à diminuer la RAM (512Mo ou 1Go devraient suffire). Vous pouvez redescendre la mémoire vidéo aussi.  

➜ Si vous voyez un 🦈 c'est qu'il y a un PCAP à produire et à mettre dans votre dépôt git de rendu

➜ **L'emoji 🖥️ indique une VM à créer**. Pour chaque VM, vous déroulerez la checklist suivante :

- [x] Créer la machine (avec une carte host-only)
- [ ] Définir une IP statique à la VM
- [ ] Donner un hostname à la machine
- [ ] Vérifier que l'accès SSH fonctionnel
- [ ] Vérifier que le firewall est actif
- [ ] Remplir votre fichier `hosts`, celui de votre PC, pour accéder au VM avec un nom
- [ ] Dès que le routeur est en place, n'oubliez pas d'ajouter une route par défaut aux autres VM pour qu'elles aient internet

> Toutes les commandes pour réaliser ces opérations sont dans [le mémo Rocky](../../cours/memo/rocky_network.md). Aucune de ces étapes ne doit figurer dan le rendu, c'est juste la mise en place de votre environnement de travail.

# I. First steps

Faites-vous un petit top 5 des applications que vous utilisez sur votre PC souvent, des applications qui utilisent le réseau : un site que vous visitez souvent, un jeu en ligne, Spotify, j'sais po moi, n'importe.

🌞 **Déterminez, pour ces 5 applications, si c'est du TCP ou de l'UDP**

🌞 **Demandez l'avis à votre OS**

## Battle.net
```
Ip dst: 37.244.28.21
port dst: 53431
port src: 1119
netstat: 
C:\Users\darkj> netstat -b -n

Connexions actives

  Proto  Adresse locale         Adresse distante       État
  TCP    10.33.16.168:1119     37.244.28.21:53431    ESTABLISHED
```
[TCP_Battle.net](tcp_battle.net.pcapng)

## Discord
```
Ip dst: 162.159.135.234
port dst: 443
port src: 61933
netstat: 
C:\Users\darkj> netstat -b -n

Connexions actives

  Proto  Adresse locale         Adresse distante       État
  TCP    10.33.16.168:61933     162.159.135.234:443    ESTABLISHED
```
[TCP_Discord](tcp_discord.pcapng)

## Minecraft
``` 
Ip dst: 20.123.104.105
port dst: 443
port src: 56514
netstat: 
C:\Users\darkj> netstat -n

Connexions actives

  Proto  Adresse locale         Adresse distante       État
  TCP    10.33.16.168:56514     20.123.104.105:443    ESTABLISHED
```
[TCP_Minecraft](tcp_minecraft.pcapng)

## Soundcloud
```
Ip dst: 52.222.158.50
port dst: 443
port src: 51782
netstat: 
C:\Users\darkj> netstat -b -n

Connexions actives

  Proto  Adresse locale         Adresse distante       État
  TCP    10.33.16.168:51782     52.222.158.50:443      ESTABLISHED
```
[TCP_Soundcloud](udp_Soundcloud.pcapng)

## PokeMMO
```
Ip dst: 8.8.8.8
port dst: 53
port src: 63438
netstat: 
C:\Users\darkj> netstat -b -n
"pas de résultat udp"
```
[UDP_PokeMMO](udp_PokeMMO.pcapng)

🦈🦈🦈🦈🦈 **Bah ouais, captures Wireshark à l'appui évidemment.** Une capture pour chaque application, qui met bien en évidence le trafic en question.

# II. Mise en place

## 1. SSH

🖥️ **Machine `node1.tp4.b1`**

- n'oubliez pas de dérouler la checklist (voir [les prérequis du TP](#0-prérequis))
- donnez lui l'adresse IP `10.4.1.11/24`

Connectez-vous en SSH à votre VM.

🌞 **Examinez le trafic dans Wireshark**

[TCP_SSH]()

🌞 **Demandez aux OS**

```
C:\Windows\system32> netstat -b -n

Connexions actives

  Proto  Adresse locale         Adresse distante       État
  TCP    10.4.1.1:64271         10.4.1.11:22           ESTABLISHED
```

🦈 **Je veux une capture clean avec le 3-way handshake, un peu de trafic au milieu et une fin de connexion**

# III. DNS

## 2. Setup

🌞 **Dans le rendu, je veux**

- un `cat` des fichiers de conf
- un `systemctl status named` qui prouve que le service tourne bien
- une commande `ss` qui prouve que le service écoute bien sur un port
```
[murci@node1 ~]$ sudo cat /etc/named.conf
//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

options {
        listen-on port 53 { 127.0.0.1; any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        secroots-file   "/var/named/data/named.secroots";
        recursing-file  "/var/named/data/named.recursing";
        allow-query     { localhost; any; };
        allow-query-cache { localhost; any; };

        /*
         - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.
         - If you are building a RECURSIVE (caching) DNS server, you need to enable
           recursion.
         - If your recursive DNS server has a public IP address, you MUST enable access
           control to limit queries to your legitimate users. Failing to do so will
           cause your server to become part of large scale DNS amplification
           attacks. Implementing BCP38 within your network would greatly
           reduce such attack surface
        */
        recursion yes;

        dnssec-validation yes;

        managed-keys-directory "/var/named/dynamic";
        geoip-directory "/usr/share/GeoIP";

        pid-file "/run/named/named.pid";
        session-keyfile "/run/named/session.key";

        /* https://fedoraproject.org/wiki/Changes/CryptoPolicy */
        include "/etc/crypto-policies/back-ends/bind.config";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "tp4.b1" IN {
     type master;
     file "tp4.b1.db";
     allow-update { none; };
     allow-query {any; };
};

include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";

zone "1.4.10.in-addr.arpa" IN {
     type master;
     file "tp4.b1.rev";
     allow-update { none; };
     allow-query { any; };
};
```

```
[murci@node1 ~]$ sudo cat /var/named/tp4.b1.db
$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

; Enregistrements DNS pour faire correspondre des noms à des IPs
dns-server IN A 10.4.1.201
node1      IN A 10.4.1.11
```
```
[murci@node1 ~]$ sudo cat /var/named/tp4.b1.rev
$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

;Reverse lookup for Name Server
201 IN PTR dns-server.tp4.b1.
11 IN PTR node1.tp4.b1.
```

```
[murci@node1 ~]$ sudo systemctl status named
● named.service - Berkeley Internet Name Domain (DNS)
     Loaded: loaded (/usr/lib/systemd/system/named.service; enabled; vendor preset: disabled)
     Active: active (running) since Thu 2022-10-27 11:52:08 CEST; 1min 27s ago
   Main PID: 11283 (named)
      Tasks: 5 (limit: 5907)
     Memory: 16.2M
        CPU: 45ms
     CGroup: /system.slice/named.service
             └─11283 /usr/sbin/named -u named -c /etc/named.conf

Oct 27 11:52:08 node1.tp4.b1 named[11283]: network unreachable resolving './NS/IN': 2001:500:2d::d#>
Oct 27 11:52:08 node1.tp4.b1 named[11283]: zone tp4.b1/IN: loaded serial 2019061800
Oct 27 11:52:08 node1.tp4.b1 named[11283]: zone 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0>
Oct 27 11:52:08 node1.tp4.b1 named[11283]: zone localhost.localdomain/IN: loaded serial 0
Oct 27 11:52:08 node1.tp4.b1 named[11283]: zone localhost/IN: loaded serial 0
Oct 27 11:52:08 node1.tp4.b1 named[11283]: all zones loaded
Oct 27 11:52:08 node1.tp4.b1 systemd[1]: Started Berkeley Internet Name Domain (DNS).
Oct 27 11:52:08 node1.tp4.b1 named[11283]: running
Oct 27 11:52:08 node1.tp4.b1 named[11283]: managed-keys-zone: Initializing automatic trust anchor m>
Oct 27 11:52:08 node1.tp4.b1 named[11283]: resolver priming query complete
```

```
[murci@node1 ~]$ ss -alntp
State      Recv-Q     Send-Q         Local Address:Port           Peer Address:Port     Process
LISTEN     0          10                10.4.1.201:53                  0.0.0.0:*
```

🌞 **Ouvrez le bon port dans le firewall**

- grâce à la commande `ss` vous devrez avoir repéré sur quel port tourne le service
  - vous l'avez écrit dans la conf aussi toute façon :)
- ouvrez ce port dans le firewall de la machine `dns-server.tp4.b1` (voir le mémo réseau Rocky)

```
[murci@node1 ~]$ sudo firewall-cmd --list-all
  ports: 53/udp
```

## 3. Test

🌞 **Sur la machine `node1.tp4.b1`**

- configurez la machine pour qu'elle utilise votre serveur DNS quand elle a besoin de résoudre des noms

```
[murci@node1 ~]$ sudo cat /etc/resolv.conf
nameserver 10.4.1.201
```

- assurez vous que vous pouvez :
  - résoudre des noms comme `node1.tp4.b1` et `dns-server.tp4.b1`

```
[murci@node1 ~]$ dig node1.tp4.b1

; <<>> DiG 9.16.23-RH <<>> node1.tp4.b1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 5616
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 849d68f46027d60201000000635a5b81bac411d0c249cd99 (good)
;; QUESTION SECTION:
;node1.tp4.b1.                  IN      A

;; ANSWER SECTION:
node1.tp4.b1.           86400   IN      A       10.4.1.11

;; Query time: 3 msec
;; SERVER: 10.4.1.201#53(10.4.1.201)
;; WHEN: Thu Oct 27 12:20:48 CEST 2022
;; MSG SIZE  rcvd: 85

[murci@node1 ~]$ dig dns-server.tp4.b1

; <<>> DiG 9.16.23-RH <<>> dns-server.tp4.b1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 55639
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 0057cc7e9808a0d701000000635a5b0ea240e05eb5838564 (good)
;; QUESTION SECTION:
;dns-server.tp4.b1.             IN      A

;; ANSWER SECTION:
dns-server.tp4.b1.      86400   IN      A       10.4.1.201

;; Query time: 2 msec
;; SERVER: 10.4.1.201#53(10.4.1.201)
;; WHEN: Thu Oct 27 12:18:54 CEST 2022
;; MSG SIZE  rcvd: 90
```

  - mais aussi des noms comme `www.google.com`

```
[murci@node1 ~]$ dig www.google.com

; <<>> DiG 9.16.23-RH <<>> www.google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 30115
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 030762852b798f5101000000635a5bad644dbbe3e558cd31 (good)
;; QUESTION SECTION:
;www.google.com.                        IN      A

;; ANSWER SECTION:
www.google.com.         300     IN      A       142.250.179.100

;; Query time: 312 msec
;; SERVER: 10.4.1.201#53(10.4.1.201)
;; WHEN: Thu Oct 27 12:21:32 CEST 2022
;; MSG SIZE  rcvd: 87
```

🌞 **Sur votre PC**

- utilisez une commande pour résoudre le nom `node1.tp4.b1` en utilisant `10.4.1.201` comme serveur DNS

```
PS C:\Users\darkj> nslookup node1.tp4.b1 10.4.1.201
Serveur :   dns-server.tp4.b1
Address:  10.4.1.201

Nom :    node1.tp4.b1
Address:  10.4.1.11
```
[DNS_request_node1](dns_node1.pcapng)

> Le fait que votre serveur DNS puisse résoudre un nom comme `www.google.com`, ça s'appelle la récursivité et c'est activé avec la ligne `recursion yes;` dans le fichier de conf.

🦈 **Capture d'une requête DNS vers le nom `node1.tp4.b1` ainsi que la réponse**