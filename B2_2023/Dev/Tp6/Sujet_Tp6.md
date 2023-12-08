# TP6 DEV : Chat room

Dans ce TP on continue toujours sur du dév réseau, c'est genre le thème un peu ! On progresse au fil des TPs en voyant de nouvelles notions au fur et à mesure.

Le but à la fin de ce TP : avoir **une petite application de chat à peu près stylée.** Plusieurs clients connectés qui discutent.

![Kittens](./img/kittens.jpg)

Pour ça, on va amener une nouvelle notion : **l'asynchrone.**

> Prenez connaissance du [cours sur le sujet](../../../cours/dev/async/README.md).

En Python ça commence à être bien intégré depuis récemment.
Pour quelque chose de basique comme ce qu'on va faire, la complexité reste sous contrôle.

➜ **Côté client :**

- se connecte au serveur, en indiquant son pseudo
- arrive dans la chatroom
- peut envoyer des messages, qui seront reçus par tous les autres clients connectés

➜ **Côté serveur :**

- attend la connexion de nouveaux clients
- quand un client se connecte, il l'ajoute à la liste des clients présents
- quand un client envoie un message, il le redistribue à tous les autres

## Quelques remarques

Vous allez commencer à produire **pas mal de lignes** de code au fur et à mesure.

Je ne serai pas trop regardant sur les TPs d'avant, mais à partir de maintenant, je serai très regardant sur **la clarté de votre code**. Ne sur-commentez pas chaque ligne, c'est pas ça, parce que c'est pire encore.

Quelques conseils donc :

- **nommez** judicieusement vos variables et fonction
- c'est souvent plus clair si vous **typez** les arguments des fonctions/retours de fonction
- **commentez** les lignes qui ne sont pas assez claires d'elles-mêmes
- éclatez votre code en **plusieurs feuilles** Python, je vous laisse libre pour l'organisation pour le moment

## Sommaire

