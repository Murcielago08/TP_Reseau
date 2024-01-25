# STP

STP pour Spanning Tree Protocol permet d'éviter les boucles topologiques.

Et donc éviter qu'un réseau entier deviennent non-opérationnel. Ca paraît enviable nan ? Que ça fonctionne ?

## Sommaire

- [STP](#stp)
  - [Sommaire](#sommaire)
  - [Concept de boucle topologique](#concept-de-boucle-topologique)
  - [Concept de STP](#concept-de-stp)
  - [STP en détails](#stp-en-détails)
    - [BPDU et BID](#bpdu-et-bid)
    - [Algorithme STP](#algorithme-stp)
  - [STP algorithms](#stp-algorithms)

## Concept de boucle topologique

➜ **Pour comprendre la nécessité d'utiliser STP**, il faut s'intéresser aux problèmes de boucle réseau ou *boucle topologique*.

**Une boucle topologique au niveau L2 se produit lorsque, pour un switch, il existe plusieurs chemin pour aller à une destination donnée.**

Dans l'exemple qui suit, par exemple, SW1 peut joindre SW3 de deux façons différentes :

- en direct
- en passant par SW2

```
        +-------+
    +---+  SW2  +----+
    |   +-------+    |
    |                |
    |                |
+---+---+        +---+---+    +---+
|  SW1  +--------+  SW3  +----+PC1|
+-------+        +-------+    +---+
```

➜ **Les boucles tpoologiques amènent plusieurs problèmes**

- **risque de *broadcast storm***
  - un message en broadcast envoyé à l'un des switches sera renvoyé sur les deux autres, et ceci indéfiniment
  - le nombre de messages est en constante augmentation pendant un *broadcast storm*, les équipements finissent par ne plus fonctionner correctement du fait d'un trop grand nombre de trames à traiter
- **des *mac address tables* instables**
  - vu qu'il existe plusieurs chemins possibles pour joindre PC1, la table de SW1 sera constamment mise à jour
  - l'adresse de PC1 sera joignable en passant par une interface donnée, puis par l'autre, puis par la première de nouveau, puis la deuxième, etc.

➜ Une façon simple d'enrayer la création de boucle topologique est tout simplement de **fermer les ports de certains switches**.  

Par exemple, dans le schéma juste au dessus, on pourrait fermer le port de SW1 qui mène vers SW2. Ainsi, il n'existe plus qu'un seul chemin pour aller de SW1 à SW2 : celui qui passe par SW3

```
        +-------+
        +  SW2  +----+
        +-------+    |
                     |
                     |
+---+---+        +---+---+    +---+
|  SW1  +--------+  SW3  +----+PC1|
+-------+        +-------+    +---+
```

> **On débranche pas le câble hein**, c'est juste visuel pour le schéma. Le câble est toujours là, mais dans la conf du switch on désactive le port.

➜ OK, mais quand ? Quel switch ? Quel port ? Comment réagir à un changement de topologie ?

**Welcome to STP.**

## Concept de STP

STP (pour *Spanning Tree Protocol*) :

- **est un protocole utilisé pour éviter les *boucles topologiques***
- tourne sur les switches concernés (donc tous les switches de l'infra généralement quoi)
- envoie des messages sur toutes les interfaces actives des switches concernés, en permanence, avec une fréquence de l'ordre de quelques secondes
- crée un consensus entre tous les switches : tous les switches se mettent d'accord sur un comportement à adopter
- **évite les *boucles topologiques* en désactivant automatiquement certains ports de certains switches**

## STP en détails

### BPDU et BID

➜ Au sein d'une topologie STP, les switches sont identifiés par leur *BID*. Un *BID* est la concaténation de la priorité STP du switch et de son adresse MAC.

- chaque switch a une priorité définie par l'admin
- la plus basse priorité l'emporte
- les priorités sont des multiples de 4096
- un switch donné avec une priorité de `32768` et une interface avec une [MAC](/memo/lexique.md#mac-media-access-control) de `78:78:78:78:78:78` aura donc pour *BID* `32768787878787878` sur cette interface

➜ Les messages envoyés sur tous les ports de tous les switches sont appelés *BPDU* (*Bridge Protocol Data Unit*). Les *BPDU* de configuration contiennent les informations suivantes :

- *BID* du switch source
- *BID* du *Root Bridge* actuel

➜ **Long story short :**

- une fois qu'on a activé STP sur les switches, les switchent SPAMMENT le réseau en envoyant des BPDU
- les échanges de BPDU entre les switches leur permet de construire une map du réseau
  - genre le SW1 comprend qu'il est co en direct au SW2, etc
- les switches déterminent alors ensemble quel port désactiver sur lequel d'entre eux

### Algorithme STP

> *Les switches exécutent cet algorithme tous de leurs côtés, et échangent des infos dans des trames appelées BPDU comme vu dans la section précédente.*

➜ 1. **Election d'un *Root Bridge* (*RB*)**

- c'est genre le roi des switches
- il fait autorité
- si deux switches envoient des infos contradictoires, c'est lui qui aura raison
- celui qui a le BID le plus petit est élu *root-bridge*
  - on le choisit pas particulièrement stratégiquement (sauf conf avancée)
  - faut juste qu'il y en ait un, sinon l'algo peut péter

➜ 2. **Sur tous les autres switches, élection d'un *Root Port* (*RP*)**

- pour chacun des switches, c'est le port qui a le chemin le plus court vers le *RB*
- afin de déterminer quel est le port qui a le chemin le plus court, cela se fait en fonction de la priorité et la vitesse des liens (10M/s, 100M/s, etc)

➜ 3. **Négotiation entre les switches pour déterminer quels ports passer dans un état *Forwarding* (*FWD*)**

- cela se fait en fonction de la priorité des liens
- un port en état *FWD* est actif

➜ 4. **Tous les autres ports sont passés dans un état "Blocking" (*BLK*)**

- en fonction de la prio des liens toujours
- un port en état *BLK* est inactif

**Cet algorithme open-source garantit la création d'une topologie *loop-free*** (sans boucle topologique L2) et ainsi éviter les soucis qui y sont liés.

## STP algorithms

Il existe plusieurs variantes du protocoles STP en particulier RSTP, lui aussi open-source, qui permet d'accéder à des temps de convergence bien plus courts.  

Le temps de convergence correspond au temps que met l'infrastructure de switches à se mettre d'accord sur une nouvelle topologie STP.

Cisco a de son côté créé deux protocoles basés respectivement sur STP et RSTP mais intégrant une gestion des VLANs. On dit que ces protocoles (PVST+, PVRST+) sont *VLAN aware*.
