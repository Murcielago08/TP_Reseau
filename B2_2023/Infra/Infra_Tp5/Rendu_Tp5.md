# Rendu Tp5 Reseau

# Sommaire 

- [Rendu Tp5 Reseau](#rendu-tp5-reseau)
- [Sommaire](#sommaire)
- [I. Tester](#i-tester)
- [II. Intégrer](#ii-intégrer)
  - [1. Environnement](#1-environnement)
  - [2. systemd service](#2-systemd-service)
    - [B. Service basique](#b-service-basique)
    - [C. Amélioration du service](#c-amélioration-du-service)
  - [3. Monitoring](#3-monitoring)
- [III. Héberger](#iii-héberger)
  - [1. Interface bridge](#1-interface-bridge)
  - [2. Firewall](#2-firewall)
  - [3. Serveur SSH](#3-serveur-ssh)
  - [4. Serveur Calculatrice](#4-serveur-calculatrice)

# I. Tester

Dans cette partie, on va déjà essayer de lancer l'application vitefé, voir si elle fonctionne à peu près correctement.  
**Juste : eske sa march enfet ?**

Tout se fait depuis la VM `hosting.tp5.b1`.

---

🌞 **Récupérer l'application dans la VM `hosting.tp5.b1`**

- je vous file le lien de l'app en cours

```bash
[joris@hostingtpb1 python_app]$ ls
client.py  server.py
```

---

🌞 **Essayer de lancer l'app**

- bah juste lance le !
- c'est le **serveur** qu'il faut lancer
- il faut :
  - déterminer dans quel langage est codé l'application
  - éventuellement lire le code vitefé, mais c'est pas le but
  - juste lancer avec une commande adaptée !

```bash
c'est en python vu le 
[joris@hostingtpb1 python_app]$ python server.py
13337
Le serveur tourne sur 10.1.1.20:13337
```

- une commande `ss` qui me montre que le programme écoute derrière IP:port
  - il faut ajouter des options à `ss` pour voir cette info
  - je peux vous les remémorer si besoin, appelez-moi

```bash
[joris@hostingtpb1 python_app]$ ss -alnp | grep python
tcp   LISTEN 0      1                                       10.1.1.20:13337            0.0.0.0:*    users:(("python",pid=11443,fd=4))
```


> Si des erreurs apparaissent au lancement du serveur, il faudra les traiter !

---

🌞 **Tester l'app depuis `hosting.tp5.b1`**

- maintenant, on lance le **client**
- et vous essayez d'utiliser l'application

```bash
[joris@hostingtpb1 python_app]$ python client.py
Veuillez saisir une opération arithmétique : 10+5

[joris@hostingtpb1 python_app]$ python client.py
Veuillez saisir une opération arithmétique : 10+10
```

➜ **Note :**

- le client va essayer spontanément de se connecter à une adresse IP spécifique (celle choisie par le dév pour ses tests) et un port spécifique
- **il sera peut-être nécessaire d'éditer vitefé le code** pour que le client se connecte à une autre IP
- par exemple `127.0.0.1` pour qu'il se connecte au serveur qui tourne en local sur la machine

> Si des erreurs apparaissent au lancement du client, il faudra les traiter !

➜ Vous passez à la suite que si vous arrivez à lancer le serveur, que le client se connecte, et que vous pouvez utiliser l'app ! (et quelle app !)

---

# II. Intégrer

Ce qu'on appelle l'intégration d'une application, c'est le fait de l'installer mais aussi de l'adapter aux règles et bonnes pratiques d'une infrastructure donnée.

Il existe en effet des bonnes pratiques partagées par à peu près tous les admins, mais aussi des règles spécifiques à un environnement ou un autres. On peut par exemple imaginer des règles de sécu plus restrictives pour une infrastructure qui gère des données médicales.

Ici on va se cantonner à des réflexes assez élémentaires :

- on va **créer un *service* systemd**
  - pour gérer plus facilement le serveur
  - le gérer de façon unifiée, comme n'importe quel autre service de la machine
  - proposer des politiques de restart par exemple
- et **monitoring du port TCP** sur lequel le serveur écoute
  - on monitore pour avoir des infos au moins si le service tombe
  - on met en place cette surveillance avec mon copain Netdata

## 1. Environnement

Petite section pour préparer un environnement correct. On va faire le strict minimum.

C'est une application installée à la main, on va la positionner un peu à l'arrache dans `/opt`.

---

🌞 **Créer un dossier /opt/calculatrice**

- il doit contenir le code de l'application

```bash
[joris@hostingtpb1 ~]$ cd /opt/calculatrice/
[joris@hostingtpb1 calculatrice]$ ls
client.py  server.py
```

## 2. systemd service

Dans cette section, on va créer un fichier `calculatrice.service` qui nous permettra de saisir des commandes comme :

```bash
$ sudo systemctl start calculatrice
$ sudo systemctl enable calculatrice

$ sudo journalctl -xe -u calculatrice
```

---

### B. Service basique

🌞 **Créer le fichier `/etc/systemd/system/calculatrice.service`**

- vous devrez apposer des permissions correctes sur ce fichier
  - c'est quoi "correctes" ?
  - go faire un `ls -al` dans le dossier pour voir les permissions des autres fichiers `.service` déjà présents et faire pareil

```bash
[joris@hostingtpb1 system]$ ls -al /etc/systemd/system/
total 8
lrwxrwxrwx. 1 root root   40 Nov 28 11:05 calculatrice -> /etc/systemd/system/calculatrice.service
-rwxrwxrwx. 1 root root    0 Nov 28 10:51 calculatrice.service
lrwxrwxrwx. 1 root root   37 Nov 26  2022 ctrl-alt-del.target -> /usr/lib/systemd/system/reboot.target

```

- un contenu minimal serait :

```bash
$ sudo cat /etc/systemd/system/calculatrice.service
[Unit]
Description=Super calculatrice réseau

[Service]
ExecStart=/usr/bin/python /opt/calculatrice/bs_server.py

[Install]
WantedBy=multi-user.target
```

> On préfère utiliser le chemin absolu vers `python` plutôt que juste écrire la commande. Cela permet d'éviter des soucis s'il existe plusieurs version de Python installée par exemple. Sur certaines versions de systemd, ça marche carrément pas si on précise pas le chemin absolu.

➜ **Il est nécessaire** de taper la commande `systemctl daemon-reload` dès qu'on modifie un fichier `.service` pour indiquer à systemd de relire les fichiers et adopter la nouvelle configuration.

```bash
[joris@hostingtpb1 system]$ sudo cat /etc/systemd/system/calculatrice.service
[Unit]
Description=Super calculatrice réseau

[Service]
ExecStart=/usr/bin/python /opt/calculatrice/bs_server.py

[Install]
WantedBy=multi-user.target

[joris@hostingtpb1 system]$ sudo systemctl daemon-reload
```

---

🌞 **Démarrer le service**

- avec une commande `sudo systemctl start calculatrice`
- prouvez que...
  - le service est actif avec un `systemctl status`
  - le service tourne derrière un port donné avec un `ss`
  - c'est fonctionnel : vous pouvez utiliser l'app en lançant le client

```bash
[joris@hostingtpb1 calculatrice]$ sudo systemctl status calculatrice
● calculatrice.service - Super calculatrice réseau
     Loaded: loaded (/etc/systemd/system/calculatrice.service; disabled; pr>
     Active: active (running) since Tue 2023-11-28 11:53:36 CET; 1s ago
   Main PID: 11964 (python)
      Tasks: 2 (limit: 4604)
     Memory: 5.6M
        CPU: 25ms
     CGroup: /system.slice/calculatrice.service
             └─11964 /usr/bin/python /opt/calculatrice/server.py

Nov 28 11:53:36 hostingtpb1 systemd[1]: Started Super calculatrice réseau.
Nov 28 11:53:36 hostingtpb1 python[11964]: Le serveur tourne sur 10.1.1.20:>
lines 1-12/12 (END)
```

---

### C. Amélioration du service

➜ **Redémarrage automatique**

- si un jour le service est down, pour n'importe quelle raison, il serait bon qu'il redémarre automatiquement
- c'est une des features de systemd, on va configurer ça !

🌞 **Configurer une politique de redémarrage** dans le fichier `calculatrice.service`

- ajoutez :
  - une clause `Restart=`
    - qui permet d'indiquer quand restart
    - vous ferez en sorte qu'il restart quand il y a une erreur, n'importe laquelle
    - à mettre dans la section `[Service]` du fichier
  - une clause `RestartSec=`
    - permet d'indiquer au bout de combien de secondes le service sera relancé
    - on part pour 30 secondes
    - n'hésitez pas à réduire pour vos tests au début, mais je veux 30 sec dans le compte-rendu :)
    - à mettre dans la section `[Service]` du fichier
- un `cat` du fichier pour le compte-rendu

```bash
[joris@hostingtpb1 calculatrice]$ sudo cat /etc/systemd/system/calculatrice.
service
[Unit]
Description=Super calculatrice réseau

[Service]
ExecStart=/usr/bin/python /opt/calculatrice/server.py
Restart=on-failure
RestartSec=30s
[Install]
WantedBy=multi-user.target
```

> [Référez-vous à cette page de la doc officielle de systemd](https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html) pour + d'informations sur ces clauses. Notamment savoir quoi écrire pour `Restart=`.

---

🌞 **Tester que la politique de redémarrage fonctionne**

- lancez le service, repérer son PID, et tuer le process avec un `kill -9 <PID>`

```bash
[joris@hostingtpb1 calculatrice]$ sudo kill -9 11964
sudo kill -9 11964
[joris@hostingtpb1 calculatrice]$ sudo systemctl status calculatrice
● calculatrice.service - Super calculatrice réseau
     Loaded: loaded (/etc/systemd/system/calculatrice.service; disabled; pr>
     Active: activating (auto-restart) (Result: signal) since Tue 2023-11-2>
    Process: 11964 ExecStart=/usr/bin/python /opt/calculatrice/server.py (c>
   Main PID: 11964 (code=killed, signal=KILL)
        CPU: 26ms

Nov 28 11:58:39 hostingtpb1 systemd[1]: calculatrice.service: Main process >
Nov 28 11:58:39 hostingtpb1 systemd[1]: calculatrice.service: Failed with r>
lines 1-9/9 (END)
```

- attendre et vérifier que le service redémarre

```bash
[joris@hostingtpb1 calculatrice]$ sudo systemctl status calculatrice
● calculatrice.service - Super calculatrice réseau
     Loaded: loaded (/etc/systemd/system/calculatrice.service; disabled; pr>
     Active: active (running) since Tue 2023-11-28 11:59:09 CET; 45s ago
   Main PID: 11987 (python)
      Tasks: 2 (limit: 4604)
     Memory: 5.6M
        CPU: 26ms
     CGroup: /system.slice/calculatrice.service
             └─11987 /usr/bin/python /opt/calculatrice/server.py

Nov 28 11:59:09 hostingtpb1 systemd[1]: calculatrice.service: Scheduled res>
Nov 28 11:59:09 hostingtpb1 systemd[1]: Stopped Super calculatrice réseau.
Nov 28 11:59:09 hostingtpb1 systemd[1]: Started Super calculatrice réseau.
Nov 28 11:59:09 hostingtpb1 python[11987]: Le serveur tourne sur 10.1.1.20:>
lines 1-14/14 (END)
```

---

➜ **Firewall !**

- pour le moment vous avez fait tous les tests localement
  - donc on a pas eu besoin de toucher au firewall
  - le firewall de Rocky Linux ne bloque aucun traffic depuis/vers `127.0.0.1`
- quand on va héberger l'app sur le réseau de l'école et accueillir des clients potentiels, il faudra ouvrir un port firewall

---

🌞 **Ouverture automatique du firewall** dans le fichier `calculatrice.service`

- ajouter une clause `ExecStartPre=` qui ouvre le port dans le firewall
  - faut juste passer en argument la commande à exécuter avant (pre) que le service démarre (start)
  - à mettre dans la section `[Service]` du fichier
- ajouter une clause `ExecStopPost=` qui ferme le port dans le firewall
  - faut juste passer en argument la commande à exécuter après (post) que le service ait quitté (stop)
  - c'est trigger quand on `systemctl stop` le service, mais aussi quand il ferme inopinément (comme notre `kill -9` juste avant)
  - à mettre dans la section `[Service]` du fichier
- un `cat` du fichier pour le compte-rendu

```bash
[joris@hostingtpb1 calculatrice]$ sudo cat /etc/systemd/system/calculatrice.
service
[Unit]
Description=Super calculatrice réseau

[Service]
ExecStart=/usr/bin/python /opt/calculatrice/server.py
Restart=always
RestartSec=5s
ExecStartPre=/usr/bin/firewall-cmd --add-port=13337/tcp
ExecStopPost=/usr/bin/firewall-cmd --remove-port=13337/tcp

[Install]
WantedBy=multi-user.target
```

> Préférez utiliser le chemin absolu vers `firewall-cmd` plutôt que juste écrire la commande. Utilisez `which firewall-cmd`  dans votre terminal pour connaître le chemin vers la commande.

---

🌞 **Vérifier l'ouverture automatique du firewall**

- lancer/stopper le service et constater avec un `firewall-cmd --list-all` que le port s'ouvre/se ferme bien automatiquement

```bash
[joris@hostingtpb1 calculatrice]$ sudo systemctl status calculatrice
● calculatrice.service - Super calculatrice réseau
     Loaded: loaded (/etc/systemd/system/calculatrice.service; disabled; pr>
     Active: active (running) since Tue 2023-11-28 12:32:20 CET; 13s ago

[joris@hostingtpb1 calculatrice]$ sudo firewall-cmd --list-all
public (active)
  ports: 13337/tcp

[joris@hostingtpb1 calculatrice]$ sudo kill 12309
[joris@hostingtpb1 calculatrice]$ sudo firewall-cmd --list-all
public (active)
  ports:

[joris@hostingtpb1 calculatrice]$ sudo systemctl status calculatrice
● calculatrice.service - Super calculatrice réseau
     Loaded: loaded (/etc/systemd/system/calculatrice.service; disabled; pr>
     Active: active (running) since Tue 2023-11-28 12:33:17 CET; 12s ago

[joris@hostingtpb1 calculatrice]$ sudo firewall-cmd --list-all
public (active)
  ports: 13337/tcp
```

- tester une connexion depuis **votre PC**
  - récupérer le client sur votre PC
  - le lancer en lui indiquant de se connecter à l'IP de la VM
  - accéder au service

```bash
PS C:\Users\darkj\OneDrive\Bureau\Doc Ynov\Programmation\TP_Reseau> python .\B2_2023\Infra_Tp5\python_app\client.py
Veuillez saisir une opération arithmétique : 10+5
```

---

## 3. Monitoring

🌞 **Installer Netdata** sur `hosting.tp5.b1`

- en suivant la doc officielle
- assurez-vous que le dashboard Web est fonctionnel une fois l'install terminée

```
[joris@hostingtpb1 ~]$ curl https://my-netdata.io/kickstart.sh > /tmp/netdata-kickstart.sh && sh /tmp/netdata-kickstart.sh

 OK 
```

---

🌞 **Configurer une sonde TCP**

- c'est à dire qu'on va demander à Netdata de faire une requête TCP vers un port
  - si le port répond, Netdata considère que le service est up
  - sinon, il considère que c'est down
- ça va nous permettre de suivre un peu en temps réel si notre service est accessible depuis le réseau
- [cette section de la doc](https://learn.netdata.cloud/docs/data-collection/synthetic-checks/tcp-endpoints) parle de comment faire, lisez et check les exemples

> Dans le monde réel, le serveur de monitoring qui fait ce genre de checks est souvent installé sur une autre machine. Comme ça on simule vraiment un accès par le réseau à l'application, pour savoir si elle est disponible.

```
[joris@hostingtpb1 netdata]$ sudo cat go.d/portcheck.conf
jobs:
 - name: cal_server
   host: 10.1.1.20
   ports: 13337
```

---

🌞 **Alerting Discord**

- vous connaissez la chanson : j'aimerai que vous récupériez des alertes automatiquement sur Discord
- [cette section de la doc qui en parle](https://learn.netdata.cloud/docs/alerting/notifications/agent-dispatched-notifications/discord)
- testez que vous recevez une alerte quand vous coupez le service, et que votre sonde TCP n'a plus de réponse

```
[joris@hostingtpb1 netdata]$ sudo cat health_alarm_notify.conf
#------------------------------------------------------------------------------
# discord (discordapp.com) global notification options

SEND_DISCORD="YES"
DISCORD_WEBHOOK_URL="weebhook"
DEFAULT_RECIPIENT_DISCORD="alerts"
```

# III. Héberger

Dans cette étape on va **rendre disponible le service Calculatrice au sein du réseau de l'école** grâce à une feature de VBox : les interfaces *bridge*.

Une interface *bridge* permet à la VM d'avoir un accès au réseau physique de l'hôte. Autrement dit, avoir une IP dans le LAN physique de l'hôte, et agir comme si c'était une autre machine du réseau.

Dans notre cas, ça va permettre de rendre le service de calculette accessible sur le réseau de l'école.

---

On parle d'ouvrir la machine sur le réseau de l'école, donc on va aussi s'assurer que vous aurez pas de soucis :

- déjà c'est une VM donc même si un vilain hacker casse tout, il est confiné dans la VM
- on va fermer les ports inutilement ouverts
- on va s'assurer que chaque service est disponible au bon endroit
  - serveur SSH écoute derrière l'IP host-only uniquement
  - serveur Calculatrice écoute derrière l'IP bridge uniquement

## 1. Interface bridge

➜ Conf VM `hosting.tp5.b1`

- éteindre la VM
- la carte NAT ne sera plus utile
- ajoutez lui une nouvelle carte réseau en bridge
- allumez la VM
- récupérez une IP en DHCP sur cette interface
  - vous devriez récup une IP dans la range du LAN de l'école
  - vous devriez avoir un accès internet

## 2. Firewall

🌞 **Assurez-vous qu'aucun port est inutilement ouvert**

```
[joris@hostingtpb1 ~]$ sudo firewall-cmd --list-port
13337/tcp 19999/tcp
```

## 3. Serveur SSH

🌞 **Conf serveur SSH**

- éditer la configuration du serveur SSH `/etc/ssh/sshd_config`
- le serveur doit être disponible uniquement sur la carte host-only (pas sur l'interface bridge)
- n'oubliez pas de redémarrer le serveur pour que ça prenne effet
- prouvez avec un `ss` que ça a pris effet

```
[joris@hostingtpb1 ~]$ sudo systemctl restart sshd
[joris@hostingtpb1 ~]$ ss -tupnl
Netid State  Recv-Q Send-Q  Local Address:Port    Peer Address:Port Process
tcp   LISTEN 0      128         10.1.1.20:22           0.0.0.0:*

```

## 4. Serveur Calculatrice

🌞 **Conf serveur Calculatrice**

- bon les dévs n'ont pas eu la bonté de nous faire un fichier de conf
- donc go éditer le code pour que le serveur n'écoute que sur une seule IP : celle de l'interface bridge
- n'oubliez pas de redémarrer le serveur pour que ça prenne effet
- prouvez avec un `ss` que le changement a bien pris effet

```
[joris@hostingtpb1 ~]$ ss -tupnl
Netid State  Recv-Q Send-Q  Local Address:Port    Peer Address:Port Process
tcp   LISTEN 0      1           10.0.2.15:13337        0.0.0.0:*

```
