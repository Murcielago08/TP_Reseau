# Routage

- [Routage](#routage)
- [1. Concept du routage](#1-concept-du-routage)
  - [A. Intro](#a-intro)
  - [B. Table de routage](#b-table-de-routage)
  - [C. La route par défaut](#c-la-route-par-défaut)
  - [D. Commandes associéess](#d-commandes-associéess)
- [2. Mise en situation](#2-mise-en-situation)
- [3. Que fait concrètement un routeur](#3-que-fait-concrètement-un-routeur)
  - [A. Explications](#a-explications)
  - [B. Exemple](#b-exemple)
- [4. Cas de la route par défaut](#4-cas-de-la-route-par-défaut)

# 1. Concept du routage

## A. Intro

**Le routage permet à deux réseaux de communiquer.** L'équipement qui effectue le routage est appelé un ***routeur***.

Un *routeur* a pour rôle d'acheminer les paquets d'un réseau à un autre. Il fait le pont entre les deux réseaux.

S'il permet aux clients d'un réseau local (LAN) de sortir vers d'autres réseaux, on l'appelle la ***passerelle*** de ce réseau.

> Par exemple, chez vous, votre box est un routeur qui fait la passerelle entre deux réseaux : votre LAN, et internet.

## B. Table de routage

Chaque équipement (PC, routeurs, serveurs, etc.) possède une ***table de routage***. Cette *table de routage* indique à la machine les réseaux qu'elle peut joindre.

Dans une table de routage, chaque ligne est appelée une ***route***. Chaque *route* contient :

- l'adresse du réseau à joindre
- comment s'y rendre
  - soit on y est directement connecté
  - soit il faut passer par une passerelle

## C. La route par défaut

Il existe une route particulière appelée ***route par défaut***. Elle indique le chemin à prendre pour n'importe quel réseau qui n'est pas explicitement précisé dans les autres *routes* de la *table de routage*. C'est un panneau "toutes directions" quoi, clairement.

> La *route par défaut* est notée comme une *route* vers le réseau `default`, ou vers le réseau `0.0.0.0.`

## D. Commandes associéess

On peut afficher la table de routage d'un PC/serveur avec :

```bash
# Windows, MacOS et GNU/Linux
$ netstat -nr       # option -r pour "routing table"

# Windows only 
$ route print
$ route print -4    # que l'iIPv4

# GNU/Linux only
$ ip route show
$ ip r s            # same, juste plus court
```

# 2. Mise en situation

Supposons deux réseaux locaux (LAN) :

```schema
    LAN1 : 10.1.1.0/24         LAN2 : 10.2.2.0/24
+---------------------------+ +---------------------------+
|                           | |                           |
|                           | |                           |
|                           | |                           |
|                           | |                 +---+     |
|                     .254+-+-+-+               |PC2|     |
|                         |  R  |               +---+     |
|                         |     |                 .57     |
|                         +-+-+-+.254                     |
|       .13                 | |                           |
|     +---+                 | |                           |
|     |PC1|                 | |                           |
|     +---+                 | |                           |
|                           | |                           |
|                           | |                           |
|                           | |                           |
+---------------------------+ +---------------------------+
```

Réseaux :

| Nom du réseau | Adresse du réseau |
| ------------- | ----------------- |
| LAN1          | `10.1.1.0/24`     |
| LAN2          | `10.2.2.0/24`     |

Machines :

| Nom     | Adresse LAN1 | Adresse LAN2 |
| ------- | ------------ | ------------ |
| Routeur | `10.1.1.254` | `10.2.2.254` |
| PC1     | `10.1.1.13`  | x            |
| PC2     | x            | `10.2.2.57`  |

PC1 pourra parler à PC2 et réciproquement, en désignant le routeur comme leur passerelle :

- pour PC1, `10.1.1.254/24` est la passerelle vers `10.2.2.0/24`
- pour PC2, `10.2.2.254/24` est la passerelle vers `10.1.1.0/24`

---

Ces deux PCs ont donc besoin de connaître une **route** vers le réseau auquel ils ne sont pas connectés, s'ils veulent échanger des messages. C'est à dire :

- sur PC1, il faut ajouter une route vers `10.2.2.0/24` en indiquant que `10.1.1.254` est sa passerelle
- sur PC2, il faut ajouter une route vers `10.1.1.0/24` en indiquant que `10.2.2.254` est sa passerelle

---

Ici, on peut utiliser le vocabulaire suivant :

- le routeur est la passerelle de PC1 et PC2
- le routeur est la passerelle du LAN1 et du LAN2
- `10.1.1.254/24` est la passerelle du LAN1 et donc, du PC1
- `10.2.2.254/24` est la passerelle du LAN2 et donc, du PC2

# 3. Que fait concrètement un routeur

## A. Explications

Okok, mais comment le routeur opère ce changement de réseau ? Comment fait-il pour savoir acheminer la réponse au bon client dans l'autre sens (dans le cas d'un échange question/réponse comme un `ping`) ?

Le routeur connaît à la fois les adresses MAC de ses clients (les machines connectées au LAN) et les adresses IP.  
On se base sur ces principes :

- une trame qui transite sur le réseau possède une adresse MAC source et une adresse MAC de destination
- cette trame contient un paquet IP
- ce paquet IP possède une IP source et une IP de destination
- les MAC servent UNIQUEMENT à communiquer au sein d'un LAN
- les IP permettent de communiquer à travers différents réseaux
- le rôle du routeur est d'acheminer nos trames d'un LAN, vers un autre réseau

Avant de passer au schéma + exemple, on peut dire de façon simple :

- les IP source et destination ne changent JAMAIS au cours du transit du message sur le réseau
- les MAC source et destination sont modifiés A CHAQUE FOIS que le message passe par un routeur, et donc, à chaque fois que le message change de réseau

**C'est ça le rôle du routeur : changer les adresses MAC source et destination des trames** qu'on lui envoie, afin de les renvoyer dans un autre réseau.

## B. Exemple

```schema
 node1                  router                 node2
┌─────┐                ┌─────┐                ┌─────┐
│     │      10.1.1.254│     │192.168.1.254   │     │
│     ├────────────────┤     ├────────────────┤     │
└─────┘10.1.1.11       └─────┘    10.1.1.22└─────┘
```

| Machine  | Réseau 1 `10.1.1.0/24`      | Réseau 2 `10.2.2.0/24`      |
| -------- | --------------------------- | --------------------------- |
| `node1`  | MAC `11:11` IP `10.1.1.1`   | x                           |
| `router` | MAC `25:25` IP `10.1.1.254` | MAC `54:54` IP `10.2.2.254` |
| `node2`  | x                           | MAC `22:22` IP `10.2.2.2`   |

On peut déjà dire que :

- `node1` connaît une route vers `10.1.1.0/24` car il est lui même dans ce réseau
- `node2` connaît une route vers `10.2.2.0/24` car il est lui même dans ce réseau
- le `router` connaît une route vers les deux réseaux, car il est dans les deux

Pour que `node1` et `node2` puissent se joindre, il va falloir ajouter deux routes :

- une pour indiquer à `node1` qu'il peut joindre `10.2.2.0/24` en passant par `10.1.1.254`
  - on dit alors que, pour `node1`, la machine qui porte l'IP `10.1.1.254` est sa passerelle vers `10.2.2.0/24`
- une deuxième pour indiquer à `node2` qu'il peut joindre `10.1.1.0/24` en passant par `10.2.2.254`
  - on dit alors que, pour `node2`, la machine qui porte l'IP `10.2.2.254` est sa passerelle vers `10.1.1.0/24`

> On peut ajouter ces routes manuellement. Usuellement, c'est le DHCP d'un réseau qui, en plus de nous donner une adresse IP utilisable, nous indique aussi l'adresse de passerelle du réseau.

Une fois que les tables de routage de `node1` et `node2` possèdent ces nouvelles infos, ils peuvent communiquer.

---

Plaçons-nous dans la situation où `node1` tape la commande `ping 10.1.1.22`. On va lister chaque étape (en omettant l'ARP) :

**`1.`** `node1` voit que `10.2.2.2/24` est dans le réseau `10.2.2.0/24`, c'est ce réseau qu'il va essayer de joindre
**`2.`** `node1` regarde sa table de routage, et voit qu'il possède une route vers `10.2.2.0/24` et que sa passerelle pour y aller est `10.1.1.254`
**`3.`** il envoie son ping :

| MAC src | MAC dst | IP src        | IP dst        | Type de message |
| ------- | ------- | ------------- | ------------- | --------------- |
| `11:11` | `25:25` | `10.1.1.1/24` | `10.2.2.2/24` | Ping            |

**`4.`** le `router` reçoit ce message. Il le traite car il voit que la MAC dst est la sienne : ce message est pour lui  
**`5.`** il regarde le paquet IP, et voit que l'IP de destination est dans un réseau différent que l'IP source : il va procéder à l'opération de routage : il va devoir modifier la trame (changer les MAC src et MAC dst)  
**`6.`** pour savoir dans quel réseau il doit envoyer la trame, il regarde sa table de routage. Il voit qu'il est directement connecté à `10.2.2.0/24`  
**`7.`** modification de la trame par le routeur :

| MAC src | MAC dst | IP src        | IP dst        | Type de message |
| ------- | ------- | ------------- | ------------- | --------------- |
| `54:54` | `22:22` | `10.1.1.1/24` | `10.2.2.2/24` | Ping            |

> Les IPs ne changent pas.

**`8.`** il envoie ce message vers `node2`  
**`9.`** `node2` reçoit le message. Il le traite car il voit que la MAC dst est la sienne : ce message est pour lui  
**`10.`** `node2` regarde le paquet IP à l'intérieur de la trame et voit que l'IP dst est bien la sienne : ce message est vraiment pour lui  
**`11.`** `node2` ouvre le paquet IP et voit un ping, il répond avec un pong. Il crafte alors la trame suivante :

| MAC src | MAC dst | IP src        | IP dst        | Type de message |
| ------- | ------- | ------------- | ------------- | --------------- |
| `22:22` | `54:54` | `10.2.2.2/24` | `10.1.1.1/24` | Pong            |

**`12.`** `node2` envoie son message

A partir de là, les opérations de 4 à 8 vont se répéter en direction de `node1` pour qu'il reçoive le pong retour. La trame modifiée par le routeur, que `node1` recevra, sera :

| MAC src | MAC dst | IP src        | IP dst        | Type de message |
| ------- | ------- | ------------- | ------------- | --------------- |
| `25:25` | `11:11` | `10.2.2.2/24` | `10.1.1.1/24` | Pong            |

# 4. Cas de la route par défaut

Les machines ont souvent une passerelle unique qui leur permet de joindre plein de réseaux. **On l'appelle la *passerelle par défaut*.** C'est notamment, cette route, la *route par défaut*, celle qui utilise la *passerelle par défaut*, qui permet "d'avoir internet".

Exemple avec la table de routage d'une machine Windows :

```powershell
# On affiche la table de routage
PS C:\Users\Hita> route print -4
[...]
IPv4 Route Table
===========================================================================
Active Routes:
Network Destination        Netmask          Gateway       Interface  Metric
          0.0.0.0          0.0.0.0      192.168.1.1     192.168.1.29     50
      192.168.1.0    255.255.255.0         On-link      192.168.1.29    306
     192.168.1.29  255.255.255.255         On-link      192.168.1.29    306
    192.168.1.255  255.255.255.255         On-link      192.168.1.29    306
===========================================================================
```

**On voit ici que la machine possède deux routes :**

- une vers `192.168.1.0/24`, la machine est directement branchée à ce réseau ("on-link") donc pas besoin de passerelle
- une autre, la passerelle par défaut, indiqué sous Windows comme une route vers `0.0.0.0` qui utilise `192.168.1.1`

> *C'est des vraies valeurs, `192.168.1.1` est l'IP de ma box chez moi.*

Donc si ma machine veut aller dans `192.168.1.0/24` elle le fait en direct : elle est dans ce réseau.  
**Pour tout autre réseau, elle enverra un message vers la passerelle `192.168.1.1`.**
