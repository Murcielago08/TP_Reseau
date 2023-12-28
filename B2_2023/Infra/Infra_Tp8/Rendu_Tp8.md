# TP8 INFRA : Make ur own

Dans ce TP on va encore monter d'un cran : on se met (presque) en situation réelle : vous êtes des admins réseau que je prends en presta pour ma boîte fictive.

J'ai actuellement un réseau foireux, et j'aimerai voir ce que me proposerait pour nouvelle architecture un prestataire externe.

> *"Presque" en situation réelle car on ne s'occupe ni de l'aspect pécunier (on va pas estimer la valeur de l'archi, ce ne sera pas un critère), ni de l'aspect physique (on suppose que les différents locaux de la boîte sont directement connectés, on omet la couche internet). De plus, pour la simplicité de l'exercice, on va considérer que chaque machine est physique. Dans un environnement réel, les serveurs sont des machines virtuelles.*

![Net engineer](./img/net_engineer.jpg)

## Sommaire

- [TP8 INFRA : Make ur own](#tp8-infra--make-ur-own)
  - [Sommaire](#sommaire)
  - [I. Expression du besoin](#i-expression-du-besoin)
    - [1. Ptite intro](#1-ptite-intro)
    - [2. Présentation des équipes](#2-présentation-des-équipes)
    - [3. Equipements connectés](#3-equipements-connectés)
    - [4. Salle serveur](#4-salle-serveur)
    - [5. Exigences diverses](#5-exigences-diverses)
    - [6. Considérations spécifiques pour le TP](#6-considérations-spécifiques-pour-le-tp)
  - [II. Rendu attendu](#ii-rendu-attendu)
    - [A. Tableau d'adressage 🍷 Site "Meow Origins"](#a-tableau-dadressage--site-meow-origins)
    - [B. Tableau des VLANs 🍷 Site "Meow Origins"](#b-tableau-des-vlans--site-meow-origins)
    - [C. Tableau d'adressage 🚀 Site "Meow and Beyond"](#c-tableau-dadressage--site-meow-and-beyond)
    - [D. Tableau des VLANs 🚀 Site "Meow and Beyond"](#d-tableau-des-vlans--site-meow-and-beyond)

## I. Expression du besoin

### 1. Ptite intro

Salu moa c it4 et j'suis patron d'une tite boîte de développeurs "Meow Corporation".

On a plusieurs clients et on développe pour eux des apps assez différentes. En ce moment, les équipes développent deux trucs :

- 🌙 **Walking on the Moon**
  - une application web pour gérer des itinéraires de randonnée sur la Lune
  - c'est dév en PHP
  - comment ça j'ai une obsession pour l'espace ? *Giant steps are what you take...*
- 🐑 **Sheeps On Orbit**
  - une application web pour gérer des troupeaux de moutons en orbite terrestre
  - c'est dév en Python
  - c'est stylé d'envoyer des moutons en orbite


![Space sheeps](./img/space_sheeps.jpg)

On s'apprête aussi à décrocher des nouveaux contrats pour dév des nouveaux trucs.

---

On est répartis sur deux sites physiques en France (ou pas) :

- 🍷 **le site "Meow Origins"**
  - locaux à Bordeaux
  - 1 seul bâtiment, 3 étages et un sous-sol
  - y'a une salle serveur au sous-sol
  - architecture type *3-tier architecture*
- 🚀 **le site "Meow and Beyond"**
  - nouveaux locaux !
  - locaux sur la Lune
  - 2 bâtiments, pas d'étage
    - reliés en direct par un câble, ils sont collés !
  - salle serveur dans le bâtiment 1
  - architecture type *router-on-a-stick*
- les deux sites
  - sont directement connectés
  - ont tous les deux un accès direct à internet

On a une volonté de garder la maîtrise sur notre infra, alors on héberge tout en interne.

On est paranos un peu alors il n'y a pas de WiFi dans nos locaux, et on fournit nous-mêmes les postes de travail à nos utilisateurs (les dévs et autres).

### 2. Présentation des équipes

➜ 🍷 **Site "Meow Origins"**

- équipe dév
  - 7 lead devs
  - 132 dévs
  - tous répartis dans deux big open-space étage 1 et étage 2
- équipe admin
  - 1 admin réseau
  - 1 admin sys
  - 1 responsable sécu
  - tous dans l'open-space étage 2
- direction
  - 1 PDG
    - un bureau pour lui étage 2
  - 5 secrétaires/agents d'accueil
    - un bureau dédié étage 1 : ils/elles sont deux
    - rez-de-chaussée  : les 3 restant(e)s
  - 2 agents RH
    - un bureau dédié étage 2

➜ 🚀 **Site "Meow and Beyond"**

- équipe dév
  - 2 lead devs
  - 12 dévs
  - tous dans un open-space dans le bâtiment 2
- équipe admin
  - 1 admin réseau
  - 1 admin sys
  - tous dans un bureau dans le bâtiment 1
- direction
  - 2 secrétaires/agents d'accueil
  - dans un bureau dans le bâtiment 1

### 3. Equipements connectés

➜ **Imprimantes**

- on a une imprimante réseau à chaque étage de chaque bâtiment

➜ **Caméras**

- 2 caméras à chaque étage de chaque bâtiment
- 1 caméra à l'entrée de chaque bâtiment

➜ **Télés**

- 2 télés à l'accueil de chaque bâtiment
- 1 télé à chaque étage hors rez-de-chaussée de chaque bâtiment

➜ **Téléphone IP**

- 1 téléphone IP par employé

### 4. Salle serveur

➜ 🍷 **Site "Meow Origins"**

- serveur DHCP
  - donne des IP à tous les réseaux de clients
  - pas les serveurs/routeurs, etc. (évidemment ! :D)
- serveur DNS
  - permet de résoudre les noms de TOUTES les machines des deux sites
  - notre domaine c'est `dev.meow`
    - par exemple notre serveur DNS c'est `dns.dev.meow`
- plateforme de production
- plateforme de tests
- dépôts git internes
- accès internet
- accès à l'autre site

➜ 🚀 **Site "Meow and Beyond"**

- serveur DHCP
  - donne des IP à tous les réseaux de clients
  - pas les serveurs/routeurs, etc. (évidemment ! :D)
- plateforme de tests
- accès internet
- accès à l'autre site

### 5. Exigences diverses

➜ **Plateforme de test**

- nous avons l'habitude de fournir aux dévs une plateforme de test
- c'est à dire un réseau qui héberge des machines dédiées aux tests des dévs
- ils peuvent se connecter à ces machines et lancer leur code
- ces machines sont (quasiment...) identiques aux machines de production
- actuellement les environnements de test comportent 30 machines
- un serveur de database est aussi présent en plus des 30 serveurs de test

➜ **Production**

- nous avons un réseau dédié qui héberge des serveurs de production
- il existe un serveur dédié à chaque application que nous développons
- en ce moment nous avons donc deux serveurs de production
- un serveur de database est aussi présent en plus, pour servir ces 2 serveurs de production

➜ **Dépôts git**

- on héberge nous-mêmes des dépôts git pour stocker le code produit en interne par nos développeurs
- on a actuellement 1 seul serveur Git hébergé sur le 🍷 **Site "Meow Origins"**

### 6. Considérations spécifiques pour le TP

➜ **Choix des OS**

- les routeurs
  - Cisco ou Rocky Linux
- les switches
  - Cisco
- serveur DHCP
  - Rocky Linux
- serveur DNS
  - Rocky Linux
- tout le reste est simulé
  - VPCS ou Rocky Linux

➜ **Les locaux**

- on considère que les deux sites sont connectés en direct avec un câble
- les deux sites disposent de leur propre accès internet
- les deux sites sont routés en direct, c'est à dire que des machines du site A peuvent ping des machines du site B
- en revanche, aucun réseau IP ni VLAN n'est partagé entre les deux sites
  - on simule une situation réelle où il y a internet entre les deux
  - pas de réseau IP dupliqué des deux côtés

## II. Rendu attendu

➜ Je vous recommande FORTEMENT de suivre la démarche suivante :

- faire un schéma réseau
  - me le soumettre
  - éventuellement l'ajuster en fonction de mes retours
- établir le tableau d'adressage IP/VLAN
- monter la topologie dans GNS
- configurer uniquement la partie L2/L3
  - c'est à dire les switches, les routeurs, accès à internet
- puis passer à la conf des serveurs Linux
  - DHCP et DNS notamment

🌞 **Schéma réseau**

➜ 🍷 **Site "Meow Origins"**

![Site Meow Origins](./img/topo_site1.png)

➜ 🚀 **Site "Meow and Beyond"**

![Site Meow and Beyond](./img/topo_site2.png)

🌞 **Tableaux d'adressage et VLAN**

### A. Tableau d'adressage 🍷 Site "Meow Origins"

| Machine - Réseau  | `10.1.10.0/24`    | `10.1.20.0/29`   | `10.1.30.0/28`    | `10.1.40.0/28`    | `10.1.50.0/28`   | `10.1.60.0/24`    | `10.1.140.0/29` |
----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `r1`       | `10.1.10.254`  | `10.1.20.254`  | `10.1.30.254`  | `10.1.40.254`  | `10.1.50.254`  | `10.1.60.254`  | `10.1.140.254`  |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `DEV` | `10.1.10.1` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `DEV1` | `10.1.10.2` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `DEV2` | `10.1.10.3` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `DEV3` | `10.1.10.4` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `AdminRes` | ❌ | `10.1.20.1` | ❌ | ❌ | ❌ | ❌ | ❌ |
| `AdminSys` | ❌ | `10.1.20.2` | ❌ | ❌ | ❌ | ❌ | ❌ |
| `ResponSec` | ❌ | `10.1.20.3` | ❌ | ❌ | ❌ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `PDG` | ❌ | ❌ | `10.1.30.1` | ❌ | ❌ | ❌ | ❌ |
| `Secré/Agent` | ❌ | ❌ | `10.1.30.2` | ❌ | ❌ | ❌ | ❌ |
| `Secré/Agent1` | ❌ | ❌ | `10.1.30.3` | ❌ | ❌ | ❌ | ❌ |
| `Secré/Agent2` | ❌ | ❌ | `10.1.30.4` | ❌ | ❌ | ❌ | ❌ |
| `Secré/Agent3` | ❌ | ❌ | `10.1.30.5` | ❌ | ❌ | ❌ | ❌ |
| `Secré/Agent4` | ❌ | ❌ | `10.1.30.6` | ❌ | ❌ | ❌ | ❌ |
| `RH` | ❌ | ❌ | `10.1.30.7` | ❌ | ❌ | ❌ | ❌ |
| `RH1` | ❌ | ❌ | `10.1.30.8` | ❌ | ❌ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `Tele` | ❌ | ❌ | ❌ | `10.1.40.1`  | ❌ | ❌ | ❌ |
| `Tele1` | ❌ | ❌ | ❌ | `10.1.40.2`  | ❌ | ❌ | ❌ |
| `Tele2` | ❌ | ❌ | ❌ | `10.1.40.3`  | ❌ | ❌ | ❌ |
| `Tele3` | ❌ | ❌ | ❌ | `10.1.40.4`  | ❌ | ❌ | ❌ |
| `Tele4` | ❌ | ❌ | ❌ | `10.1.40.5`  | ❌ | ❌ | ❌ |
| `Tele5` | ❌ | ❌ | ❌ | `10.1.40.6`  | ❌ | ❌ | ❌ |
| `Imprimante` | ❌ | ❌ | ❌ | `10.1.40.7`  | ❌ | ❌ | ❌ |
| `Imprimante1` | ❌ | ❌ | ❌ | `10.1.40.8`  | ❌ | ❌ | ❌ |
| `Imprimante2` | ❌ | ❌ | ❌ | `10.1.40.9`  | ❌ | ❌ | ❌ |
| `Imprimante3` | ❌ | ❌ | ❌ | `10.1.40.10`  | ❌ | ❌ | ❌ |
| `Imprimante4` | ❌ | ❌ | ❌ | `10.1.40.11`  | ❌ | ❌ | ❌ |
| `Cam` | ❌ | ❌ | ❌ | ❌ | `10.1.50.1`  | ❌ | ❌ |
| `Cam1` | ❌ | ❌ | ❌ | ❌ | `10.1.50.2`  | ❌ | ❌ |
| `Cam2` | ❌ | ❌ | ❌ | ❌ | `10.1.50.3`  | ❌ | ❌ |
| `Cam3` | ❌ | ❌ | ❌ | ❌ | `10.1.50.4`  | ❌ | ❌ |
| `Cam4` | ❌ | ❌ | ❌ | ❌ | `10.1.50.5`  | ❌ | ❌ |
| `Cam5` | ❌ | ❌ | ❌ | ❌ | `10.1.50.6`  | ❌ | ❌ |
| `Cam6` | ❌ | ❌ | ❌ | ❌ | `10.1.50.7`  | ❌ | ❌ |
| `Cam7` | ❌ | ❌ | ❌ | ❌ | `10.1.50.8`  | ❌ | ❌ |
| `Cam8` | ❌ | ❌ | ❌ | ❌ | `10.1.50.9` | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `Tel` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.1` | ❌ |
| `Tel1` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.2` | ❌ |
| `Tel2` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.3` | ❌ |
| `Tel3` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.4` | ❌ |
| `Tel4` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.5` | ❌ |
| `Tel5` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.6` | ❌ |
| `Tel6` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.7` | ❌ |
| `Tel7` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.8` | ❌ |
| `Tel8` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.9` | ❌ |
| `Tel9` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.10` | ❌ |
| `Tel10` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.11` | ❌ |
| `Tel11` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.12` | ❌ |
| `Tel12` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.13` | ❌ |
| `Tel13` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.14` | ❌ |
| `Tel14` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.15` | ❌ |
| `Tel21` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.60.16` | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `dhcp.tp8.site1` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.140.252` |
| `dns.tp8.site1` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | `10.1.140.251` |

### B. Tableau des VLANs 🍷 Site "Meow Origins"

- Association VLAN <> réseau IP

| VLAN              | VLAN 10 `Devs` | VLAN 20 `admins` | VLAN 30 `directions` | VLAN 40 `Imp/Télé` | VLAN 50 `Cams` | VLAN 60 `Tel IP` | VLAN 140 `DHCP/DNS`|
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| Réseau IP associé | `10.1.10.0/24`    | `10.1.20.0/29`   | `10.1.30.0/28`    | `10.1.40.0/28`    | `10.1.50.0/28`   | `10.1.60.0/24`    | `10.1.140.0/29` |

---

- Quel employée est dans quel VLAN

| Machine - VLAN | VLAN 10 `Devs` | VLAN 20 `admins` | VLAN 30 `directions` | VLAN 40 `Imp/Télé` | VLAN 50 `Cams` | VLAN 60 `Tel IP` | VLAN 140 `DHCP/DNS`|
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `DEV` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `DEV1` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `DEV2` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `DEV3` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `AdminRes` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `AdminSys` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `ResponSec` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `PDG` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Secré/Agent` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Secré/Agent1` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Secré/Agent2` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Secré/Agent3` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Secré/Agent4` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `RH` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `RH1` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `Tele` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `Tele1` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `Tele2` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `Tele3` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `Tele4` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `Tele5` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `Imprimante` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `Imprimante1` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `Imprimante2` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `Imprimante3` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `Imprimante4` | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| `Cam` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `Cam1` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `Cam2` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `Cam3` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `Cam4` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `Cam5` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `Cam6` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `Cam7` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| `Cam8` | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `Tel` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel1` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel2` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel3` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel4` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel5` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel6` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel7` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel8` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel9` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel10` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel11` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel12` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel13` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel14` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel21` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `dhcp.tp8.site1` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| `dns.tp8.site1` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

### C. Tableau d'adressage 🚀 Site "Meow and Beyond"

| Machine - Réseau  | `10.2.70.0/28`    | `10.2.80.0/29`   | `10.2.90.0/29`    | `10.2.100.0/28`    | `10.2.110.0/29`   | `10.2.120.0/27` | `10.2.130.0/30` |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `r2`       | `10.1.70.254`  | `10.1.80.254`  | `10.1.90.254`  | `10.1.100.254`  | `10.1.110.254`  | `10.1.120.254`  | `10.1.130.254`  |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `DEV4` | `10.2.70.1` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `DEV4` | `10.2.70.2` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `AdminRes1` | ❌ | `10.2.80.1` | ❌ | ❌ | ❌ | ❌ | ❌ |
| `AdminSys1` | ❌ | `10.2.80.2` | ❌ | ❌ | ❌ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `Secré/Agent5` | ❌ | ❌ | `10.2.90.1` | ❌ | ❌ | ❌ | ❌ |
| `Secré/Agent6` | ❌ | ❌ | `10.2.90.2` | ❌ | ❌ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `Tele6` | ❌ | ❌ | ❌ | `10.2.100.1`  | ❌ | ❌ | ❌ |
| `Tele7` | ❌ | ❌ | ❌ | `10.2.100.2`  | ❌ | ❌ | ❌ |
| `Tele8` | ❌ | ❌ | ❌ | `10.2.100.3`  | ❌ | ❌ | ❌ |
| `Tele9` | ❌ | ❌ | ❌ | `10.2.100.4`  | ❌ | ❌ | ❌ |
| `Tele10` | ❌ | ❌ | ❌ | `10.2.100.5`  | ❌ | ❌ | ❌ |
| `Imprimante6` | ❌ | ❌ | ❌ | `10.2.100.6`  | ❌ | ❌ | ❌ |
| `Imprimante7` | ❌ | ❌ | ❌ | `10.2.100.7`  | ❌ | ❌ | ❌ |
| `Imprimante8` | ❌ | ❌ | ❌ | `10.2.100.8`  | ❌ | ❌ | ❌ |
| `Cam9` | ❌ | ❌ | ❌ | ❌ | `10.2.110.1`  | ❌ | ❌ |
| `Cam10` | ❌ | ❌ | ❌ | ❌ | `10.2.110.2`  | ❌ | ❌ |
| `Cam11` | ❌ | ❌ | ❌ | ❌ | `10.2.110.3`  | ❌ | ❌ |
| `Cam12` | ❌ | ❌ | ❌ | ❌ | `10.2.110.4`  | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `Tel15` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.2.120.1` | ❌ |
| `Tel16` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.2.120.2` | ❌ |
| `Tel17` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.2.120.3` | ❌ |
| `Tel18` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.2.120.4` | ❌ |
| `Tel19` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.2.120.5` | ❌ |
| `Tel20` | ❌ | ❌ | ❌ | ❌ | ❌ | `10.2.120.6` | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `dhcp.tp8.site2` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | `10.2.130.252` |
### D. Tableau des VLANs 🚀 Site "Meow and Beyond"

- Association VLAN <> réseau IP

| VLAN              | VLAN 70 `Devs` | VLAN 80 `admins` | VLAN 90 `directions` | VLAN 100 `Imp/Télé` | VLAN 110 `Cams` | VLAN 120 `Tel IP` | VLAN 130 `DHCP` |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| Réseau IP associé | `10.2.70.0/28`    | `10.2.80.0/30`   | `10.2.90.0/30`    | `10.2.100.0/28`    | `10.2.110.0/29`   | `10.2.120.0/27` | `10.2.130.0/30` |

---

- Quel employée est dans quel VLAN

| Machine - VLAN | VLAN 70 `Devs` | VLAN 80 `admins` | VLAN 90 `directions` | VLAN 100 `Imp/Télé` | VLAN 110 `Cams` | VLAN 120 `Tel IP` | VLAN 130 `DHCP` |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `DEV4` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `DEV4` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `AdminRes1` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| `AdminSys1` | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `Secré/Agent5` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Secré/Agent6` | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `Tele6` | ❌ | ❌ | ❌ | ✅  | ❌ | ❌ | ❌ |
| `Tele7` | ❌ | ❌ | ❌ | ✅  | ❌ | ❌ | ❌ |
| `Tele8` | ❌ | ❌ | ❌ | ✅  | ❌ | ❌ | ❌ |
| `Tele9` | ❌ | ❌ | ❌ | ✅  | ❌ | ❌ | ❌ |
| `Tele10` | ❌ | ❌ | ❌ | ✅  | ❌ | ❌ | ❌ |
| `Imprimante6` | ❌ | ❌ | ❌ | ✅  | ❌ | ❌ | ❌ |
| `Imprimante7` | ❌ | ❌ | ❌ | ✅  | ❌ | ❌ | ❌ |
| `Imprimante8` | ❌ | ❌ | ❌ | ✅  | ❌ | ❌ | ❌ |
| `Cam9` | ❌ | ❌ | ❌ | ❌ | ✅  | ❌ | ❌ |
| `Cam10` | ❌ | ❌ | ❌ | ❌ | ✅  | ❌ | ❌ |
| `Cam11` | ❌ | ❌ | ❌ | ❌ | ✅  | ❌ | ❌ |
| `Cam12` | ❌ | ❌ | ❌ | ❌ | ✅  | ❌ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `Tel15` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel16` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel17` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel18` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel19` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| `Tel20` | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| ----------------- | ----------------- | ---------------- | ----------------- | ----------------- | ---------------- | ----------------- | ----------------- |
| `dhcp.tp8.site2` | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |


🌞 **Config de toutes les machines**

- un `show-run` pour les équipements réseau
  - routeurs et switches
- la suite des étapes pour les machines Linux
  - vous ne configurez QUE le serveur DHCP et DNS pour la partie Linux
  - le reste est simulé avec VPCS ou VM vierge (production, tests, serveur git, etc.)

[show-run switch/routeur](./show-run.md)