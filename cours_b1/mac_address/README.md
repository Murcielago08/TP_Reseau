# Adresses MAC

- [Adresses MAC](#adresses-mac)
- [I. C koa](#i-c-koa)
- [II. A koa sa sert](#ii-a-koa-sa-sert)

# I. C koa

> *Une adresse MAC porte aussi le nom de "adresse physique" ou "physical address" en anglais. MAC c'est pour Mandatory Access Control.*

L'adresse MAC est une adresse qui est **gravée physiquement** sur chaque carte réseau du monde.  
**Chaque carte réseau a une et une seule adresse MAC.** On ne peut pas la modifier.

Chaque adresse MAC est **unique**.

> Que ce soit une carte réseau filaire Ethernet, ou une carte réseau WiFi, ou une carte bluetooth, ou une carte 4G, peu importe. Qu'elle soit dans un PC, un téléphone, un frigo connecté, peu importe. Chaque carte réseau a une seule et unique adresse MAC.

Une adresse MAC est souvent représentée sous la forme de **12 caractères hexadécimal.**  
Par exemple : `D4-6D-6D-00-15-3B`. Y'a des `-` mais c'est juste pour faciliter la lecture, ils ne font pas partie de l'adresse MAC.

> L'hexadécimal, c'est le fait d'utiliser 16 caractères pour représenter des nombres. On utilise les caractères de 0 à 9 et de A à F.

On peut visualiser facilement l'adresse MAC de chaque carte réseau depuis un terminal, l'adresse MAC est signalée par des ⭐ *~~(que j'ai rajouté évidemment)~~* :

```powershell
# Pour un Windows
PS C:\Users\it4> ipconfig /all

Wireless LAN adapter Wi-Fi:

   Connection-specific DNS Suffix  . : home
   Description . . . . . . . . . . . : Intel(R) Wireless-AC 9560 160MHz
   Physical Address. . . . . . . . . : ⭐ D4-6D-6D-00-15-3B ⭐
   DHCP Enabled. . . . . . . . . . . : Yes
   Autoconfiguration Enabled . . . . : Yes
   IPv4 Address. . . . . . . . . . . : 192.168.1.29(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Lease Obtained. . . . . . . . . . : Monday, October 16, 2023 6:11:24 PM
   Lease Expires . . . . . . . . . . : Tuesday, October 17, 2023 6:11:25 PM
   Default Gateway . . . . . . . . . : 192.168.1.1
   DHCP Server . . . . . . . . . . . : 192.168.1.1
   DNS Servers . . . . . . . . . . . : 192.168.1.1
```

# II. A koa sa sert

L'adresse MAC permet de :

- être **identifié** de façon unique au sein d'un LAN
- fabriquer des **trames Ethernet** (*frame* en anglais) pour envoyer des messages aux autres membres du LAN

> L'adresse MAC de destination d'une trame doit **forcément** être celle d'une machine qui est dans le même LAN que la machine qui envoie la trame.

➜ Si on prend l'exemple de **2 PCs connectés entre eux avec un câble**, pour être dans le cas d'un LAN simpliste :

![LAN 1](./img/lan1.svg)

➜ Si **PC1 envoie un message à PC2** (un `ping` par exemple), PC1 va fabriquer une trame qui ressemblera à :

![Trame 1](./img/trame1.svg)

➜ Le **PC2 va recevoir cette trame, et se demander : "est-ce que cette trame est pour moi ?"**

Voyant que l'adresse MAC de destination est bien la sienne, il considère que la trame lui est bien destinée.

Il ouvre la trame et découvre un `ping`. Il va alors répondre au `ping` par un `pong`.

![Trame 2](./img/trame2.svg)

➜ **PC1 va procéder avec la même logique** : vérifier que la MAC destination est bien la sienne, et ouvrir le message pour découvrir le `pong`.

> Pour être plus précis : la commande `ping` envoie des paquets ICMP. Un *ICMP echo request* pour le "Ping !" et un *ICMP echo reply* pour le "Pong !" C'est un message très simple qui est utilisé pour mesurer le temps d'un aller-retour entre une IP et celui qui utilise le `ping`.
