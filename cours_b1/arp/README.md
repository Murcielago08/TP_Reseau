# ARP

ARP est un protocole essentiel au bon fonctionnement des communications au sein d'un LAN.

> ARP c'est pour *Adress Resolution Protocol*.

On va voir dans ce cours le problème qu'il vient résoudre, et son fonctionnement dans une utilisation classique.

- [ARP](#arp)
  - [1. Le problème](#1-le-problème)
  - [2. ARP à la rescousse](#2-arp-à-la-rescousse)
  - [3. Fonctionnement de ARP](#3-fonctionnement-de-arp)
  - [4. Quelques subtilités](#4-quelques-subtilités)
    - [A. Broadcast problématique](#a-broadcast-problématique)
    - [B. Limiter le broadcast](#b-limiter-le-broadcast)

## 1. Le problème

Pour mettre en évidence le soucis auquel on fait face, le problème que ARP vient résoudre, donnons tout de suite un exemple.

Supposons un LAN très simpliste :

![LAN 1](./img/lan1.svg)

Les deux PCs ont une interface réseau, branchée à l'aide d'un câble à un switch. Ils sont donc connectés physiquement entre eux.

On change pas les règles du jeu : chaque interface réseau a une adresse MAC et une adresse IP.

Si PC1 ouvre un terminal et essaie d'envoyer un `ping` :

```bash
PC1$ ping 10.1.1.2
```

Il doit alors fabriquer une trame qui ressemble à :

![Trame 1](./img/trame1.svg)

> *Comme d'habitude, le message ("PING !") est placé dans un paquet IP, lui-même placé dans une trame Ethernet.*

Dans cette trame on note 4 informations :

- `IP src` : le PC1 la connaît car c'est sa propre adresse IP : `10.1.1.1`
- `IP dst` : le PC1 la connaît car c'est l'adresse IP que l'utilisateur a saisi dans la commande `ping 10.1.1.2`
- `MAC src` : le PC1 la connaît car c'est sa propre adresse MAC : `11:11:11:11:11:11`
- `MAC dst` : **le PC1 ne la connaît pas**

➜ **Le PC1 est incapable de construire la trame qui enverrait un `ping` vers PC2. Strictement incapable, car il ne connaît pas l'adresse MAC du destinataire.**

> *Oui ok pour un humain c'est évident avec le schéma sous les yeux. Sauf que le PC1 n'a pas le schéma sous les yeux, et que ça devient de toute façon vite un gros bordel quand on a pas 2 PCs mais genre 1000.*

Pour que PC1 ***apprenne*** l'adresse MAC de son destinataire, le PC2, il va devoir utiliser le protocole ARP.

## 2. ARP à la rescousse

➜ **ARP est un protocole qui est utilisé de façon *spontanée* et complètement automatique par tous les PCs connectés en réseau.**

> *On dit "PC" ici, mais c'est pareil pour un téléphone, un routeur, un frigo connecté, une montre, peu importe. Un appareil connecté au réseau.*

Dès qu'un PC a besoin d'apprendre la MAC d'une autre machine qui se trouve **sur son LAN**, il peut utiliser ARP.

Je répète : **SUR SON LAN**. ARP est un protocole qui est utilisé et utilisable uniquement au sein d'un LAN.

> *ARP ne peut donc pas être utilisé à travers Internet par exemple, si votre PC se trouve lui dans un LAN.*

➜ **Grâce à ARP, un PC peut donc apprendre l'adresse MAC des autres machines du réseau**

Il faut, pour utiliser ARP et apprendre l'adresse MAC d'une autre machine, connaître à l'avance l'adresse IP de notre correspondant (ce qui est quasiment tout le temps le cas : on connaît l'IP mais pas la MAC).

> On voit dans la partie qui suit le fonctionnement en détail de ARP.

➜ **Une fois qu'une MAC a été apprise par un PC, il l'enregistre automatiquement dans sa table ARP**

> Il existe des synonymes pour "table ARP", notamment "ARP cache" ou "table de voisinnage".

```powershell
# Sur Windows, on peut afficher la table ARP de la machine avec :
PS C:\Users\it4> arp -a

Interface: 192.168.1.29 --- 0xa
  Internet Address      Physical Address      Type
  192.168.1.1           78-94-b4-de-fd-c4     dynamic
  192.168.1.255         ff-ff-ff-ff-ff-ff     static
[...]
```

La table ARP contient donc une liste de correspondances entre des adresses IP et des adresses MAC : c'est la liste des machines avec laquelle le PC a discuté jusqu'alors sur son LAN.

Je le répète encore : **SUR SON LAN**.

> *A noter que sur la plupart des OS modernes, une entrée dans la table ARP reste valide le temps d'une minute ou deux. Après cela, le PC va considérer qu'il n'est plus certain que l'information est vraie, et va donc réutiliser ARP pour vérifier que à telle IP se trouve toujours telle adresse MAC.*

## 3. Fonctionnement de ARP

ARP est un protocole très simpliste qui repose principalement sur deux trames :

- ***ARP Request***
  - message envoyé par le PC qui souhaite apprendre la MAC d'une autre machine sur son LAN
  - le message est envoyé à tout le monde sur le réseau, tous les gens connectés au LAN
  - le message signifie "Qui a l'IP `x.x.x.x` svp ?"
- ***ARP Reply***
  - message de réponse envoyé en réponse à l'ARP Request
  - il est envoyé depuis la machine qui porte l'IP `x.x.x.x` vers la machine qui a envoyé l'ARP Request
  - le message signifie "C'est moi qui ait l'IP `x.x.x.x` et mon adresse MAC est `xx:xx:xx:xx:xx:xx`"

> Pour envoyer une trame à tout le monde dans un LAN, il faut indiquer **`ff:ff:ff:ff:ff:ff`** en adresse MAC de destination. `ff:ff:ff:ff:ff:ff` est une adresse MAC réservée, qu'on appelle ***adresse de broadcast***. C'est son utilité : envoyer un message à tous les autres membres du LAN. Quand un switch reçoit une trame à destination de `ff:ff:ff:ff:ff:ff`, il la renvoie sur TOUS ses ports : à toutes les machines du LAN.

---

Un exemple ? On reprend le même schéma que plus tôt :

![LAN 1](./img/lan1.svg)

Et on suppose la même chose : PC1 va essayer de ping PC2 avec la commande :

```bash
PC1$ ping 10.1.1.2
```

➜ **PC1 va donc avoir besoin d'apprendre l'adresse MAC de PC2** afin de communiquer avec lui. Comme vu dans la partie 1 de ce cours, il a besoin de connaître l'adresse MAC du PC2 pour constuire la trame adéquate.

Une fois que la commande `ping` est envoyée, le PC1 va donc **spontanément** envoyer un ARP Request à tout le monde sur le réseau.

La trame ressemble à :

![ARP request](img/arp_req.svg)

➜ **Tout le monde reçoit cette trame**, le PC2, mais aussi n'importe quel autre PC connecté au LAN.

Tout le monde ignore cet ARP request **sauf PC2**, qui se rend compte que c'est lui qu'on cherche, il se rend compte que PC1 cherche à apprendre son adresse MAC.

➜ PC2 va donc répondre à PC1 un ARP Reply afin que PC1 connaisse la MAC de PC2.

La trame ressemble à :

![ARP reply](img/arp_rep.svg)

➜ Une fois l'échange ARP effectué, les deux PCs vont **enregistrer dans leur table ARP respective l'adresse MAC de leur correspondant**.

Ainsi, PC1 va stocker l'information que l'adresse IP `10.1.1.2` correspond à la MAC `22:22:22:22:22:22`.

```powershell
# Sur PC1 :
PS C:\Users\PC1> arp -a

Interface: 10.1.1.1 --- 0xa
  Internet Address      Physical Address      Type
  10.1.1.2              22-22-22-22-22-22     dynamic
[...]
```

```powershell
# Sur PC2 :
PS C:\Users\PC2> arp -a

Interface: 10.1.1.2 --- 0xa
  Internet Address      Physical Address      Type
  10.1.1.1              11-11-11-11-11-11     dynamic
[...]
```

➜ Enfin, **après l'échange ARP** et l'enregistrement dans la table ARP, le **PC1 va pouvoir constuire la trame qui contiendra son `ping`**.

Il va pouvoir renseigner correctement l'adresse MAC `22:22:22:22:22:22` qu'il vient d'apprendre avec l'échange ARP en adresse MAC de destination de son message :

![Il part ce ping ou pas enfet](img/trame1.svg)

➜ **PC2 pourra répondre un `pong` car il a déjà appris l'adresse MAC de PC1 lors de leur échange ARP**.

> Tout ça se passe très vite, à tel point que quand on fait un `ping` on a l'impression que c'est instantané, alors que la plupart du temps, un échange ARP a été nécessaire.

## 4. Quelques subtilités

### A. Broadcast problématique

Le fait d'envoyer l'ARP Request en broadcast est un soucis de sécurité. En effet, n'importe qui peut répondre un ARP Reply avec de fausses informations et donc se faire passer pour une autre machine au sein d'un LAN.

On appelle cette attaque un **ARP poisoning** : c'est le fait d'injecter de fausses informations dans la table ARP de quelqu'un d'autre.

Une telle attaque peut déboucher sur une situation de MITM (man-in-the-middle) : un hacker pouvant intercepter toutes les communications entre deux machines qui sont dans le même LAN que lui (une victime et le routeur typiquement).

![ARP sniffed ?](img/arp_snif.jpg)

### B. Limiter le broadcast

Il existe une solution simpliste que mettent en place tous nos OS modernes pour limiter la quantité de trames ARP Request qui partent avec une destination en broadcast. Elle consiste à :

- à la toute première fois qu'on a besoin de connaître l'adresse MAC d'une autre machine, ça part en broadcast (ça change pas quoi pour le moment)
- la machine enregistre la MAC du correspondant dans sa table ARP
- si la machine a besoin de réitérer l'échange, la trame ne partira pas en broadcast, mais directement vers la MAC anciennement enregistrée.

Pour humaniser le raisonnement : plutôt que de dire à toutes les machines du réseau "HE LES GARS, qui porte l'IP x.x.x.x svp ?", on contacte directement une machine, et on lui demande "HE SALUT TOI, est-ce que c'est toujours toi qui porte l'IP x.x.x.x ?".