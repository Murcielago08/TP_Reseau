# MITM et DNS Spoofing

Dans ce TP, on va développer un machin qui permet de :

- scan un réseau et trouver les autres machines présentes
- usurper l'identité de deux personnes
- et ainsi se retrouver en position de MITM
- une fois en position de MITM on va  mettre en place un DNS spoofing

Chaque partie sera un peu plus détaillée dans la section dédiée, lisez le document en entier :)

Je vous conseille l'environnement suivant pour réaliser le TP :

- vous codez sur votre machine
- je vous conseille
  - Python pour le langage
  - Scapy comme librairie pour mettre en place le TP
- 3 VMs Linux (OS de votre choix)
  - une victime (utilisez un Debian/Ubuntu)
  - un attaquant (utilisez un Debian/Ubuntu)
  - un routeur (utilisez un Rocky)
- un dépôt git où vous stockez le code
  - vous faites des push depuis votre machine
  - vous faites des pull depuis la machine attaquant

> Sérieux, vous mettez pas Windows dans les pattes pour ce TP, utilisez une machine Linux.

## 1. Scan réseau

Pour scanner un réseau, plusieurs méthodes peuvent être intéressantes :

- envoyer des *pings* à tout le réseau, c'est des paquets ICMP pour rappel
- envoyer des *ARP request* à tout le réseau

> L'avantage de l'ARP c'est qu'il n'est quasiment jamais bloqué sur les réseaux, car il ne repose pas suir le protocole IP, c'est juste de l'Ethernet.

➜ **Votre script Python doit :**

- déterminer toutes les IPs d'un réseau et itérer dessus avec une boucle
- envoyer un ARP request et/ou un ping à toutes ces IPs
- établir une liste des IPs qui ont répondu

> Il peut être utile de stocker les adresses IPs des machines trouvées, mais aussi leur adresse MAC.

## 2. ARP Poisoning et MITM

### A. ARP Spoof

Une fois qu'on a obtenu l'adresse des deux victimes, on peut passer à l'attaque elle-même. J'ai déjà décrit l'attaque [au TP2, je vous invite donc à aller relire la section dédiée dans le TP2](../../2/README.md).

➜ **Dans un premier temps, essayez d'envoyer un ARP reply à la machine victime qui contient des mauvaises informations**

- envoyer un ARP reply à la victime
- il contient de fausses informations
- il faut donc mettre dans cet ARP reply :
  - une fausse MAC source
  - une fausse IP source
- constatez que ça fonctionne en affichant la table ARP sur la victime
  - un ptit `ip neigh show`

### B. MITM

➜ **Pour mettre en place le MITM il faut :**

- ARP reply vers la passerelle
  - qui contient les adresses IP et MAC source de la victime
- ARP reply vers la victime
  - qui contient les adresses IP et MAC source de la passerelle
- spam les ARP replies
- faire en sorte que votre machine accepte de faire passer le trafic de l'un à l'autre de façon transparente
  - sur un Debian/Ubuntu il faut activer l'IPv4 forwarding

➜ **Constater avec un `tcpdump` ou Wireshark que le trafic de la victime passe par l'attaquant**

## 3. DNS Spoofing

Une fois que le MITM est en place, vous pouvez en faire quelque chose.

Les requêtes DNS passent en clair sur le réseau quand votre victime essaie de joindre des noms de domaine comme `google.com`.

Il est possible de les intercepter et d'y répondre de façon malicieuse :

- la victime demande l'adresse IP correspondant au nom `www.google.com`
- vous répondez une fausse adresse IP
- l'idée est de mener la victime sur un site de phishing dans une attaque réelle, on se contentera ici de la réponse malicieuse

> Pour pousser plus loin il faut utiliser un site hébergé en ligne ou un outil comme `ngrok`.