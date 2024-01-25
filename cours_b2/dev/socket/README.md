# Ports TCP et UDP

Dans ce cours : quelques rappels sur la notion de **ports** : les protocoles TCP et UDP.

> *En anglais, un "port" ça se dit "socket".*

- [Ports TCP et UDP](#ports-tcp-et-udp)
  - [1. Notion technique](#1-notion-technique)
  - [2. With Python](#2-with-python)
    - [A. Ecoute](#a-ecoute)
    - [B. Connexion](#b-connexion)

## 1. Notion technique

Ptit récap général de la situation et de ce que vous savez sur le sujet :

- deux machines A et B peuvent communiquer si A connaît l'IP de B (ou inversement)
- ils peuvent s'envoyer des paquets (niveau 3)
- des paquets...
  - ICMP par exemple `ping`
  - IP avec des trucs probablement plus intéressants qu'un `ping` dedans
- à l'intérieur des paquets IP on trouve du trafic TCP ou UDP
- TCP et UDP sont utilisés pour échanger des données entre deux programmes

C'est donc l'objectif de l'utilisation des ports : permettre à deux programmes de communiquer, potentiellement qui s'exécutent sur deux machines différentes, à travers le réseau, grâce à TCP et UDP.

> Typiquement, l'un des deux programmes on dit que c'est **un serveur**, et l'autre **un client**. Le serveur attend que des clients se connectent. Par abus de langage, les mots "client" et "serveur" désigne aussi bien les machines que les programmes qui tournent dessus.

On change pas les règles avec les les ports TCP et UDP :

- il existe 65535 TCP, autant en UDP, pour CHAQUE interface réseau
  - c'est le nombre de programme différents qui peuvent communiquer en utilisant le le réseau
  - chaque programme peut choisir un port et recevoir ou envoyer des données en l'utilisant
- en effet, un programme peut se placer derrière un port (on dit que le programme se `bind`) et envoyer des données à travers ce port
- lorsque deux machines A et B le souhaitent, elles peuvent établir un tunnel de communication
  - par exemple A écoute sur un port
  - B se connecte au port de A pour lui envoyer des données
  - pour ce faire, B a spontanément et automatiquement ouvert un port de son côté
  - ici on dit que *A est le serveur (il écoute)* et *B le client (il effectue la connexion)*

Quand on fait aucune fifollerie, on est donc toujours dans ce cas là :

- **la machine serveur...**
  - choisit un port TCP ou UDP (arbitrairement)
  - **exécute un programme** qui va **écouter derrière ce port**
    - on appelle ce programme un service ou un serveur
- **alors une machine cliente...**
  - si elle connaît l'IP du serveur
  - et qu'elle connaît aussi le port derrière le serveur écoute
  - elle peut **exécuter un programme** qui va **se connecter à l'IP du serveur, sur le bon port**
    - on appelle ce programme un client
  - pour ce faire, la machine cliente ouvre spontanément un port de son côté, et établit un tunnel de communication entre son port et celui du serveur

> *Les commandes `netstat` sous Windows et MacOS ainsi que la commande `ss` sous les OS GNU/Linux permettent d'obtenir des infos sur les ports actuellement utilisés par des programmes : en tant que client (connexion) ou serveur (écoute).*

## 2. With Python

On a donc besoin d'apprendre à faire les choses suivantes depuis du code :

- écouter sur un port
  - comme ça on sait faire un programme qui agit comme un serveur
- se connecter à un port distant
  - comme ça on sait faire un programme qui agit comme un client
- une fois la connexion effectuée (le tunnel de communication établi), envoyer des données
  - bah oui, le client et le serveur vont se dire des trucs !

➜ **En Python, c'est la librairie `socket` qu'on va utiliser pour toutes ces opérations.**

### A. Ecoute

Pour demander à un programme d'écouter sur un port, l'idée c'est :

- instancier un objet `socket` de type TCP ou UDP
- demander au programme de se *bind* sur le port, et de passer en mode écoute
- déclarer quoi faire à chaque réception d'un message d'un client
  - typiquement, dans une boucle infinie, pour que le serveur soit up tout le temps

Let's go :

```python
import socket

# On choisit une IP et un port où on va écouter
host = '' # string vide signifie, dans ce conetxte, toutes les IPs de la machine
port = 8888 # port choisi arbitrairement

# On crée un objet socket
# SOCK_STREAM c'est pour créer un socket TCP (pas UDP donc)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# On demande à notre programme de se bind sur notre port
s.bind((host, port))  

# Place le programme en mode écoute derrière le port auquel il s'est bind
s.listen(1)
# On définit l'action à faire quand quelqu'un se connecte : on accepte
conn, addr = s.accept()
# Dès que quelqu'un se connecte, on affiche un message qui contient son adresse
print('Connected by', addr)

# Petite boucle infinie (bah oui c'est un serveur)
# A chaque itération la boucle reçoit des données et les traite
while True:

    try:
        # On reçoit 1024 bytes de données
        data = conn.recv(1024)

        # Si on a rien reçu, on continue
        if not data: break

        # On affiche dans le terminal les données reçues du client
        print(f"Données reçues du client : {data}")

        # On répond au client un truc
        conn.sendall("Salut mec.")

    except socket.error:
        print("Error Occured.")
        break

# On ferme proprement la connexion TCP
conn.close()
```

### B. Connexion

Pour le client, plus simple :

- on crée un objet `socket` de type TCP pour se connecter au serveur
- on établit la connexion vers le serveur
- on envoie quelques données, et on close
- on devrait avoir une réponse du serveur qui s'affiche

```python
import socket

# On définit la destination de la connexion
host = '<IP_du_serveur>'  # IP du serveur
port = 8888               # Port choisir par le serveur

# Création de l'objet socket de type TCP (SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connexion au serveur
s.connect((host, port))
# note : la double parenthèse n'est pas une erreur : on envoie un tuple à la fonction connect()

# Envoi de data bidon
s.sendall(b'SALUT MEC')

# On reçoit 1024 bytes qui contiennent peut-être une réponse du serveur
data = s.recv(1024)

# On libère le socket TCP
s.close()

# Affichage de la réponse reçue du serveur
print(f"Le serveur a répondu {repr(data)}")
```
