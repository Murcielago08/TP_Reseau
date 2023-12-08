# TP4 DEV : I'm Socketing, r u soketin ?

- [TP4 DEV : I'm Socketing, r u soketin ?](#tp4-dev--im-socketing-r-u-soketin-)
- [I. Simple bs program](#i-simple-bs-program)
  - [1. First steps](#1-first-steps)
  - [2. User friendly](#2-user-friendly)
  - [3. You say client I hear control](#3-you-say-client-i-hear-control)
- [II. You say dev I say good practices](#ii-you-say-dev-i-say-good-practices)
  - [1. Args](#1-args)
  - [2. Logs](#2-logs)
    - [A. Logs serveur](#a-logs-serveur)
    - [B. Logs client](#b-logs-client)
    - [C. NOTE IMPORTANTE](#c-note-importante)
- [III. COMPUTE](#iii-compute)


Dans ce TP on va rentrer dans le vif du sujet et créer une interaction entre deux programmes Python, grâce au réseau. On va donc créer un client et un serveur. Pour ça on va utiliser la librairie `socket`.

Dans tout ce TP, vous aurez à chaque fois deux feuilles de code pour faire vos tests :

- **une qui s'exécute sur le serveur : `bs_server.py`**
  - il devra s'exécuter sur une machine Rocky
- **une qui s'exécute sur le client : `bs_client.py`**
  - il devra d'exécuter sur une autre machine virtuelle, peu importe l'OS
  - Linux quand même, comme ça on reste dans un environnement similaire pour tous
  - vous pouvez utiliser un OS graphique si vous le souhaitez : plus proche du monde réel pour le client !
- on va faire évoluer ces deux fichiers au fil du TP
  - pour le rendu, gardez à chaque fois les versions intermédiaires que je vous demande de coder
  - la plupart des 🌞 c'est un fichier de code Python que je veux voir dans le dépôt git de rendu de toute façon !

![Client/Server](./img/calf-cow.jpeg)

> J'ai séparé les trois parties du TP en trois docs pour épurer un peu le bail !

# I. Simple bs program

Première partie pour mettre en place un environnement fonctionnel et deux programmes simples qui discutent à travers le réseau.

## 1. First steps

> Référez-vous [**au cours sur les sockets**](../../../../cours/dev/socket/README.md) pour la syntaxe.

🌞 **`bs_server_I1.py`**

- écoute sur une IP spécifique et port 13337 en TCP
- répond automatiquement "Hi mate !" dès qu'un client se connecte
- affiche la réponse des clients qui se connectent

> Il faudra ouvrir ce port dans le *firewall* de la machine.

🌞 **`bs_client_I1.py`**

- se connecte à l'IP spécifique de la VM serveur et au port 13337
- envoie la string "Meooooo !"
- affiche une éventuelle réponse
- quitte proprement

➜ **Pour quitter proprement, on attend pas juste que l'exécution arrive en fin de fichier, mais on quitte explicitement**

- librairie `sys`
- elle contient une méthode `exit()`
- la méthode `exit()` prend un entier en paramètre : le code retour à retourner quand le programme se termine. Pour rappel :
  - `0` veut dire que le programme s'est terminé correctement
  - autre chose veut dire que le programme ne s'est pas terminé correctement

🌞 **Commandes...**

- je veux dans le compte-rendu toutes les commandes réalisées sur le client et le serveur pour que ça fonctionne
- et je veux aussi voir une exécution de votre programme
- oh et je veux un `ss` sur le serveur
  - n'affiche qu'une ligne : celle qui concerne l'écoute de notre programme
  - ajoutez les bonnes options à `ss` ainsi qu'un `| grep ...` pour n'afficher que la bonne ligne

## 2. User friendly

🌞 **`bs_client_I2.py`**

> Vous aurez besoin du [**cours sur la gestion d'erreurs**](../../../../cours/dev/error_handling/README.md) pour cette partie.

- retour visuel
  - afficher un message de succès chez le client quand il se co au serveur
  - le message doit être : `Connecté avec succès au serveur <IP_SERVER> sur le port <PORT>`
  - vous utiliserez un `try` `except` pour savoir si la connexion est correctement effectuée
- le programme doit permettre à l'utilisateur d'envoyer la string qu'il veut au serveur
  - on peut récupérer un input utilisateur avec la fonction `input()` en Python
  - au lancement du programme, un prompt doit apparaître pour indiquer à l'utilisateur qu'il peut envoyer une string au serveur :
    - `Que veux-tu envoyer au serveur : `

🌞 **`bs_server_I2.py`**

- retour visuel
  - afficher un message de succès quand un client se co
  - le message doit être : `Un client vient de se co et son IP c'est <CLIENT_IP>.`
- réponse adaptative
  - si le message du client contient "meo" quelque part, répondre : `Meo à toi confrère.`
  - si le message du client contient "waf" quelque part, répondre : `ptdr t ki`
  - si le message du client ne contient PAS "meo", ni "waf", répondre : `Mes respects humble humain.`

## 3. You say client I hear control

On va ajouter un peu de contrôle pour éviter que notre client fasse nawak à l'utilisation du programme.

🌞 **`bs_client_I3.py`**

- vérifier que...
  - le client saisit bien une string
    - utilisez la méthode native `type()` pour vérifier que c'est une string
  - que la string saisie par le client contient obligatoirement soit "waf" soit "meo"
    - utilisez [**une expression régulière**](https://www.programiz.com/python-programming/regex) (signalez-le moi s'il serait bon de faire un cours sur cette notion)
- sinon lever une erreur avec `raise`
  - choisissez avec pertinence l'erreur à lever dans les deux cas (s'il saisit autre chose qu'une string, ou si ça contient aucun des deux mots)
  - y'a une liste des exceptions natives (choisissez-en une donc) tout en bas du [cours sur la gestion d'erreur](../../../../cours/dev/error_handling/README.md)

> On poussera le contrôle plus loin plus tard.

# II. You say dev I say good practices

## 1. Args

Je veux une vraie gestion d'arguments et d'options sur le serveur ! C'est à dire que quand on lance la commande pour exécuter le serveur, j'aimerai pouvoir préciser sur la ligne de commande le port où je souhaite écouter.

C'est à dire, par exemple, si je veux lancer le serveur pour qu'il écoute sur le port 8888 TCP, j'aimerai pouvoir taper :

```bash
python bs_server.py -p 8888
```

**On utilise [la lib `argparse`](../../../../cours/dev/argparse/README.md) pour faire ça bien en Python !**

🌞 **`bs_server_II1.py`**

- gère l'option `-p` ou `--port`
  - ne tolère qu'un entier passé en argument
  - si c'est inférieur à 0 ou supérieur à 65535
    - afficher `ERROR Le port spécifié n'est pas un port possible (de 0 à 65535).` 
    - quitter avec le code retour 1
  - si c'est entre 0 et 1024 compris
    - afficher `ERROR Le port spécifié est un port privilégié. Spécifiez un port au dessus de 1024.`
    - quitter avec le code retour 2
  - si `-p` n'est pas utilisé, alors le port par défaut c'est `13337`
- gère l'option `-h` ou `--help`
  - affiche un petit help de la commande
  - le format du help doit respecter le format standard avec une ligne de `usage` et la liste des options possibles avec leur utilité
  - inspirez-vous de la sortie de `ls --help`

On devra donc pouvoir faire :

```
$ python bs_server_II1.py -p 8888
```

## 2. Logs

**Allô les dévs ? Ici it4 l'admin qui vous parle. Ils sont où les ptain de logs de votre application bowdel.**

![No logs](../img/nologs.jpg)

Ce qu'on ~~voudrait~~ veut :

➜ **des logs serveur**

- dans la console
- dans un fichier de log

➜ **des logs client**

- PAS dans la console : c'est le client, c'est un moldu, on lui montre R
- dans un fichier de log

---

Chaque ligne de log :

- **doit être *timestamped***
  - préfixée par date et heure, dans un format standard si possible
- **doit être nivelée**
  - je viens d'inventer le terme
  - c'est à dire que vous préciser un niveau de logging

Il existe des standards sur les niveaux de log en informatique. Les trois en gras sont les plus utilisés. En haut le plus critique, en bas, le moins :

- Emergency
- Alert
- Critical
- **Error** : ERROR ou ERR en rouge
- **Warning** : WARNING ou WARN en jaune
- Notice
- **Informational** : INFO en blanc
- Debug

**Toutes les lignes de log de ce TP devront être au format suivant :**

```
yyyy-mm-dd hh:mm:ss LEVEL message
```

Par exemple :

```
2023-11-03 03:43:21 INFO Un client vient de se co et son IP c'est <CLIENT_IP>.
```

### A. Logs serveur

Le serveur va log chacune des actions à la fois dans la console, et aussi dans un fichier.

Ce fichier il est pas à n'importe quel endroit si on utilise un système GNU/Linux, un dossier est dédié aux logs : `/var/log/`.  
On peut donc créer là-bas un sous-dossier pour notre application, et on stocke dedans le fichier de log de notre application.

Vous pouvez faire ça à la main, ou utiliser [**la librairie `logger`**](https://realpython.com/python-logging/), vous êtes libres pour le moment ! (`logger` c'est le feu quand même).

🌞 **`bs_server_II2A.py`**

- ce qui doit générer une ligne de log :
  - `INFO` lancement du serveur
    - `Le serveur tourne sur <IP>:<port>`
  - `INFO` connexion d'un client
    - l'IP du client doit apparaître dans la ligne de log
    - `Un client <IP_CLIENT> s'est connecté.`
  - `INFO` message reçu d'un client
    - `Le client <IP_CLIENT> a envoyé <MESSAGE>.`
  - `INFO` message envoyé par le serveur
    - `Réponse envoyée au client <IP_CLIENT> : <MESSAGE>.`
  - `WARN` aucun client connecté depuis + de 1 minute
    - le message : `Aucun client depuis plus de une minute.`
    - il doit apparaître toutes les minutes si personne ne se co
- en console
  - le mot-clé `INFO` doit apparaître en blanc
  - le mot clé `WARN` doit apparaître en jaune
- dans un fichier
  - le fichier doit être `/var/log/bs_server/bs_server.log`
  - le créer en amont si nécessaire, précisez la(les) commande(s) dans le compte-rendu

### B. Logs client

Les logs du client, c'est que dans un fichier. En effet, que ce soit une app console ou graphique, le client on veut lui montrer que ce qui est directement lié à SON utilisation de l'application. Et pas le reste.   
Donc on lui jette pas les logs et des vilaines erreurs au visage, ni 14000 messages informatifs.

Je vous laisse choisir l'emplacement du fichier de log de façon **pertinente**.

🌞 **`bs_client_II2B.py`**

- ce qui doit générer une ligne de log :
  - `INFO` connexion réussie à un serveur
    - `Connexion réussie à <IP>:<PORT>.`
  - `INFO` message envoyé par le client
    - `Message envoyé au serveur <IP_SERVER> : <MESSAGE>.`
  - `INFO` message reçu du serveur
    - `Réponse reçue du serveur <IP_SERVER> : <MESSAGE>.`
  - `ERROR` connexion au serveur échouée
    - pour le tester, il suffit de lancer le client alors que le serveur est éteint !
    - le message : `Impossible de se connecter au serveur <IP_SERVER> sur le port <PORT>.`
- en console
  - affiche juste `ERROR Impossible de se connecter au serveur <IP_SERVER> sur le port <PORT>.` en rouge quand ça fail (pas de timestamp là)
  - les messages de niveau INFO ne sont pas visibles dans la console du client
- dans un fichier
  - `<DOSSIER_DE_LOG>/bs_client.log`

### C. NOTE IMPORTANTE

**A partir de maintenant, vous savez gérer des logs à peu près proprement.**

Vous allez dév plusieurs machins en cours, vous devrez utiliser exactement la même méthode que précédemment pour générer les logs : timestamp, niveau de log, message, stocké dans un fichier précis etc.

# III. COMPUTE

**Dans cette partie, on va ajouter une "vrai" fonctionnalité au serveur : résoudre des opérations arithmétiques que le client lui envoie.** Coder une calculette réseau quoi. Ca c'est une folie dis-donc. Encore une fois, on y va petit à petit pour introduire les nouvelles notions une à une.

> *Puis plus tu dév, plus t'es bon. La répétition fait le travail. Et le fait de se creuser la tête sur des problèmes de merde une fois, c'est les résoudre instantanément toutes les fois suivantes.*

DONC dans cette partie, on va faire évoluer simplement le serveur pour qu'il résolve des opérations arithmétiques simples que lui envoie le client.

**Par exemple**, si le client envoie au serveur `2 + 2`, alors le serveur répondra `4`.

![Maths.](../img/compute.jpg)

🌞 **`bs_client_III.py`**

- doit générer des logs
- demande au client de saisir une opération arithmétique
- ajoutez du contrôle (expression régulière) pour ne tolérer que :
  - additions, soustractions, multiplications
  - des nombres entiers compris entre -100000 et +100000

🌞 **`bs_server_III.py`**

- doit générer des logs
- récupérez le code de `bs_server_II2A.py` si vous voulez mais enlevez tout ce qui est en rapport avec les meos et les wafs, on fait une calculette ici !
- la string qu'envoie le client, il faut l'interpréter comme un calcul pour stocker le résultat dans une variable
- en Python y'a par exemple la fonction native `eval()` qui permet de faire ça

```python
>>> client_request = "3 + 3"
>>> result = eval(client_request)
>>> print(result)
6
```
