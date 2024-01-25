# DHCP

- [DHCP](#dhcp)
  - [I. Intro](#i-intro)
  - [II. Fonctionnement de DHCP](#ii-fonctionnement-de-dhcp)
    - [1. L'échange DORA](#1-léchange-dora)
    - [2. Les options DHCP](#2-les-options-dhcp)
    - [3. DHCP spoofing](#3-dhcp-spoofing)
  - [III. Bail DHCP](#iii-bail-dhcp)

## I. Intro

*DHCP* signifie *Dynamic Host Configuration Protocl*. C'est un protocole qui permet de proposer une IP disponible à un client qui en fait la demande.

Plus concrètement, le serveur DHCP propose aux clients du réseau :

- une IP disponible au sein du LAN
- (facultatif) l'adresse de la passerelle du LAN
- (facultatif) l'adresse d'un serveur DNS utilisable

Il existe généralement un serveur DHCP dans tous les LANs du monde.  
**Tous les réseaux auxquels on se connecte et pour lesquels on ne saisit pas une IP manuellement**, ainsi qu'une adresse de passerelle et/ou de DNS, alors **il y a forcément un serveur DHCP sur le réseau.**

> Dans les réseaux de particulier, chez nous, c'est la box qui porte le serveur DHCP.

## II. Fonctionnement de DHCP

### 1. L'échange DORA

Considérons un client qui arrive dans un LAN dans lequel il ne s'est jamais connecté pour la suite.

**L'échange DHCP consiste en 4 trames (DORA) :**

- ***Discover*** : permet au client de trouver le serveur DHCP au sein du LAN, s'il y en a un
- ***Offer*** : le serveur propose une IP au client
- ***Request*** : le client accepte cette IP, et valide l'échange
- ***Acknowledge*** : le serveur valide à son tour l'échange

La trame *Discover* a pour particularité d'avoir **`ff:ff:ff:ff:ff` pour MAC de destination** : l'adresse de broadcast.  
Ainsi, toutes les machines du LAN recevront cette trame *Discover*.  
Le serveur DHCP du réseau pourra alors continuer l'échange en répondant directement au client (en utilisant la MAC du client qu'il connaît désormais) avec un *Offer*.

### 2. Les options DHCP

Un serveur DHCP peut aussi proposer au client, en plus d'une IP disponible au sein du LAN, d'autres informations qui pourrait lui être utile.

Ainsi, dans la plupart des cas, le serveur DHCP donnera au moins deux autres informations aux clients :

- l'adresse IP de la passerelle du réseau
- l'addrese IP d'un serveur DNS joignable depuis le LAN

Ces deux informations permettront au client d'avoir un accès internet normal.

Ces informations supplémentaires que peut proposer le DHCP à ses clients sont appelées **options DHCP**.

> Il est aisé de visualiser ces options DHCP dans le ***Offer*** du serveur en lançant un p'tit Wireshark.

### 3. DHCP spoofing

Il existe une attaque liée au fonctionnement du protocole DHCP appelée "DHCP spoofing".

En effet, puisque tout le monde reçoit le *Discover*, un hacker pourrait répondre au client à la place du serveur DHCP. Dans ce cas, c'est le hacker qui choisit quelle IP il donne au client, ainsi que les adresses IP de la passerelle et du serveur DNS que le client utilisera.

Evidemment, le hacker donnera au client sa propre IP pour IP de passerelle et de DNS. Ainsi, le client utilisera le hacker comme passerelle et serveur DNS : le hacker sera en man-in-the-middle entre le client et le reste du monde.

## III. Bail DHCP

Un ***bail DHCP*** est un fichier texte qui est créé sur le serveur DHCP **ET** sur le client qui reçoit une IP : chacun crée son *bail DHCP*.  

Le fichier est créé juste après un échange DORA. Ce *bail* permet de stocker les informations obtenues par les deux parties lors de l'échange DHCP.

Le serveur DHCP stocke notamment dans son *bail* :

- adresse IP donnée au client
- adresse MAC du client
- date à laquelle le *bail* a été délivré
- durée de vie du *bail*

Le client stocke notamment dans son *bail* :

- adresse IP du serveur DHCP de ce LAN
- date à laquelle le *bail* a été délivré
- durée de vie du *bail*

➜ Le *bail DHCP* du client contient aussi l'adresse IP du serveur DHCP, afin qu'il s'en souvienne dans le cas de connexions ultérieures.

➜ Le *bail DHCP* du serveur contient la MAC du client. Ainsi, si le client revient ultérieurement sur le réseau, le serveur pourra lui donner la même IP que lors de sa première connexion.

➜ Un *bail DHCP* a une durée de vie. A l'issue de cette durée de vie, le client effectuera de nouveau l'échange DHCP avec le serveur.
