# TP5 DEV : Coding Encoding Decoding

Dans ce TP on va faire plusieurs choses qui tournent toujours autour du réseau, mais qui amènent la problématique de l'encodage au premier plan.

Au menu :

- premiers pas pour jouer avec l'encodage
  - utilisation des méthodes natives de python
  - encodage à la mano
- une calculatrice un peu opti
  - la calculatrice du TP précédent
  - l'idée sera de maîtriser au bit près ce qu'on envoie sur le réseau
- serveur Web et transfert de fichier

![Python hurts](./img/python_hurts.png)

## Sommaire

- [TP5 DEV : Coding Encoding Decoding](#tp5-dev--coding-encoding-decoding)
  - [Sommaire](#sommaire)
- [I. Jouer avec l'encodage](#i-jouer-avec-lencodage)
- [II. Opti calculatrice](#ii-opti-calculatrice)
  - [0. Setup](#0-setup)
  - [1. Strings sur mesure](#1-strings-sur-mesure)
  - [2. Code Encode Decode](#2-code-encode-decode)
- [III. Serveur Web HTTP](#iii-serveur-web-http)
  - [0. Ptite intro HTTP](#0-ptite-intro-http)
  - [1. Serveur Web](#1-serveur-web)
  - [2. Client Web](#2-client-web)
  - [3. Délivrer des pages web](#3-délivrer-des-pages-web)
  - [4. Quelques logs](#4-quelques-logs)
  - [5. File download](#5-file-download)

# I. Jouer avec l'encodage

➜ **Rien à rendre dans cette partie**

- jouez avec l'encodage et les sockets avant de passer à la suite
- faites un client qui envoie un grand nombre "100000" par exemple à un serveur
- interdiction d'utiliser `encode()` avant d'envoyer sur le réseau : traitez le nombre comme un entier, pas une string !

# II. Opti calculatrice

Dans cette partie on va commencer par **gérer correctement l'envoi/réception comme un flux de données** plutôt qu'un appel à `recv(1024)` random (pourquoi 1024 ?).

> On reste sur le thème nul de la calculatrice réseau pour le moment.

## 0. Setup

Réutilisez votre code du TP5, la calculatrice, ou partez avec cette version minimale et simplifiée :

> *Pas besoin de logs ni rien là, on se concentre sur le sujet : l'encodage.*

➜ **Client**

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 9999))
s.send('Hello'.encode())

# On reçoit la string Hello
data = s.recv(1024)

# Récupération d'une string utilisateur
msg = input("Calcul à envoyer: ")

# On envoie
s.send(msg.encode())

# Réception et affichage du résultat
s_data = s.recv(1024)
print(s_data.decode())
s.close()
```

➜ **Serveur**

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('127.0.0.1', 9999))  

s.listen(1)
conn, addr = s.accept()

while True:

    try:
        # On reçoit la string Hello du client
        data = conn.recv(1024)
        if not data: break
        print(f"Données reçues du client : {data}")

        conn.send("Hello".encode())

        # On reçoit le calcul du client
        data = conn.recv(1024)

        # Evaluation et envoi du résultat
        res  = eval(data.decode())
        conn.send(str(res).encode())
         
    except socket.error:
        print("Error Occured.")
        break

conn.close()
```

## 1. Strings sur mesure

On gère toujours que des strings pour le moment, on reste sur de simples `encode()` et `decode()` pour le transit sur le réseau.

🌞 **`tp5_enc_client_1.py`**

- permet à l'utilisateur de saisir une string, qui doit être une expression arithmétique simple
  - on tolère uniquement les nombres qui tiennent sur 4 octets (inférieur à 4294967295 donc, *un nombre que certains gamers reconnaîtront... hihi*)
  - uniquement les opérations addition, soustraction, multiplication (restons simples)
  - sous la forme simple "x opération y" par exemple `3 + 3` (pas de `3 + 3 + 3` par exemple)
  - vous devez donc contrôler la saisie utilisateur avant de l'envoyer
- détecter la taille de l'expression saisie par l'utilisateur
- le client envoie au serveur :
  - un en-tête qui annonce la taille du message (ou des messages)
  - le message
  - une séquence de fin (par exemple `<clafin>` ou juste un `0`)

> Va falloir être un peu **créatif** pour gérer tout ça, avec votre ptit encodage maison, c'est un problème algorithmique. Peut-être que ce serait malin d'annoncer la taille des deux entiers dans des en-têtes. Par exemple : lire 1 octets qui contiennent la taille du premier entier, puis lire X octets pour obtenir le premier entier, puis lire 1 octet pour l'opération, puis lire 1 octets qui contiennent la taille du deuxième entier, etc.

➜ [Bout de code client pour vous aider](./example_code/stream_tcp_client.py)

- il réceptionne un message utilisateur
- calcule sa taille
- créer un header
- envoie le tout sur le réseau

🌞 **`tp5_enc_server_1.py`**

- attend la réception des messages d'un client
- à la réception d'un message
  - lit l'en-tête pour déterminer combien il doit lire ensuite
  - lit les x octets suivants
  - reconstitue le message
  - vérifie que le message se terminent bien par la séquence de fin

➜ [Bout de code serveur pour vous aider](./example_code/stream_tcp_server.py)

- fonctionnel avec le client juste avant
- il lit le header et lit dynamiquement la taille du message qui suit

> *Hé on s'approche de plus en plus de problèmes réels là, tu le sens ou pas meow.* 🐈‍

![Don't stop](./img/dontstop.jpg)

## 2. Code Encode Decode

🌞 **`tp5_enc_client_2.py` et `tp5_enc_server_2.py`**

- maintenant vous traitez les entiers comme des entiers et plus comme des strings


# III. Serveur Web HTTP

Un protocole c'est donc juste des headers, des décisions sur l'encodage, et des données brutes derrière. Genre c'est tout.

Bon bah on va coder un serveur web à la main dukoo. Basique, mais fonctionnel.

Et un navigateur aussi. Un nul, qui supporte rien ou presque, et en ligne de commande.

Faire un vrai navigateur en ligne de commande, genre imiter `curl`, ça demande pas grand chose de plus en terme de cerveau, c'est "juste" des milliers de `if` à rajouter (sans être trop réducteur vis-à-vis de ce beau HTTP).

> Cette section c'est pour montrer aussi les limites de l'encodage opti. Le web c'est trop diversifié comme contenu. Un clieu de MMORPG, tu contrôles exactement ce qu'il t'envoie, et le contenu du jeu, étou. Sur le web, c'est la jungle y'a de tout partout, alors on utilise juste un encodage standard comme UTF-8.

## 0. Ptite intro HTTP

Si je lance un serveur web NGINX avec juste la page d'accueil, je peux le `curl` (ou visiter en navigateur) :

```bash
❯ curl localhost:8080
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
[...BLABLABLA HTML...]
<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

Mais je peux aussi me connecter directement au port TCP et faire la requête HTTP à la main. Bah faut juste savoir parler l'HTTP quoi. J'ai des bases :D

Une requête HTTP c'est :

- un verbe, par exemple `GET`
  - `GET` c'est pour demander une page
  - `POST` pour envoyer des données
  - y'en a d'autres
- on précise une URI, par exemple `/index.html`
  - c'est genre la ressource sur laquelle on veut agir
  - `GET /index.html` ça veut dire "DONNE L'INDEX STP" et le client le télécharges l'index
- et euh c'est tout
  - enfin c'est le strict minimum
  - on peut aussi préciser des options, avec des les headers HTTP
  - par exemple indiquer qu'on est sur mobile ou PC, pour que le serveur retourne la bonne version du site

Exemple, avec le même serveur Web qu'au dessus. J'utilise `nc` pour me connecter directement au port TCP, mais un bout de code Python qui se co avec la lib `socket` ce serait pareil :

```bash
❯ nc localhost 8080
coucou le serveur donne moi la page html stp
HTTP/1.1 400 Bad Request
Server: nginx/1.25.3
Date: Mon, 27 Nov 2023 13:50:18 GMT
Content-Type: text/html
Content-Length: 157
Connection: close

<html>
<head><title>400 Bad Request</title></head>
<body>
<center><h1>400 Bad Request</h1></center>
<hr><center>nginx/1.25.3</center>
</body>
</html>
```

Apparemment, lui envoyer `coucou le serveur donne moi la page html stp` il me chie dessus avec un code retour 400 qui signifie Bad Request.

Essayons de parler l'HTTP :

```bash
❯ nc localhost 8080
GET /le_plus_beau_des_index.html
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx/1.25.3</center>
</body>
</html>
```

Cette fois une 404 : il trouve pas le fichier `le_plus_beau_des_index.html`, sad. MAIS il a compris notre requête !

Dernier exemple et vous savez parler le HTTP LV1 :

```bash
❯ nc localhost 8080
GET /index.html
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
[...BLABLABLA HTML...]
<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

Donc : on se co au port TCP, on envoie la string `GET /index.html` et on récupère en retour une string aussi : la page HTML.

> On peut aussi juste `GET /` et il retourne automatiquement la page d'accueil. Souvent c'est l'index, mais pas forcément. C'est l'admin du serveur web qui choisit.

C JUSTE SA ENFET.

## 1. Serveur Web

🌞 **`tp5_web_serv_1.py` un serveur HTTP** super basique

- il répond à la string `GET /` par `HTTP/1.0 200 OK\n\n<h1>Hello je suis un serveur HTTP</h1>`
- un vrai serveur web HTTP qui respecte le standard :
  - la version de HTTP utilisée
  - le code retour (`200 OK` ça indique que tout s'est bien passé)
  - et ensuite le contenu de la page
- testez avec `curl`
- testez avec votre navigateur

## 2. Client Web

🌞 **`tp5_web_client_2.py` un client HTTP** super basique

- il peut envoyer des ptits `GET /`
- il doit fonctionner avec votre serveur

> Essaie de visiter la page d'accueil de l'école avec pour voir si ça fonctionne ? Juste pour voir :D

## 3. Délivrer des pages web

🌞 **`tp5_web_serv_3.py`**

- il délivre des pages HTML stockées sur le disque ce fou
- en fonction de ce qui est demandé par le client il peut donner tel ou tel fichier HTML
  - si le client il envoie `GET /toto.html`, votre serveur renvoie le contenu du fichier `toto.html`
  - ça doit marcher avec votre navigateur aussi !
- ptit exemple pour lire le contenu d'un fichier et l'envoyer :

```python
file = open('htdocs/index.html')
html_content = file.read()
file.close()

http_response = 'HTTP/1.0 200 OK\n\n' + html_content
sock.send(response.encode())
```

## 4. Quelques logs

🌞 **`tp5_web_serv_4.py`**

- gestion de logs !
- quand un client télécharge un fichier, on log la requête
- au format standard
- pas de couleurs ni rien (sauf si tu veux t'amuser)  

## 5. File download

Euuuuuh. On a pas créé accidentellement un downloader de fichier là ? En fait le protocole HTTP c'est juste ça à la base hein : une langue standard qui permet à un client de télécharger des fichiers.

Ca fait quoi si au lieu de demander un `.html` on demande un `.mp3` ou `.jpg` ? Bah pareil : tu le télécharges.

🌞 **`tp5_web_serv_5.py`**

- doit permettre de télécharger des plus volumineux que 3 lignes de HTML
- comme des images par exemple (JPG)
- il sera intéressant de réutiliser la mécanique de chunks, de headers, etc de la section II. précédente avec la calculatrice !

> Un gros fichier de ce genre, il sera forcément fragmenté en plusieurs bouts sur le réseau. Il est donc essentiel de gérer le transfert morceau par morceau.