- [TP6 DEV : Chat room](#tp6-dev--chat-room)
  - [Quelques remarques](#quelques-remarques)
  - [Sommaire](#sommaire)
- [I. Faire joujou avec l'asynchrone](#i-faire-joujou-avec-lasynchrone)
  - [1. Premiers pas](#1-premiers-pas)
  - [2. Web Requests](#2-web-requests)
- [II. Chat room](#ii-chat-room)
  - [1. Intro](#1-intro)
  - [2. Première version](#2-première-version)
  - [3. Client asynchrone](#3-client-asynchrone)
  - [4. Un chat fonctionnel](#4-un-chat-fonctionnel)
  - [5. Gérer des pseudos](#5-gérer-des-pseudos)
  - [6. Déconnexion](#6-déconnexion)
- [III. Chat Room bonus](#iii-chat-room-bonus)
  - [1. Basic Cosmetic](#1-basic-cosmetic)
  - [2. Gestion d'ID](#2-gestion-did)
  - [2. Logs](#2-logs)
  - [3. Config et arguments](#3-config-et-arguments)
  - [4. Encodage maison](#4-encodage-maison)
  - [5. Envoi d'image](#5-envoi-dimage)
  - [6. Gestion d'historique](#6-gestion-dhistorique)
  - [7. Plusieurs rooms](#7-plusieurs-rooms)

# I. Faire joujou avec l'asynchrone

Avant de passer au vif du sujet, on va commencer par juste se faire la main sur l'asynchrone avec Python.

## 1. Premiers pas

🌞 **`sleep_and_print.py`**

- écrire une fonction qui compte jusqu'à 10, affiche l'entier, et sleep 0.5 secondes entre chaque print
- appeler deux fois la fonction

> *Le code va exécuter la première fonction (~5 secondes) puis la deuxième (à nouveau ~5 secondes) pour un total de ~10 secondes d'exécution. Pas de surprises.*

🌞 **`sleep_and_print_async.py`**

- version asynchrone
  - la fonction doit être une fonction asynchrone
  - vous l'appelez toujours deux fois à la fin du script
- utilisez la mécanique de *loop* de `asyncio`

> *Dès que l'exécution de la première fonction commencera à produire de l'attente, l'exécution de la deuxième commencera.*

## 2. Web Requests

🌞 **`web_sync.py`**

- on peut l'appeler comme ça : `python web_sync.py https://www.ynov.com`
- il télécharge le contenu d'une page Web qu'on lui passe en argument
- la page web est téléchargée dans `/tmp/web_page`
- le code doit comprendre une fonction `get_content(url)`
  - `url` est l'URL de la page à récupérée
  - la fonction fait la requête HTTP GET pour récupérer la page
  - la fonction retourne le résultat
- le code doit comprendre une fonction `write_content(content, file)`
  - `content` est le contenu à écrire dans le fichier
  - `file` est le path dans lequel écrire

> Utilisez les méthodes classiques pour faire ça. Lib `requests` pour faire la requête HTTP, et méthode native `open()` pour écrire dans un fichier.

🌞 **`web_async.py`**

- pareil mais en asynchrone
  - utilisez bien `aiohttp` pour faire la requête web
  - et `aiofiles` pour l'écriture sur disque
  - référez-vous [au cours sur l'asynchrone](../../../cours/dev/async/README.md) pour la syntaxe
- les deux fonctions imposées précédemment doivent être converties en asynchrone
- pas besoin de gather pour le moment : il faut que la requête se termine, afin de récup le contenu, avant de pouvoir effectuer l'écriture du contenu sur le disque

> *Ici on a deux appels qui peuvent générer de l'attente : la requête HTTP, et l'écriture sur le disque. L'un comme l'autre sont sujet à produire des temps d'attente, temps pendant lesquels Python pourra décider d'aller exécuter autre chose. L'asynchrone donc.*

🌞 **`web_sync_multiple.py`**

- synchrone (PAS asynchrone)
- pareil `web_sync.py` que mais le script prend en argument un fichier qui contient une liste d'URL
- il stocke le résultat dans `/tmp/web_<URL>` où l'URL c'est par exemple `www.ynov.com` (il faudra enlever le `https://` devant car on peut pas mettre de `/` dans un nom de fichier)

🌞 **`web_async_multiple.py`**

- version asynchrone de `web_sync_multiple.py`
- pas de *loop* utilisez la syntaxe moderne avec `gather()`

🌞 **Mesure !**

- utilisez la technique de votre choix pour chronométrer le temps d'exécution du script
- comparez les deux pour par exemple 10 URLs passées en argument

# II. Chat room

## 1. Intro

![Yet another](./img/yet_another.jpg)

L'idée de la ***chatroom*** c'est :

- **serveur**
  - écoute sur un port TCP
  - accueille des clients
  - entretient une liste de tous les clients connectés
  - à la réception d'un message d'un client, il le redistribue à tous les autres
  - **l'asynchrone** va permettre de gérer plusieurs clients "simultanément"
- **client**
  - se connecte au port TCP du serveur
  - peut envoyer des messages
  - reçoit les messages des autres
  - **l'asynchrone** va permettre d'attendre une saisie utilisateur et en même temps recevoir et afficher les messages des autres

Dans les deux cas, on va utiliser la lib Python `asyncio` pour mettre ça en place, mais on va utiliser deux choses différentes :

➜ **le serveur**

- on va utiliser la méthode `asyncio.start_server(handle_packet)` qui permet d'écouter sur un port TCP
- à chaque fois qu'un paquet est reçu, la méthode `handle_packet` (qu'on aura défini) le traite
- à chaque paquet reçu il est facile de lire le contenu, ou de formuler une réponse
- il pourra traiter en parallèle la réception/l'envoi de plusieurs messages

➜ **le client**

- on reste sur la lib `socket` pour la connexion TCP
- on pourra créer des *tasks* à exécuter de façon asynchrones :
  - une *task* pour la saisie utilisateur (le message que le user veut envoyer)
  - une *task* réception de données (les messages reçus des autres users)

## 2. Première version

Là on veut juste un truc qui ressemble de trèèès loin à un outil de chat. On va avancer ptit à ptit.

🌞 `chat_server_ii_2.py`

- utilise un `asyncio.start_server()` pour écouter sur un port TCP
- si un client se connecte
  - il affiche le message du client
  - il envoie `"Hello {IP}:{Port}"` au client
    - `{IP}` est l'IP du client
    - `{Port}` est le port utilisé par le client

> *Vous pouvez utiliser des `recv(1024)` partout pour le moment on s'en fout, on gérera des headers plus tard pour annoncer des tailles précises en bonus.*

🌞 `chat_client_ii_2.py`

- rien de nouveau pour le moment
- juste utilisation de `socket` comme aux TPs précédents
- quand le client se connecte
  - il envoie `"Hello"` au serveur
  - il attend une réponse du serveur et l'affiche

> Seul changement pour le moment, par rapport à ce qu'on a fait à avant : le serveur utilise `asyncio` pour écouter sur le port TCP. Ainsi, à chaque fois que des données sont reçues, on peut les traiter de manière concurrente (si par exemple, plus tard, deux clients envoient des données).

## 3. Client asynchrone

Adapter le code du client pour qu'il contienne deux fonctions asynchrones :

- **une qui attend une saisie utilisateur** : `async input()`
  - y'a un `while True:`
  - si le user saisit un truc
  - vous l'envoyez au serveur
- **une autre qui attend les messages du serveur** : `async_receive()`
  - y'a un `while True:` là aussi
  - si un message du serveur est reçu
  - afficher le message

Oui oui, un seul programme, deux `while True:`. Ils seront exécutés de façon concurrente, en asynchrone, grâce à `asyncio`.

➜ N'utilisez pas la fonction native `input()` de Python pour la saisie utilisateur : elle ne permet pas l'asynchrone. Il existe `aioconsole.ainput()` qui fait ça ! Il sera peut-être nécessaire d'installer le package `aioconsole`

➜ On peut pas non plus utiliser `sock.recv(1024)` comme d'hab : cette méthode `recv()` ne supporte pas `await`. Pas de `socket` en fait.

Comme chaque méthode qui génère de l'attente, il existe (probablement) une autre méthode qui fait ça en asynchrone (et qu'on peut donc await) en Python.

Pour le `sock.recv(1024)`, on va plutôt utiliser une version asynchrone de la gestion de socket client :

```python
# ouvrir une connexion vers un serveur
reader, writer = await asyncio.open_connection(host="127.0.0.1", port=8888)

# lire des données qui arrive du serveur
data = await reader.read(1024)
print(data.decode())

# envoyer des données
msg = 'hello'.encode()
writer.write(msg)
await writer.drain()
```

🌞 `chat_client_ii_3.py`

- **exécute de façon asynchrone une saisie utilisateur et la réception des messages**
- faites en sorte que l'affichage soit *pas trop* chaotique (vous prenez pas la tête non plus s'il y a quelques bugs/mochetés, on s'en fout pour le moment)
- le client ne quitte pas tant qu'on press pas `<CTRL + C>`
  - on peut donc saisir un message, l'envoyer, en saisir un deuxième, l'envoyer, etc
  - pendant que les messages reçus des autres clients s'affichent s'il y en a !

> **Pas de *event loop* uniquement du `gather()`.**

🌞 `chat_server_ii_3.py`

- quand un message est reçu, il l'affiche dans le terminal au format
  - `Message received from {IP}:{Port} : {msg}`

➜ Bon bah tout est asynchrone là déjà ?

- normalement, plusieurs clients peuvent se co et envoyer des messages
- les uns ne reçoivent pas les messages des autres, mais ça fonctionne le traitement de plusieurs clients propres

## 4. Un chat fonctionnel

➜ **Pour avoir un chat fonctionnel** *(sûrement moche, mais fonctionnel techniquement)* il reste plus qu'à **redistribuer le message quand un client envoie un truc**.

Le serveur donc, s'il reçoit un message d'un client, il le renvoie à tous les autres clients. Un chat quoi !

➜ Pour ça, il faut connaître que **le serveur connaisse à chaque instant la liste des clients connectés**.

On va rester simple ici et utiliser une **variable globale**. Ce sera un dictionnaire qui contiendra les infos des clients connectés.

A chaque fois qu'un client se connecte, ses infos sont ajoutées au dictionnaire.

Quand on veut envoyer un message à tout le monde, suffit de l'envoyer à tous les membres du dictionnaire.

Déclaration d'un dictionnaire global :

```python
global CLIENTS
CLIENTS = {}
```

🌞 `chat_server_ii_4.py`

- utilise une variable globale `CLIENTS`
- quand un client se co : son IP, son port, son reader et son writer sont stockées dans `CLIENTS`
  - si le client s'est déjà co (s'il est déjà dans `CLIENTS`) on ne fait rien
- soyons smart, vous stockerez sous cette forme là :

```python
# addr est le tuple (IP, port) du client : ce sera la clé de notre dico
# le reader nous permet de recevoir des données de ce client là
# le writer permet d'envoyer à ce client là
CLIENTS[addr] = {}
CLIENTS[addr]["r"] = reader
CLIENTS[addr]["w"] = writer
```

- quand un message d'un client est reçu
  - parcours du dictionnaire `CLIENTS`
  - envoi du message à tout le monde (sauf celui qui l'a envoyé)
  - le message doit être sous la forme `{IP}:{Port} a dit : {msg}`
    - `{IP}` est l'IP du client qui a envoyé le message
    - `{Port}` est le port utilisé par le client qui a envoyé le message

## 5. Gérer des pseudos

On va faire en sorte que chaque user choisisse un pseudo, et que le serveur l'enregistre. Ce sera plus sympa que `{IP}:{port}` pour identifier les clients.

🌞 `chat_client_ii_5.py`

- avant de lancer les deux tâches asynchrones (saisie user et réception de données)
- au début du code donc, de façon synchrone (PAS asynchrone)
  - une saisie utilisateur pour qu'il saisisse son pseudo
  - le client envoie le pseudo saisi au serveur
  - il envoie exactement : `Hello|<PSEUDO>`, par exemple `Hello|it4`

> **Si vous avez encore le client qui envoie juste la string "Hello" à la connexion, enlevez-le !**

➜ Dès sa connexion, le client envoie donc un message contenant son pseudo

- on peut utiliser ce savoir côté serveur : le premier message d'un client contient le pseudo

🌞 `chat_server_ii_5.py`

- à la réception d'un message
  - si le client est nouveau
  - on vérifie que la data commence par `Hello`
  - on stocke son pseudo dans le dictionnaire des clients
  - on envoie à tout le monde `Annonce : <PSEUDO> a rejoint la chatroom`

```python
# avant, isoler le pseudo du message "Hello|<PSEUDO>" dans une variable "pseudo"
CLIENTS[addr] = {}
CLIENTS[addr]["r"] = reader
CLIENTS[addr]["w"] = writer
CLIENTS[addr]["pseudo"] = pseudo
```

- quand il redistribue les messages il envoie `<PSEUDO> a dit : {msg}`

## 6. Déconnexion

Enfin, gérer proprement la déconnexion des clients.

Pendant vos tests, vous avez du apercevoir des comportements rigolos quand un client est coupé pendant que le serveur tourne.

Quand un client se déconnecte, il envoie un message vide facilement reconnaissable. Idem si le serveur se déconnecte, il envoie au client un message vide assez reconnaissable.

🌞 `chat_server_ii_6.py` et `chat_client_ii_6.py`

- côté client, si le serveur se déco
  - afficher un message et quitter l'app
- côté serveur, si un client se déco
  - l'enlever du dictionnaire global `CLIENTS`
  - envoyer un message à tout le monde comme quoi `Annonce : <PSEUDO> a quitté la chatroom`


# III. Chat Room bonus

Plusieurs bonus liés à la chatroom.

Ils sont tous indépendants les uns des autres.

Un bonus c'est... bonus, mais il serait de bon ton d'en faire au moins un ou deux.

## 1. Basic Cosmetic

Parlons un peu cosmétique côté client.

➜ **`Vous avez dit`**

- côté client, quand le user saisit et envoie un message, ça s'affiche de son côté dans l'historique sous la forme `Vous avez dit : {msg}`

➜ **Colors**

- côté serveur
  - une couleur random est générée pour chaque nouveau client qui se connecte
  - elle est stockée dans la variable globale `CLIENTS`, une couleur par client, choisie aléatoirement à sa connexion donc
  - dès qu'un message est reçu, et redistribué aux autres, la couleur associé au user qui a envoyé le message est aussi envoyée
- côté client
  - affiche le nom de l'utilisateur qui a parlé en couleur

> Ca augmente fortement la lisibilité du chat d'avoir une couleur unique associée à chaque user 💄

![Yet another](./img/not_sure.jpg)

➜ **Timestamp**

- **côté serveur**
  - quand un message est reçu, vous **enregistrer dans une variable l'heure et la date actuelle** : l'heure de réception du message en soit
  - quand il est redistribué aux clients, **l'heure est envoyée aussi**, pour que le client l'affiche
- **côté client**
  - affiche l'heure sous la forme `[hh:mm]` devant chaque message

## 2. Gestion d'ID

Bon c'est bien les pseudos étou, mais on aime bien les IDs pour gérer des users normalement. Ca apporte plein d'avantage quand on gère des applications à grandes échelle, ou juste en terme de conception si on commence à ajouter de la base de données dans le mix.

Surtout surtout, ça va nous permettre de gérer la déco/reco des clients. Quand un client se co, on peut vérifier si on le connaît déjà ou non.

➜ **Gestion d'ID uniques pour les utilisateurs**

- à la nouvelle connexion d'un client, un nouvel ID unique lui est attribué
- à vous de choisir une méthode, quelques idées :
  - juste un bête incrément : premier user c'est 1, deuxième 2, etc
    - mais... faut garder un trace de l'incrément actuel en permanence
    - et si un user est supprimé, ça crée un ID vaquant
  - un hash
    - le hash de la concaténation `IP:port:pseudo` par exemple, ça me paraît assez unique
    - ça implique qu'on reconnaît un user que s'il se co depuis la même IP et le même port aussi
- si un client se déco/reco
  - le serveur lui envoie un ptit message "Welcome back <PSEUDO> !"
  - le serveur envoie aux autres "<PSEUDO> est de retour !"

> Vous pouvez par exemple, dans le dictionnaire `CLIENTS` ajouter une propriété pour chaque client : `connected` qui est un booléen. Les clients qui sont à `connected = True` reçoivent des messages. Le serveur n'envoie pas de messages aux clients qui sont à `connected = False` mais peut les reconnaître en cas de reconnexion.

## 2. Logs

➜ **Gestion de logs côté client**

- un fichier dans `/var/log/chat_room/client.log`
- contient tout l'historique de conversation

➜ **Gestion de logs côté serveur**

- un fichier dans `/var/log/chat_room/server.log`
  - contient tout l'historique de conversation
  - contient l'heure d'arrivée et départ des clients
- logs console propres. Un message pour :
  - connexion d'un client
  - réception d'un message
  - envoi d'un message à un client
  - déconnexion d'un client

> Logs logs logs 📜 everywhere. Indispensable pour n'importe quelle application sérieuse.

## 3. Config et arguments

➜ **Gestion d'arguments et d'un fichier de conf**

- côté client
  - choisir l'IP et le port auxquels on se conncte
- côté serveur
  - choisir l'IP et le port sur lesquels écouter

> Ui parce que c'est super chiant de devoir éditer directement le code pour trouver la variable qui déclare l'IP et celle qui déclare le port.

**Le fichier de conf pour le client**, par exemple, doit pouvoir supporter cette syntaxe :

```
HOST=127.0.0.1
PORT=9999
```

> *Vous êtes libres de choisir une autre syntaxe ou d'autres mots-clés. Restez standards SVP, inventez pas un truc de ouf.*

Et toujours l'exemple avec le client, on doit pouvoir **appeler le script** comme ça :

```python
$ python client.py --port 9999 --address 127.0.0.1
$ python client.py -p 9999 -a 127.0.0.1
```

> *S'il existe un fichier de conf ET que des options sont précisées, ce sont les options qui sont prioritaires normalement.*

## 4. Encodage maison

Une des parties les plus tricky mais les plus abouties et qui fait suite au TP précédent.

La perf la perf la perf ! On va gérer des en-têtes pour indiquer la taille des messages et arrêter les `recv(1024)`.

➜ **Inventez un encodage maison pour la chatroom.**

---

➜ Par exemple, dès qu'un user envoie un message, le client pourrait formater son message comme ça :

```
1|32|salut à tous dans la chat room !
```

- `1` indique que le client envoie un message court qui doit être redistribué à tout le monde
- `32` est la longueur du message
- `salut à tous dans la chat room !` est le message que client a saisi
- les `|` ne sont pas envoyés : c'est juste pour faciliter votre lecture

Autrement dit on a :

- le premier octet qui contient le type de message
  - un `1` c'est un simple texte court à renvoyer aux autres (court = 2 octets)
- si le premier octet est un `1`, les deux octets suivants contiennent la taille du message
  - ici on lira 32 qui **doit** être encodé sur deux octets
- on peut ensuite lire autant d'octets que la valeur qu'on vient d'apprendre
  - ici on lira donc les 32 octets suivants, qui contiennent le message

➜ **On peut même faire mieux et imaginer un header lui-même à taille variable** (et pas que le message)

Par exemple, le client, à la saisie d'un message long, pourrait envoyer :

```
2|7|48038396025285290|<MSG TRES LONG>
```

- `2` indique que le client envoie un message long qui doit être redistribué à tout le monde
- `7` est le nombre d'octets qui contient la taille
- `48038396025285290` est la taille du message
- `<MSG TRES LONG>` c'est... le très long message

Le serveur :

- lit un octet et découvre `1` ou `2`
- si c'est un `1`
  - il lit 2 octets pour apprendre la taille du message
- si c'est un `2`
  - il lit 1 octet pour apprendre la taille du header de la taille
  - il lit n octets (valeur qu'il vient d'apprendre) pour apprendre la taille du message
- il lit le message en précisant le bon nombre d'octets à lire

➜ **Côté serveur, il faudrait aussi encoder les messages qui sont envoyés aux clients.**

Par exemple, si `toto` dit `bonjour`, le serveur pourrait envoyer le message suivant aux clients :

```
1|4|toto|1|7|bonjour
```

- `1` indique un message court (sur 1 octet)
- `4` indique la taille du pseudo (sur 1 octet, 256 caractères max par pseudo donc)
- `toto` le pseudo (taille variable, annoncée juste avant)
- `1` indique la taille du header du message (sur 1 octet)
- `7` indique la taille du message (taille variable, annoncée juste avant)
- `bonjour` le message

➜ **Ce n'est ici qu'un exemple, une proposition, inventez votre propre protocole/encodage :D**

![Pretend](./img/pretend.jpg)

## 5. Envoi d'image

**Euh j'ai trouvé cette lib hihihi** : https://pypi.org/project/ascii-magic/.

Ca convertit des PNG ou des JPG (j'ai testé avec ça) en ASCII art.

Genre de ça :

![Fleur](./img/flower.png)

A ça :

![ASCII Fleur](./img/flower_ascii.png)

➜ **Supporter l'envoi d'image**

- libre à vous de transformer l'image sur le client puis envoyer
- ou envoyer l'image et transformer sur le serveur
- utilisez `ascii-magic` pour la conversion
- les autres clients ont l'ASCII art qui s'affiche

> *Si t'as fait la partie sur l'encodage, on peut imaginer que l'envoi d'une image, c'est le message de type `3`... :)*

## 6. Gestion d'historique

Quand tu rejoins la conversation en retard, t'as pas l'historique, relou.

➜ **Gérer un historique de conversation**

- oui oui y'a déjà les logs, mais tu vas pas envoyer les logs comme ça au client pour qu'il affiche l'historique
- donc : enregistrer les conversations au format JSON côté serveur
  - à chaque réception d'un message, il faut l'enregistrer
  - attention, ça devient vite très violent si vous demandez une lecture puis une écriture sur le disque à chaque réception d'un message...
- quand un nouveau client arrive, lui envoyer en format JSON l'historique
- le client le réceptionne et fait l'affichage nécessaire

![JSON](img/json.png)

## 7. Plusieurs rooms

Quand un client se connecte, après avoir envoyé son pseudo, on lui propose de créer une nouvelle room ou d'en rejoindre une existante.

➜ **Côté serveur**

- entretient une liste des rooms, et qui y est connecté
- quand il reçoit un message, il ne le renvoie qu'aux users de la room concernée
- peut-être intéressant d'ajouter un niveau au dictionnaire `CLIENTS` par exemple : `CLIENTS["room 1"][addr]`

➜ **Côté client**

- le choix de la room se fait de façon synchrone (pas asynchrone) après le choix du pseudo

