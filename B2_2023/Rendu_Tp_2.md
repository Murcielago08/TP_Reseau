# TP2 : Environnement virtuel

Dans ce TP, on remanipule toujours les mêmes concepts qu'au TP1, mais en environnement virtuel avec une posture un peu plus orientée administrateur qu'au TP1.

- [TP2 : Environnement virtuel](#tp2--environnement-virtuel)
- [I. Topologie réseau](#i-topologie-réseau)
  - [Topologie](#topologie)
  - [Tableau d'adressage](#tableau-dadressage)
  - [Hints](#hints)
  - [Marche à suivre recommandée](#marche-à-suivre-recommandée)
  - [Compte-rendu](#compte-rendu)
- [II. Interlude accès internet](#ii-interlude-accès-internet)
- [III. Services réseau](#iii-services-réseau)
  - [1. DHCP](#1-dhcp)
  - [2. Web web web](#2-web-web-web)


# I. Topologie réseau

Vous allez dans cette première partie préparer toutes les VMs et vous assurez que leur connectivité réseau fonctionne bien.

On va donc parler essentiellement IP et routage ici.

## Topologie

![Topologie](./img/topo.png)

## Tableau d'adressage

| Node             | LAN1 `10.1.1.0/24` | LAN2 `10.1.2.0/24` |
| ---------------- | ------------------ | ------------------ |
| `node1.lan1.tp1` | `10.1.1.11`        | x                  |
| `node2.lan1.tp1` | `10.1.1.12`        | x                  |
| `node1.lan2.tp1` | x                  | `10.1.2.11`        |
| `node2.lan2.tp1` | x                  | `10.1.2.12`        |
| `router.tp1`     | `10.1.1.254`       | `10.1.2.254`       |

## Hints

➜ **Sur le `router.tp1`**

Il sera nécessaire d'**activer le routage**. Par défaut Rocky n'agit pas comme un routeur. C'est à dire que par défaut il ignore les paquets qu'il reçoit s'il l'IP de destination n'est pas la sienne. Or, c'est précisément le job d'un routeur.

> Dans notre cas, si `node1.lan1.tp1` ping `node1.lan2.tp1`, le paquet a pour IP source `10.1.1.11` et pour IP de destination `10.1.2.11`. Le paquet passe par le routeur. Le routeur reçoit donc un paquet qui a pour destination `10.1.2.11`, une IP qui n'est pas la sienne. S'il agit comme un routeur, il comprend qu'il doit retransmettre le paquet dans l'autre réseau. Par défaut, la plupart de nos OS ignorent ces paquets, car ils ne sont pas des routeurs.

Pour activer le routage donc, sur une machine Rocky :

```bash
$ firewall-cmd --add-masquerade
$ firewall-cmd --add-masquerade --permanent
$ sysctl -w net.ipv4.ip_forward=1
```

---

➜ **Les switches sont les host-only de VirtualBox pour vous**

Vous allez donc avoir besoin de créer deux réseaux host-only. Faites bien attention à connecter vos VMs au bon switch host-only.

---

➜ **Aucune carte NAT**

## Marche à suivre recommandée

Dans l'ordre, je vous recommande de :

**1.** créer les VMs dans VirtualBox (clone du patron)  
**2.** attribuer des IPs statiques à toutes les VMs  
**3.** vous connecter en SSH à toutes les VMs  
**4.** activer le routage sur `router.tp1`  
**5.** vous assurer que les membres de chaque LAN se ping, c'est à dire :

- `node1.lan1.tp1`
  - doit pouvoir ping `node2.lan1.tp1`
  - doit aussi pouvoir ping `router.tp1` (il a deux IPs ce `router.tp1`, `node1.lan1.tp1` ne peut ping que celle qui est dans son réseau : `10.1.1.254`)
- `router.tp1` ping tout le monde
- les membres du LAN2 se ping aussi

**6.** ajouter les routes statiques

- sur les deux machines du LAN1, il faut ajouter une route vers le LAN2
- sur les deux machines du LAN2, il faut ajouter une route vers le LAN1

## Compte-rendu

☀️ Sur **`node1.lan1.tp1`**

- afficher ses cartes réseau

```
[joris@node1lan1tp1 ~]$ ip -c a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:f6:4f:f9 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.11/24 brd 10.1.1.255 scope global noprefixroute enp0s3
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fef6:4ff9/64 scope link
       valid_lft forever preferred_lft forever
```

- afficher sa table de routage

```
[joris@node1lan1tp1 ~]$ ip r s
10.1.1.0/24 dev enp0s3 proto kernel scope link src 10.1.1.11 metric 100
10.1.2.0/24 via 10.1.1.254 dev enp0s3 proto static metric 100
```

- prouvez qu'il peut joindre `node2.lan2.tp2`

```
[joris@node1lan1tp1 ~]$ ping 10.1.2.11
PING 10.1.2.11 (10.1.2.11) 56(84) bytes of data.
64 bytes from 10.1.2.11: icmp_seq=1 ttl=63 time=0.501 ms
64 bytes from 10.1.2.11: icmp_seq=2 ttl=63 time=0.644 ms
64 bytes from 10.1.2.11: icmp_seq=3 ttl=63 time=0.752 ms
64 bytes from 10.1.2.11: icmp_seq=4 ttl=63 time=0.524 ms
64 bytes from 10.1.2.11: icmp_seq=5 ttl=63 time=0.904 ms
64 bytes from 10.1.2.11: icmp_seq=6 ttl=63 time=1.02 ms
--- 10.1.2.11 ping statistics ---
6 packets transmitted, 6 received, 0% packet loss, time 5077ms
rtt min/avg/max/mdev = 0.501/0.724/1.022/0.190 ms
```

- prouvez avec un `traceroute` que le paquet passe bien par `router.tp1`

```
[joris@node1lan1tp1 ~]$ traceroute 10.1.2.11
traceroute to 10.1.2.11 (10.1.2.11), 30 hops max, 60 byte packets
 1  10.1.1.254 (10.1.1.254)  0.646 ms  0.625 ms  0.561 ms
 2  10.1.2.11 (10.1.2.11)  1.919 ms !X  1.916 ms !X  1.905 ms !X
```

# II. Interlude accès internet

**On va donner accès internet à tout le monde.** Le routeur aura un accès internet, et permettra à tout le monde d'y accéder : il sera la passerelle par défaut des membres du LAN1 et des membres du LAN2.

**Ajoutez une carte NAT au routeur pour qu'il ait un accès internet.**

☀️ **Sur `router.tp1`**

- prouvez que vous avez un accès internet (ping d'une IP publique)

```
[joris@routertp1 ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=111 time=106 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=111 time=29.3 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=111 time=29.2 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=111 time=29.6 ms
^C
--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 29.171/48.520/106.055/33.218 ms
```

- prouvez que vous pouvez résoudre des noms publics (ping d'un nom de domaine public)

```
[joris@routertp1 ~]$ ping google.com
PING google.com (142.250.179.110) 56(84) bytes of data.
64 bytes from par21s20-in-f14.1e100.net (142.250.179.110): icmp_seq=1 ttl=114 time=29.0 ms
64 bytes from par21s20-in-f14.1e100.net (142.250.179.110): icmp_seq=2 ttl=114 time=32.1 ms
64 bytes from par21s20-in-f14.1e100.net (142.250.179.110): icmp_seq=3 ttl=114 time=133 ms
64 bytes from par21s20-in-f14.1e100.net (142.250.179.110): icmp_seq=4 ttl=114 time=32.3 ms
^C
--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 28.984/56.523/132.672/43.984 ms
```

☀️ **Accès internet LAN1 et LAN2**


- dans le compte-rendu, mettez-moi que la conf des points précédents sur `node2.lan1.tp1`

```
[joris@node2lan1tp1 ~]$ sudo cat /etc/sysconfig/network-scripts/ifcfg-enp0s3
[sudo] password for joris:
DEVICE=enp0s3

BOOTPROTO=static
ONBOOT=yes

IPADDR=10.1.1.11
NETMASK=255.255.255.0
GATEWAY=10.1.1.254


[joris@node2lan1tp1 ~]$ sudo cat /etc/resolv.conf
# Generated by NetworkManager
nameserver 8.8.8.8
nameserver 8.8.4.4
nameserver google.com
```

- prouvez que `node2.lan1.tp1` a un accès internet :
  - il peut ping une IP publique
  - il peut ping un nom de domaine public

```

[joris@node2lan1tp1 ~]$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=111 time=27.5 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=111 time=26.9 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=111 time=26.1 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=111 time=26.4 ms
^C
--- 8.8.8.8 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3003ms
rtt min/avg/max/mdev = 26.121/26.730/27.528/0.539 ms

[joris@node2lan1tp1 ~]$ ping google.com
PING google.com (172.217.20.174) 56(84) bytes of data.
64 bytes from waw02s07-in-f174.1e100.net (172.217.20.174): icmp_seq=1 ttl=116 time=26.7 ms
64 bytes from waw02s07-in-f174.1e100.net (172.217.20.174): icmp_seq=2 ttl=116 time=26.7 ms
64 bytes from waw02s07-in-f14.1e100.net (172.217.20.174): icmp_seq=3 ttl=116 time=26.2 ms
64 bytes from waw02s07-in-f14.1e100.net (172.217.20.174): icmp_seq=4 ttl=116 time=26.3 ms
^C
--- google.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 26.217/26.454/26.673/0.217 ms
```

# III. Services réseau

**Adresses IP et routage OK, maintenant, il s'agirait d'en faire quelque chose nan ?**

Dans cette partie, on va **monter quelques services orientés réseau** au sein de la topologie, afin de la rendre un peu utile que diable. Des machines qui se `ping` c'est rigolo mais ça sert à rien, des machines qui font des trucs c'est mieux.

## 1. DHCP


☀️ **Sur `dhcp.lan1.tp1`**

- setup du serveur DHCP
  - commande d'installation du paquet

```
[joris@dhcp ~]$ sudo dnf install dhcp-server -y
Complete!
```

  - fichier de conf

```
[joris@dhcp ~]$ sudo cat /etc/dhcp/dhcpd.conf
#
# DHCP Server Configuration file.
#   see /usr/share/doc/dhcp-server/dhcpd.conf.example
#   see dhcpd.conf(5) man page
#
default-lease-time 900;
max-lease-time 10800;

authoritative;

subnet 10.1.1.0 netmask 255.255.255.0 {
range 10.1.1.100 10.1.1.200;
option routers 10.1.1.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.1.1.1;
}
```

  - service actif

```
[joris@dhcp ~]$ sudo systemctl status sshd
● sshd.service - OpenSSH server daemon
     Loaded: loaded (/usr/lib/systemd/system/sshd.service; enabled; preset:>
     Active: active (running) since Thu 2023-10-19 18:48:15 CEST; 35min ago
       Docs: man:sshd(8)
             man:sshd_config(5)
   Main PID: 695 (sshd)
      Tasks: 1 (limit: 4604)
     Memory: 6.4M
        CPU: 79ms
     CGroup: /system.slice/sshd.service
             └─695 "sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 startups"

Oct 19 18:48:15 dhcp.lan1.tp2 systemd[1]: Starting OpenSSH server daemon...
Oct 19 18:48:15 dhcp.lan1.tp2 sshd[695]: main: sshd: ssh-rsa algorithm is d
```

☀️ **Sur `node1.lan1.tp1`**

- demandez une IP au serveur DHCP
- prouvez que vous avez bien récupéré une IP *via* le DHCP

```
[joris@node1lan1tp1 ~]$ sudo systemctl restart NetworkManager
[joris@node1lan1tp1 ~]$ ip -c a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:f6:4f:f9 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.11/24 brd 10.1.1.255 scope global noprefixroute enp0s3
       valid_lft forever preferred_lft forever
    inet 10.1.1.100/24 brd 10.1.1.255 scope global secondary dynamic noprefixroute enp0s3
       valid_lft 894sec preferred_lft 894sec
    inet6 fe80::a00:27ff:fef6:4ff9/64 scope link
       valid_lft forever preferred_lft forever
```

- prouvez que vous avez bien récupéré l'IP de la passerelle

```
[joris@node1lan1tp1 ~]$ ping 10.1.1.254
PING 10.1.1.254 (10.1.1.254) 56(84) bytes of data.
64 bytes from 10.1.1.254: icmp_seq=1 ttl=64 time=0.294 ms
64 bytes from 10.1.1.254: icmp_seq=2 ttl=64 time=0.427 ms
64 bytes from 10.1.1.254: icmp_seq=3 ttl=64 time=0.450 ms
64 bytes from 10.1.1.254: icmp_seq=4 ttl=64 time=0.434 ms
^C
--- 10.1.1.254 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3104ms
rtt min/avg/max/mdev = 0.294/0.401/0.450/0.062 ms

[joris@node1lan1tp1 ~]$ ping google.com
PING google.com (216.58.214.78) 56(84) bytes of data.
64 bytes from fra15s10-in-f78.1e100.net (216.58.214.78): icmp_seq=1 ttl=115 time=25.9 ms
64 bytes from par10s39-in-f14.1e100.net (216.58.214.78): icmp_seq=2 ttl=115 time=26.2 ms
64 bytes from fra15s10-in-f78.1e100.net (216.58.214.78): icmp_seq=3 ttl=115 time=25.7 ms
^C
--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 25.738/25.944/26.215/0.199 ms
```

- prouvez que vous pouvez `ping node1.lan2.tp1`

```
[joris@node1lan1tp1 ~]$ ping 10.1.2.11
PING 10.1.2.11 (10.1.2.11) 56(84) bytes of data.
64 bytes from 10.1.2.11: icmp_seq=1 ttl=63 time=2.58 ms
64 bytes from 10.1.2.11: icmp_seq=2 ttl=63 time=0.986 ms
64 bytes from 10.1.2.11: icmp_seq=3 ttl=63 time=0.822 ms
64 bytes from 10.1.2.11: icmp_seq=4 ttl=63 time=0.864 ms
^C
--- 10.1.2.11 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3009ms
rtt min/avg/max/mdev = 0.822/1.313/2.581/0.734 ms
```

## 2. Web web web

☀️ **Sur `web.lan2.tp1`**

- setup du service Web
  - gestion de la racine web `/var/www/site_nul/`

```
[joris@web ~]$ sudo cat /var/www/site_nul/index.html

oe le site oe
```

  - service actif

```
[joris@web ~]$ sudo systemctl status nginx
● nginx.service - The nginx HTTP and reverse proxy server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; preset>     Active: active (running) since Thu 2023-10-19 20:24:05 CEST; 3min 36s >   Main PID: 1544 (nginx)
      Tasks: 2 (limit: 4604)
     Memory: 1.9M
        CPU: 16ms
     CGroup: /system.slice/nginx.service
             ├─1544 "nginx: master process /usr/sbin/nginx"
             └─1545 "nginx: worker process"

Oct 19 20:24:05 web.lan2.tp2 systemd[1]: Starting The nginx HTTP and revers>Oct 19 20:24:05 web.lan2.tp2 nginx[1542]: nginx: the configuration file /et>Oct 19 20:24:05 web.lan2.tp2 nginx[1542]: nginx: configuration file /etc/ng>Oct 19 20:24:05 web.lan2.tp2 systemd[1]: Started The nginx HTTP and reverse>lines 1-15/15 (END)...skipping...
● nginx.service - The nginx HTTP and reverse proxy server
     Loaded: loaded (/usr/lib/systemd/system/nginx.service; enabled; preset: disabled)
     Active: active (running) since Thu 2023-10-19 20:24:05 CEST; 3min 36s ago
   Main PID: 1544 (nginx)
      Tasks: 2 (limit: 4604)
     Memory: 1.9M
        CPU: 16ms
     CGroup: /system.slice/nginx.service
             ├─1544 "nginx: master process /usr/sbin/nginx"
             └─1545 "nginx: worker process"

Oct 19 20:24:05 web.lan2.tp2 systemd[1]: Starting The nginx HTTP and reverse proxy server...
Oct 19 20:24:05 web.lan2.tp2 nginx[1542]: nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
Oct 19 20:24:05 web.lan2.tp2 nginx[1542]: nginx: configuration file /etc/nginx/nginx.conf test is successful
Oct 19 20:24:05 web.lan2.tp2 systemd[1]: Started The nginx HTTP and reverse proxy server.
```

- prouvez qu'il y a un programme NGINX qui tourne derrière le port 80 de la machine (commande `ss`)

```
[joris@web ~]$ ss -tupnl | grep 80
tcp   LISTEN 0      511          0.0.0.0:80        0.0.0.0:*
tcp   LISTEN 0      511             [::]:80           [::]:*
```

- prouvez que le firewall est bien configuré

```
[joris@web ~]$ sudo firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: enp0s3
  sources:
  services: cockpit dhcpv6-client ssh
  ports: 80/tcp
  protocols:
  forward: yes
  masquerade: no
  forward-ports:
  source-ports:
  icmp-blocks:
  rich rules:
```

☀️ **Sur `node1.lan1.tp1`**

- éditez le fichier `hosts` pour que `site_nul.tp1` pointe vers l'IP de `web.lan2.tp1`

```
[joris@node1lan1tp1 ~]$ cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
10.1.2.12 site_nul.tp1
```

- visitez le site nul avec une commande `curl` et en utilisant le nom `site_nul.tp1`

```
[joris@node1lan1tp1 ~]$ curl site_nul.tp1

oe le site oe
```