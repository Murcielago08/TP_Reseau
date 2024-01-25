# Websocket

## 1. Contexte

➜ **Les Websockets c'est une techno de plus en plus en vogue car elle permet des comportements que HTTP ne supporte pas.**

On parle par exemple du fait qu'un serveur peut envoyer un message à un client qui n'a rien sollicité. Là où, avec HTTP, on est dans un modèle où c'est systématiquement le client qui d'abord effectue une requête, pour qu'ensuite le serveur lui réponde.

Ouais mais avec ce modèle de HTTP, comment tu fais pour push une notification sur le smartphone de tes clients ? Faut qu'ils fassent une requête toutes les 5 secondes pour voir s'il y a pas de nouvelle notif ? Vous avez pas trouvé plus dégueu ?

Donc Websockets à la rescousse.

> Pour vous qui avez travaillé avec des sockets TCP, vous allez voir que c'est assez similaire à utiliser.

## 2. Intro technique

Les Websockets c'est donc une alternative au protocole HTTP.

➜ **Bon concrètement c'est quoi HTTP ?**

Un protocole **très simple** (`GET /` c'est compliqué ?) qui permet de télécharger des fichiers.

`1.` Le client effectue une requête HTTP vers un serveur pour indiquer quel fichier il souhaite télécharger. Eventuellement, il y a des métadonnées dans l'en-tête HTTP.

`2.` Le serveur lui répond avec une réponse HTTP qui contient le fichier demandé. Eventuellement, il y a des métadonnées dans l'en-tête HTTP.

Une requête, une réponse. Nice and easy, mais si le serveur veut envoyer des nouvelles datas au client de lui-même c'est impossible : il doit attendre que le client effectue une requête.

➜ **HTTP est encapsulé dans du TCP**

HTTP met en place de la compression, une gestion de session, d'encodage, de headers à taille variable, bref il automatise tout ce qu'on a fait à la main dans les premiers TPs.

Il est lui-même encapsulé dans du TCP. HTTP c'est un protocole standard qui remplace nos encodages maison de début de cours.

➜ **Websocket alors ?**

Ca remplace HTTP mais ça ne repose pas sur un modèle de requête/réponse. Le client se connecte au serveur et maintient la connexion établie (c'est pas juste ponctuel requête/réponse/orvoar).

Il fait tout pareil que HTTP : compression, gestion de sessions, chiffrement, etc.

MAIS le serveur et le client échangent des données librement : à n'importe quel moment l'un ou l'autre peut envoyer des données à son partenaire.

➜ **Gestion d'évènements**

Contrairement à avant où le client n'avait une activité que ponctuelle (il fait sa requête, il obtient sa réponse, au revoir) maintenant avec des Websockets il doit être attentif aux messages qui arrivent du serveur.

Les langages/librairies qui nous donnent accès aux Websockets permettent de gérer la réception d'un message à travers un Websocket.

Ainsi, le client peut réagir à la réception d'un message du serveur.

➜ **Le flow typique**

- le client se connecte à un serveur HTTP
- il effectue une multitude de requêtes successives pour construire la page en entier
  - le serveur répond à chaque requête HTTP par une réponse HTTP avec le contenu du fichier demandé

> *Par exemple pour afficher une belle interface de tracing GPS.*

- une fois l'échange terminé, on passe sur un échange WebSockets
  - ainsi le serveur peut envoyer des nouvelles données quand il le veut
  - et le client pourra injecter ces nouvelles données dans la page

> *Par exemple, mettre à jour la position GPS sur notre belle interface de tracking : le serveur envoie la nouvelle position, et le client met à jour la page (pas de refresh) avec les nouvelles données.*

## 3. Show me the cooooode

Talk is cheap, show me the code.

> [La doc officielle de la lib Websocket Python](https://websockets.readthedocs.io) est super courte, concise, et claire, je vous copie/colle les exemples de là en bas en direct.

En Python, pour un serveur Websocket :

```python
# from https://websockets.readthedocs.io/en/stable/howto/quickstart.html
import asyncio
import websockets

async def hello(websocket):
    name = await websocket.recv()
    print(f"<<< {name}")
    greeting = f"Hello {name}!"
    await websocket.send(greeting)
    print(f">>> {greeting}")


async def main():
    async with websockets.serve(hello, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
```

Et pour le client :

```python
# from https://websockets.readthedocs.io/en/stable/howto/quickstart.html
import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f">>> {name}")

        greeting = await websocket.recv()
        print(f"<<< {greeting}")

if __name__ == "__main__":
    asyncio.run(hello())
```

Après avoir poncé du TCP je pense que c'est trivial de faire ça maintenant !

> *Encore une fois, gardez à l'esprit que ça ne remplace pas TCP, car ce trafic Websocket circule DANS du TCP. Ouvrez Wireshark pour les curieux :)*
