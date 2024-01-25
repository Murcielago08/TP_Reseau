# Asynchrone

- [Asynchrone](#asynchrone)
  - [1. Intro](#1-intro)
  - [2. Bénéfices](#2-bénéfices)
  - [3. En Python](#3-en-python)
  - [4. asyncio](#4-asyncio)
    - [A. Utilisation de gather](#a-utilisation-de-gather)
    - [C. Socket TCP](#c-socket-tcp)
  - [5. Autres libs natives](#5-autres-libs-natives)
    - [A. Requêtes HTTP](#a-requêtes-http)
    - [B. Lire ou écrire des fichiers](#b-lire-ou-écrire-des-fichiers)

## 1. Intro

![Asyyyyync](../img/async.jpg)

L'asynchrone est une technique d'exécution concurentielle.

Il ne s'agit pas là d'exécuter vraiment *en parallèle* des choses, mais plutôt de profiter de l'attente produite par certains bouts de code pour faire autre chose.

Par exemple, si un bout de code est chargé de faire 10 requêtes HTTP, il est notoire que ça rame sa mère. Un code classique va exécuter les requêtes les unes après les autres, et va passer la plus grande partie de sa vie à **attendre**. Attendre la réponse du serveur, attendre que l'OS réceptionne, attendre qu'il puisse lire les octets de la réponse. **Attendre**.

Plutôt que de juste **attendre**, on va indiquer dans le code que cette fonction est une fonction qui peut-être, à un moment, va **attendre**.

**On dit que cette fonction est asynchrone.**

Si on demande l'exécution de plusieurs fonctions asynchrones en même temps :

- la première sera exécutée...
- ...si elle se met à attendre, la deuxième sera exécutée tout de suite
- on met à profit le temps d'attente

Pour l'exemple des requêtes HTTP, ça produit **tellement** d'attente qu'on a l'impression que les 10 requêtes s'exécutent en parallèle.

## 2. Bénéfices

Les bénéfices sont multiples.

➜ **Déjà, ui, la perf**

Exécuter concurentiellement c'est poteneitllement réduire le temps de calcul, et ça c'est cool. Faster is better.

➜ **Pas trop de soucis de partage de données**

Y'a **PAS** de parallélisation avec l'asynchrone : les trucs sont toujours exécutés les uns derrière les autres.

Quand tu fais du multiprocess, et que tu veux modifier une variable globale, euh c'est le BIG BORDEL. Il se passe quoi si deux bouts de code *en parallèle* (multiprocess) modifient la même variable en même temps ? Ecrivent dans le même fichier ? Boom.

➜ **On opti des temps d'attente**

C'est la classe en fait, ton CPU c'est un bijou de technologie, il a franchement mieux à faire qu'attendre. Fais le travailler, rentabilise-le, on fait les choses de façon élégante ici monsieur.

## 3. En Python

> Sachez que c'est le bordel l'exécution concurentielle avec Python depuis des années, depuis toujours quoi. MAIS depuis récemment (6 mois/1 an à l'heure de rédaction de ces lignes), de grosses mises à jour sont passées dans Python, et l'asynchrone commence à avoir vraiment la classe. Faites attention aux dates de vos ressources en ligne donc.

En Python, l'asynchrone ça se fait avec les mots clés `async` et `await` pour déclarer des fonctions asynchrones (`async`) et appeler une fonction qui a été déclarée en asynchrone (`await`).

## 4. asyncio

On utilise aussi la librairie `asyncio` pour des comportements plus complexes. Par exemple :

- la gestion de plein de tâches concurrentes avec une mécanique de *loop*
- la gestion de sockets TCP de façon asynchrone
- d'autres facilités liées à l'asynchrone

### A. Utilisation de gather

> La mécanique de *event loop* va devenir obsolète, j'ai décidé de le retirer du cours.

La fonction `asyncio.gather()` prend une liste de fonctions asynchrones en arguments, et les lance de façon concurentielle.

Voyons comment transformer un code synchrone simple, avec deux fonctions à exécuter, en un code asynchrone.

- un code synchrone tout nul :

```python
# sync_count.py
import time

def p1():
    for i in range(5):
        print(i)
        time.sleep(1)

def p2():
    for i in range(5):
        print(i + 10)
        time.sleep(1)

p1()
p2()
```

- transformation en asynchrone :

```python
# async_count.py
import asyncio

# définitions des fonctions en async
async def p1():
    for i in range(5):
        print(i)
        # asyncio.sleep et pas time.sleep
        # await pour indiquer que cette ligne va produire de l'attente
        await asyncio.sleep(1)

async def p2():
    for i in range(5):
        print(i + 10)
        await asyncio.sleep(1)

async def main():
    tasks = [ p1(), p2() ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
```

Exécution :

- version synchrone

```bash
❯ time python sync_count.py
0
1
2
3
4
10
11
12
13
14
python sync_count.py  0.04s user 0.01s system 0% cpu 10.049 total
```

- version asynchrone

```bash
❯ time python async_count.py
0
10
1
11
2
12
3
13
4
14
python async_count.py  0.10s user 0.01s system 2% cpu 5.118 total
```

> La commande `time` n'est pas super fiable, mais là ça done clairement une idée de l'ordre de grandeur : la version asynchrone est allée deux fois plus vite.

### C. Socket TCP

Pour ce qui est des sockets TCP (et UDP), la librairie `asyncio` nous refait aussi avec un armada d'objets et méthodes pour traiter des flux réseau.

Ici, démonstration pour un serveur TCP de la méthode `start_server()`.

Un serveur TCP simple qui, dès qu'il reçoit une connexion, affiche l'IP et le port du client, ainsi qu'un potentiel message envoyé :

> Pas de librairie `socket` donc mais que du `asyncio` à la place !

```python
import asyncio

# cette fonction sera appelée à chaque fois qu'on reçoit une connexion d'un client
async def handle_client_msg(reader, writer):
    while True:
        # les objets reader et writer permettent de lire/envoyer des données auux clients

        # on lit les 1024 prochains octets
        # notez le await pour indiquer que cette opération peut produire de l'attente
        data = await reader.read(1024)
        addr = writer.get_extra_info('peername')

        # si le client n'envoie rien, il s'est sûrement déco
        if data == b'':
            break

        # on décode et affiche le msg du client
        message = data.decode()
        print(f"Received {message!r} from {addr!r}")

        # on envoie le message, ça se fait en deux lignes :
        ## une ligne pour write le message (l'envoyer)
        writer.write(f"Hello client, j'suis le serveur !".encode())
        ## une ligne qui attend que tout soit envoyé (on peut donc l'await)
        await writer.drain()

async def main():
    # on crée un objet server avec asyncio.start_server()
    ## on précise une fonction à appeler quand un paquet est reçu
    ## on précise sur quelle IP et quel port écouter
    server = await asyncio.start_server(handle_client_msg, '127.0.0.1', 8888)

    # ptit affichage côté serveur
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    # on lance le serveur
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    # lancement du main en asynchrone avec asyncio.run()
    asyncio.run(main())
```

## 5. Autres libs natives

### A. Requêtes HTTP

Requêtes HTTP GET en asynchrone et récupération du résultat avec `aiohttp` :

```python
import aiohttp

url = 'https://www.ynov.com'
async with aiohttp.ClientSession() as session:
    async with session.get(url) as resp:
        resp = await resp.read()
        # resp contient le contenu HTML de la page
        print(resp)
```

### B. Lire ou écrire des fichiers

Ecriture ou lecture de fichier en asyncrhone avec `aiofiles` :

```python
import aiofiles

async with aiofiles.open('meo.txt', "w") as out:
    await out.write("meoooow")
    await out.flush() 
```

![Used to promises](./../img/used_to_promises.jpg)
