# TP1 : Maîtrise réseau du poste

Pour ce TP, on va utiliser **uniquement votre poste** (pas de VM, rien, quedal, quetchi).

Le but du TP : se remettre dans le bain tranquillement en manipulant pas mal de concepts qu'on a vu l'an dernier.

C'est un premier TP *chill*, qui vous(ré)apprend à maîtriser votre poste en ce qui concerne le réseau. Faites le seul ou avec votre mate préféré bien sûr, mais jouez le jeu, faites vos propres recherches.

La "difficulté" va crescendo au fil du TP, mais la solution tombe très vite avec une ptite recherche Google si vos connaissances de l'an dernier deviennent floues.

- [TP1 : Maîtrise réseau du poste](#tp1--maîtrise-réseau-du-poste)
- [I. Basics](#i-basics)
- [II. Go further](#ii-go-further)
- [III. Le requin](#iii-le-requin)

# I. Basics

> Tout est à faire en ligne de commande, sauf si précision contraire.

☀️ **Carte réseau WiFi**

Déterminer...

- l'adresse MAC de votre carte WiFi

```
PS C:\Users\darkj> ipconfig /all

Carte réseau sans fil Wi-Fi :
   
   Adresse physique . . . . . . . . . . . : 82-30-BF-B6-57-2F
   
```

- l'adresse IP de votre carte WiFi

```
PS C:\Users\darkj> ipconfig /all

Carte réseau sans fil Wi-Fi :
   Adresse IPv4. . . . . . . . . . . . . .: 10.33.76.195(préféré)
   
```

- le masque de sous-réseau du réseau LAN auquel vous êtes connectés en WiFi
  - en notation CIDR, par exemple `/16`
    ```
    (fait sur https://www.site24x7.com/fr/tools/ipv4-sous-reseau-calculatrice.html)
    10.33.64.0/20
    ```
  - ET en notation décimale, par exemple `255.255.0.0`
    ```
    PS C:\Users\darkj> ipconfig /all

    Carte réseau sans fil Wi-Fi :
        Masque de sous-réseau. . . . . . . . . : 255.255.240.0
    ```



---

☀️ **Déso pas déso**

Pas besoin d'un terminal là, juste une feuille, ou votre tête, ou un tool qui calcule tout hihi. Déterminer...

- l'adresse de réseau du LAN auquel vous êtes connectés en WiFi

```
10.33.64.0
```

- l'adresse de broadcast

```
10.33.79.255
```

- le nombre d'adresses IP disponibles dans ce réseau

```
4096
```

---

☀️ **Hostname**

- déterminer le hostname de votre PC

```
PS C:\Users\darkj> hostname
LAPTOP-7TICS219
```

---

☀️ **Passerelle du réseau**

Déterminer...

- l'adresse IP de la passerelle du réseau

```
PS C:\Users\darkj> ipconfig
Carte réseau sans fil Wi-Fi :

   Passerelle par défaut. . . . . . . . . : 10.33.79.254

```

- l'adresse MAC de la passerelle du réseau

```
PS C:\Users\darkj> arp -a 10.33.79.254

Interface : 10.33.76.195 --- 0x16
  Adresse Internet      Adresse physique      Type
  10.33.79.254          7c-5a-1c-d3-d8-76     dynamique
```

---

☀️ **Serveur DHCP et DNS**

Déterminer...

- l'adresse IP du serveur DHCP qui vous a filé une IP

```
PS C:\Users\darkj> ipconfig
Carte réseau sans fil Wi-Fi :
   
   Serveur DHCP . . . . . . . . . . . . . : 10.33.79.254
```

- l'adresse IP du serveur DNS que vous utilisez quand vous allez sur internet

```
PS C:\Users\darkj> ipconfig
Carte réseau sans fil Wi-Fi :
   
   Serveurs DNS. . .  . . . . . . . . . . : 8.8.8.8
                                       1.1.1.1
```

---

☀️ **Table de routage**

Déterminer...

- dans votre table de routage, laquelle est la route par défaut

```
PS C:\Users\darkj> netstat -r
    IPv4 Table de routage
    ===========================================================================
    Itinéraires actifs :
    Destination réseau    Masque réseau  Adr. passerelle   Adr. interface Métrique
            0.0.0.0          0.0.0.0     10.33.79.254     10.33.76.195     35
```

---

# II. Go further

---

☀️ **Hosts ?**

- faites en sorte que pour votre PC, le nom `b2.hello.vous` corresponde à l'IP `1.1.1.1`
- prouvez avec un `ping b2.hello.vous` que ça ping bien `1.1.1.1`

```
PS C:\Users\darkj> ping b2.hello.vous

Envoi d’une requête 'ping' sur b2.hello.vous [1.1.1.1] avec 32 octets de données :
Réponse de 1.1.1.1 : octets=32 temps=14 ms TTL=57
Réponse de 1.1.1.1 : octets=32 temps=15 ms TTL=57
Réponse de 1.1.1.1 : octets=32 temps=11 ms TTL=57
Réponse de 1.1.1.1 : octets=32 temps=11 ms TTL=57

Statistiques Ping pour 1.1.1.1:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 11ms, Maximum = 15ms, Moyenne = 12ms
```

---

☀️ **Go mater une vidéo youtube et déterminer, pendant qu'elle tourne...**

```
PS C:\Users\darkj> netstat -a -n -b
 [msedge.exe]
  TCP    192.168.1.28:54537     192.229.221.95:80      TIME_WAIT
  TCP    192.168.1.28:54538     20.223.46.67:443       TIME_WAIT
  TCP    192.168.1.28:54541     13.107.246.42:443      ESTABLISHED
```


- l'adresse IP du serveur auquel vous êtes connectés pour regarder la vidéo

```
13.107.246.42
```

- le port du serveur auquel vous êtes connectés

```
443
```

- le port que votre PC a ouvert en local pour se connecter au port du serveur distant

```
54541
```

---

☀️ **Requêtes DNS**

Déterminer...

- à quelle adresse IP correspond le nom de domaine `www.ynov.com`

> Ca s'appelle faire un "lookup DNS".

```
PS C:\Users\darkj> nslookup www.ynov.com
Serveur :   dns.google
Address:  8.8.8.8

Réponse ne faisant pas autorité :
Nom :    www.ynov.com
Addresses:  2606:4700:20::ac43:4ae2
          2606:4700:20::681a:ae9
          2606:4700:20::681a:be9
          172.67.74.226
          104.26.11.233
          104.26.10.233
```

- à quel nom de domaine correspond l'IP `x`

> Ca s'appelle faire un "reverse lookup DNS".

```
PS C:\Users\darkj> nslookup 174.43.238.89
Serveur :   dns.google
Address:  8.8.8.8

Nom :    89.sub-174-43-238.myvzw.com
Address:  174.43.238.89
```

---

☀️ **Hop hop hop**

Déterminer...

- par combien de machines vos paquets passent quand vous essayez de joindre `www.ynov.com`

```
PS C:\Users\darkj> tracert www.ynov.com

Détermination de l’itinéraire vers www.ynov.com [104.26.10.233]
avec un maximum de 30 sauts :

  1    <1 ms     8 ms    <1 ms  box [192.168.1.1]
  2     6 ms     5 ms     5 ms  1.57.25.109.rev.sfr.net [109.25.57.1]
  3     6 ms     5 ms     6 ms  97.186.96.84.rev.sfr.net [84.96.186.97]
  4    13 ms    13 ms    13 ms  68.150.6.194.rev.sfr.net [194.6.150.68]
  5    13 ms    13 ms    13 ms  68.150.6.194.rev.sfr.net [194.6.150.68]
  6    13 ms    13 ms    13 ms  141.101.67.48
  7    14 ms    13 ms    14 ms  172.71.124.4
  8    14 ms    14 ms    14 ms  104.26.10.233

Itinéraire déterminé.
```

---

☀️ **IP publique**

Déterminer...

- l'adresse IP publique de la passerelle du réseau (le routeur d'YNOV donc si vous êtes dans les locaux d'YNOV quand vous faites le TP)

```
PS C:\Users\darkj> tracert 8.8.8.8

Détermination de l’itinéraire vers dns.google [8.8.8.8]
avec un maximum de 30 sauts :

  1    <1 ms    <1 ms    <1 ms  box [192.168.1.1]
```

---

☀️ **Scan réseau**

Déterminer...

- combien il y a de machines dans le LAN auquel vous êtes connectés

```
PS C:\Users\darkj> arp -a

Interface : 192.168.1.28 --- 0x8
  Adresse Internet      Adresse physique      Type
  192.168.1.1           e4-5d-51-cd-01-f0     dynamique
  192.168.1.255         ff-ff-ff-ff-ff-ff     statique
  224.0.0.2             01-00-5e-00-00-02     statique
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.0.251           01-00-5e-00-00-fb     statique
  224.0.0.252           01-00-5e-00-00-fc     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique
  255.255.255.255       ff-ff-ff-ff-ff-ff     statique
```

# III. Le requin

Faites chauffer Wireshark. Pour chaque point, je veux que vous me livrez une capture Wireshark, format `.pcap` donc.

Faites *clean* 🧹, vous êtes des grands now :

- livrez moi des captures réseau avec uniquement ce que je demande et pas 40000 autres paquets autour
  - vous pouvez sélectionner seulement certains paquets quand vous enregistrez la capture dans Wireshark
- stockez les fichiers `.pcap` dans le dépôt git et côté rendu Markdown, vous me faites un lien vers le fichier, c'est cette syntaxe :

```markdown
[Lien vers capture ARP](./captures/arp.pcap)
```

---

☀️ **Capture ARP**

- 📁 fichier `arp.pcap`
- capturez un échange ARP entre votre PC et la passerelle du réseau

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

```
filtre arp utilisé
```

[ARP.pcap](/B2_2023/fichier/ARP_Tp2_Reseau_2023.pcapng)


---

☀️ **Capture DNS**

- 📁 fichier `dns.pcap`
- capturez une requête DNS vers le domaine de votre choix et la réponse
- vous effectuerez la requête DNS en ligne de commande

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

```
filtre dns utilisé
```

[DNS.pcap](/B2_2023/fichier/DNS_Tp2_Reseau_2023.pcapng)

---

☀️ **Capture TCP**

- 📁 fichier `tcp.pcap`
- effectuez une connexion qui sollicite le protocole TCP
- je veux voir dans la capture :
  - un 3-way handshake
  - un peu de trafic
  - la fin de la connexion TCP

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

```
filtre tcp utilisé
```

[TCP.pcap](/B2_2023/fichier/TCP_Tp2_Reseau_2023.pcapng)

