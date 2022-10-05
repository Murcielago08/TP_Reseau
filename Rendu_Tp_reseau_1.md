# TP1 - Premier pas réseau

# Sommaire
- [TP1 - Premier pas réseau](#tp1---premier-pas-réseau)
- [Sommaire](#sommaire)
- [I. Exploration locale en solo](#i-exploration-locale-en-solo)
  - [1. Affichage d'informations sur la pile TCP/IP locale](#1-affichage-dinformations-sur-la-pile-tcpip-locale)
    - [En ligne de commande](#en-ligne-de-commande)
    - [En graphique (GUI : Graphical User Interface)](#en-graphique-gui--graphical-user-interface)
  - [2. Modifications des informations](#2-modifications-des-informations)
    - [A. Modification d'adresse IP (part 1)](#a-modification-dadresse-ip-part-1)
- [II. Exploration locale en duo](#ii-exploration-locale-en-duo)
  - [1. Prérequis](#1-prérequis)
  - [2. Câblage](#2-câblage)
  - [Création du réseau (oupa)](#création-du-réseau-oupa)
  - [3. Modification d'adresse IP](#3-modification-dadresse-ip)
  - [4. Utilisation d'un des deux comme gateway](#4-utilisation-dun-des-deux-comme-gateway)
  - [5. Petit chat privé](#5-petit-chat-privé)
  - [6. Firewall](#6-firewall)
- [III. Manipulations d'autres outils/protocoles côté client](#iii-manipulations-dautres-outilsprotocoles-côté-client)
  - [1. DHCP](#1-dhcp)
  - [2. DNS](#2-dns)
- [IV. Wireshark](#iv-wireshark)
  - [1. Intro Wireshark](#1-intro-wireshark)
  - [2. Bonus : avant-goût TCP et UDP](#2-bonus--avant-goût-tcp-et-udp)

# I. Exploration locale en solo

## 1. Affichage d'informations sur la pile TCP/IP locale

### En ligne de commande

En utilisant la ligne de commande (CLI) de votre OS :

**🌞 Affichez les infos des cartes réseau de votre PC**

```
C:\Users>ipconfig/all
Carte réseau sans fil Wi-Fi :
   Adresse physique . . . . . . . . . . . : 80-30-49-B6-DA-5D
   Adresse IPv4. . . . . . . . . . . . . .: 10.33.16.59(préféré)
```
```
C:\Users>ipconfig/all
Carte Ethernet Ethernet :
   Adresse physique . . . . . . . . . . . : 54-05-DB-D7-F6-E3
```

**🌞 Affichez votre gateway**

```
C:\Users\darkj>ipconfig/all
Carte réseau sans fil Wi-Fi :
   Passerelle par défaut. . . . . . . . . : 10.33.19.254
   ```

**🌞 Déterminer la MAC de la passerelle**

```
C:\Users\darkj>arp -a
Interface : 10.33.16.59 --- 0xd
  10.33.19.254          00-c0-e7-e0-04-4e     dynamique
```

### En graphique (GUI : Graphical User Interface)

En utilisant l'interface graphique de votre OS :  

**🌞 Trouvez comment afficher les informations sur une carte IP (change selon l'OS)**

```
panneau de configuration > Réseau et Internet > Centre Réseau et partage > Etats de Wi-fi > Détails
```

## 2. Modifications des informations

### A. Modification d'adresse IP (part 1)  

🌞 Utilisez l'interface graphique de votre OS pour **changer d'adresse IP** :

```
panneau de configuration > Réseau et Internet > Centre Réseau et partage > Etats de Wi-fi > Propriétés de Wi-fi > Protocole Internet version 4(TCP/IPv4)
```

🌞 **Il est possible que vous perdiez l'accès internet.** Que ce soit le cas ou non, expliquez pourquoi c'est possible de perdre son accès internet en faisant cette opération.

```
Si on fait cette manipulation on peut perdre la Wi-Fi car notre adresse ip peut être non reconnu par le réseau.
```

---

- **NOTE :** si vous utilisez la même IP que quelqu'un d'autre, il se passerait la même chose qu'en vrai avec des adresses postales :
  - deux personnes habitent au même numéro dans la même rue, mais dans deux maisons différentes
  - quand une de ces personnes envoie un message, aucun problème, l'adresse du destinataire est unique, la lettre sera reçue
  - par contre, pour envoyer un message à l'une de ces deux personnes, le facteur sera dans l'impossibilité de savoir dans quelle boîte aux lettres il doit poser le message
  - ça marche à l'aller, mais pas au retour

# II. Exploration locale en duo

Owkay. Vous savez à ce stade :

- afficher les informations IP de votre machine
- modifier les informations IP de votre machine
- c'est un premier pas vers la maîtrise de votre outil de travail

On va maintenant répéter un peu ces opérations, mais en créant un réseau local de toutes pièces : entre deux PCs connectés avec un câble RJ45.

## 1. Prérequis

- deux PCs avec ports RJ45
- un câble RJ45
- **firewalls désactivés** sur les deux PCs

## 2. Câblage

Ok c'est la partie tendue. Prenez un câble. Branchez-le des deux côtés. **Bap.**

## Création du réseau (oupa)

Cette étape pourrait paraître cruciale. En réalité, elle n'existe pas à proprement parlé. On ne peut pas "créer" un réseau.

**Si une machine possède une carte réseau, et si cette carte réseau porte une adresse IP**, alors cette adresse IP se trouve dans un réseau (l'adresse de réseau). Ainsi, **le réseau existe. De fait.**  

**Donc il suffit juste de définir une adresse IP sur une carte réseau pour que le réseau existe ! Bap.**

## 3. Modification d'adresse IP

🌞 **Modifiez l'IP des deux machines pour qu'elles soient dans le même réseau**

- Si vos PCs ont un port RJ45 alors y'a une carte réseau Ethernet associée

```panneau de configuration > Réseau et Internet > Centre Réseau et partage > Etats de Ethernet > Propriétés de Ethernet > Protocole Internet version 4(TCP/IPv4)```

🌞 **Vérifier à l'aide d'une commande que votre IP a bien été changée**

```
C:\Users\darkj>ipconfig
Carte Ethernet Ethernet :

   Adresse IPv4. . . . . . . . . . . . . .: 10.10.10.1
   Masque de sous-réseau. . . . . . . . . : 255.255.255.0
```

🌞 **Vérifier que les deux machines se joignent**

- utilisez la commande `ping` pour tester la connectivité entre les deux machines

```
C:\Users\darkj>ping 10.10.10.2

Envoi d’une requête 'Ping'  10.10.10.2 avec 32 octets de données :
Réponse de 10.10.10.2 : octets=32 temps=2 ms TTL=128
Réponse de 10.10.10.2 : octets=32 temps=2 ms TTL=128
Réponse de 10.10.10.2 : octets=32 temps=3 ms TTL=128
Réponse de 10.10.10.2 : octets=32 temps=3 ms TTL=128

Statistiques Ping pour 10.10.10.2:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 2ms, Maximum = 3ms, Moyenne = 2ms
```

🌞 **Déterminer l'adresse MAC de votre correspondant**

- pour cela, affichez votre table ARP

```
C:\Users\darkj>arp -a
Interface : 10.10.10.1 --- 0x5
  Adresse Internet      Adresse physique      Type
  10.10.10.2            9c-2d-cd-5b-40-5f     dynamique
```

## 4. Utilisation d'un des deux comme gateway

---

🌞**Tester l'accès internet**

- pour tester la connectivité à internet on fait souvent des requêtes simples vers un serveur internet connu
- essayez de ping l'adresse IP `1.1.1.1`, c'est un serveur connu de CloudFlare (demandez-moi si vous comprenez pas trop la démarche)

```
C:\Users\darkj>ping 1.1.1.1

Envoi d’une requête 'Ping'  1.1.1.1 avec 32 octets de données :
Réponse de 1.1.1.1 : octets=32 temps=23 ms TTL=54
Réponse de 1.1.1.1 : octets=32 temps=23 ms TTL=54
Réponse de 1.1.1.1 : octets=32 temps=24 ms TTL=54
Réponse de 1.1.1.1 : octets=32 temps=24 ms TTL=54

Statistiques Ping pour 1.1.1.1:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 23ms, Maximum = 24ms, Moyenne = 23ms

C:\Users\darkj>ping 8.8.8.8

Envoi d’une requête 'Ping'  8.8.8.8 avec 32 octets de données :
Réponse de 8.8.8.8 : octets=32 temps=24 ms TTL=113
Réponse de 8.8.8.8 : octets=32 temps=24 ms TTL=113
Réponse de 8.8.8.8 : octets=32 temps=23 ms TTL=113
Réponse de 8.8.8.8 : octets=32 temps=24 ms TTL=113

Statistiques Ping pour 8.8.8.8:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 23ms, Maximum = 24ms, Moyenne = 23ms

C:\Users\darkj>ping google.com

Envoi d’une requête 'ping' sur google.com [142.250.179.78] avec 32 octets de données :
Réponse de 142.250.179.78 : octets=32 temps=24 ms TTL=113
Réponse de 142.250.179.78 : octets=32 temps=29 ms TTL=113
Réponse de 142.250.179.78 : octets=32 temps=23 ms TTL=113
Réponse de 142.250.179.78 : octets=32 temps=24 ms TTL=113

Statistiques Ping pour 142.250.179.78:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 23ms, Maximum = 29ms, Moyenne = 25ms

C:\Users\darkj>ping 192.168.137.1

Envoi d’une requête 'Ping'  192.168.137.1 avec 32 octets de données :
Réponse de 192.168.137.1 : octets=32 temps<1ms TTL=128
Réponse de 192.168.137.1 : octets=32 temps<1ms TTL=128
Réponse de 192.168.137.1 : octets=32 temps=1 ms TTL=128
Réponse de 192.168.137.1 : octets=32 temps<1ms TTL=128

Statistiques Ping pour 192.168.137.1:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 0ms, Maximum = 1ms, Moyenne = 0ms
```

🌞 **Prouver que la connexion Internet passe bien par l'autre PC**

- utiliser la commande `traceroute` ou `tracert` (suivant votre OS) pour bien voir que les requêtes passent par la passerelle choisie (l'autre le PC)

```
C:\Users\darkj>tracert 192.168.137.1

Détermination de l’itinéraire vers LAPTOP-7TICS219 [192.168.137.1]
avec un maximum de 30 sauts :

  1    <1 ms    <1 ms    <1 ms  LAPTOP-7TICS219 [192.168.137.1]
```

## 5. Petit chat privé

🌞 **sur le PC *serveur*** avec par exemple l'IP 192.168.1.1

- `nc.exe -l -p 8888`
  - "`netcat`, écoute sur le port numéro 8888 stp"
- il se passe rien ? Normal, faut attendre qu'un client se connecte

```
C:\Users\darkj>.\nc.exe -l -p 8888
oui
voilà
```


🌞 **sur le PC *client*** avec par exemple l'IP 192.168.1.2

- `nc.exe 192.168.1.1 8888`
  - "`netcat`, connecte toi au port 8888 de la machine 192.168.1.1 stp"
- une fois fait, vous pouvez taper des messages dans les deux sens
- appelez-moi quand ça marche ! :)
- si ça marche pas, essayez d'autres options de `netcat`

```
C:\Users\darkj>.\nc.exe 192.168.137.1 8888
voilà
oui
```

---

🌞 **Visualiser la connexion en cours**

- ouvrez un deuxième terminal pendant une session `netcat`, et utilisez la commande correspondant à votre OS pour repérer la connexion `netcat` :

```
C:\Windows\system32>netstat -a -n -b
 TCP    192.168.137.1:8888     192.168.137.2:53496    ESTABLISHED
 [nc.exe]
 ```

🌞 **Pour aller un peu plus loin**

- si vous faites un `netstat` sur le serveur AVANT que le client `netcat` se connecte, vous devriez observer que votre serveur `netcat` écoute sur toutes vos interfaces

```
C:\Windows\system32> netstat -a -n -b | Select-String 8888

  TCP    0.0.0.0:8888           0.0.0.0:0              LISTENING
```

```
C:\Windows\system32> netstat -a -n -b | Select-String 8888

  TCP    192.168.137.1:8888     0.0.0.0:0              LISTENING
```

## 6. Firewall

Toujours par 2.

Le but est de configurer votre firewall plutôt que de le désactiver

🌞 **Activez et configurez votre firewall**

- autoriser les `ping`

```
netsh advfirewall firewall add rule name="ICMP Allow incoming V4 echo request" protocol=icmpv4:8,any dir=in action=allow
```

- autoriser le traffic sur le port qu'utilise `nc`

```
ça marche sans changement ¯\_(ツ)_/¯
Normalement ça ne marcherait pas mais il y a une règle inconnue qui l'autorise.
```
  
# III. Manipulations d'autres outils/protocoles côté client

## 1. DHCP

🌞**Exploration du DHCP, depuis votre PC**

- afficher l'adresse IP du serveur DHCP du réseau WiFi YNOV

```
C:\Users\darkj> ipconfig /all
Carte réseau sans fil Wi-Fi :
   Bail obtenu. . . . . . . . . . . . . . : mardi 4 octobre 2022 13:59:47
   Bail expirant. . . . . . . . . . . . . : mercredi 5 octobre 2022 13:59:47
   Passerelle par défaut. . . . . . . . . : 10.33.19.254
   Serveur DHCP . . . . . . . . . . . . . : 10.33.19.254
```

## 2. DNS

🌞** Trouver l'adresse IP du serveur DNS que connaît votre ordinateur**

```
C:\Users> ipconfig /all
Carte réseau sans fil Wi-Fi :
Serveurs DNS. . .  . . . . . . . . . . : 8.8.8.8
                                       8.8.4.4
                                       1.1.1.1
```

🌞 Utiliser, en ligne de commande l'outil `nslookup` (Windows, MacOS) ou `dig` (GNU/Linux, MacOS) pour faire des requêtes DNS à la main

- faites un *lookup* (*lookup* = "dis moi à quelle IP se trouve tel nom de domaine")
  - pour `google.com`
  - pour `ynov.com`
  - interpréter les résultats de ces commandes
- déterminer l'adresse IP du serveur à qui vous venez d'effectuer ces requêtes

```
C:\Users\darkj> nslookup google.com
Serveur :   dns.google
Address:  8.8.8.8

Réponse ne faisant pas autorité :
Nom :    google.com
Addresses:  2a00:1450:4007:805::200e
          142.250.179.78
```
```
C:\Users\darkj> nslookup ynov.com
Serveur :   dns.google
Address:  8.8.8.8

Réponse ne faisant pas autorité :
Nom :    ynov.com
Addresses:  2606:4700:20::681a:be9
          2606:4700:20::ac43:4ae2
          2606:4700:20::681a:ae9
          172.67.74.226
          104.26.11.233
          104.26.10.233
```
3 serv pour répartir les tâches


- faites un *reverse lookup* (= "dis moi si tu connais un nom de domaine pour telle IP")
  - pour l'adresse `231.34.113.12`
  - pour l'adresse `78.34.2.17`
  - interpréter les résultats
  - *si vous vous demandez, j'ai pris des adresses random :)*

```
C:\Users\darkj> nslookup 231.34.113.12
Serveur :   dns.google
Address:  8.8.8.8

*** dns.google ne parvient pas à trouver 231.34.113.12 : Non-existent domain
```

```
C:\Users\darkj> nslookup 78.34.2.17
Serveur :   dns.google
Address:  8.8.8.8

Nom :    cable-78-34-2-17.nc.de
Address:  78.34.2.17
```


# IV. Wireshark

## 1. Intro Wireshark

🌞 Utilisez le pour observer les trames qui circulent entre vos deux carte Ethernet. Mettez en évidence :

- un `ping` entre vous et votre passerelle

![](https://i.imgur.com/Jf0ruLA.png)

- un `netcat` entre vous et votre mate, branché en RJ45

![](https://i.imgur.com/5bHn67p.png)

- une requête DNS. Identifiez dans la capture le serveur DNS à qui vous posez la question.

![](https://i.imgur.com/50r8I5y.png)

## 2. Bonus : avant-goût TCP et UDP

🌞 **Wireshark it**

- déterminez à quelle IP et quel port votre PC se connecte quand vous regardez une vidéo Youtube

![](https://i.imgur.com/KKzfvyw.png)

(pas sur de ça x))