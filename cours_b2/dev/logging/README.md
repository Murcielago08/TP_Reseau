# Logging

➜ **Une application qui ne produit pas de logs c'est une application qui n'existe pas.**

C'est tout en fait. Si ton app elle log quedal, on peut pas savoir ce qu'elle fait. Ni pourquoi elle fonctionne, ni pourquoi elle fonctionne pas.

Bref, elle ne sera pas utilisée.

➜ **En Python, il existe une lib dédiée à la journalisation : `logging`.**

Cette lib facilite grandement la gestion des logs dans une application, en intégrant par exemple nativement :

- niveaux de log (WARN, ERROR, INFO, etc)
- formatage de chaque ligne de log
- plusieurs flux de logging (affichage console, fichier, etc)

![Better than print](./img/bt_print.png)

## Sommaire

- [Logging](#logging)
  - [Sommaire](#sommaire)
  - [1. Les objets de la lib](#1-les-objets-de-la-lib)
    - [Mention sur les couleurs](#mention-sur-les-couleurs)
  - [2. Niveaux de log](#2-niveaux-de-log)
  - [3. Format standard d'une ligne de log](#3-format-standard-dune-ligne-de-log)

## 1. Les objets de la lib

La lib définit principalement trois types d'objets :

- les *loggers*
  - utilisé pour logger des trucs
  - c'est cet objet qui a les méthodes `warn()`, `error()`, etc.
  - en appelant ces méthodes, on log des messages
- les *handlers*
  - un objet qui va gérer UNE sortie de log
  - il gère par exemple la sortie console
  - ou la sortie dans un fichier
- les *formatters*
  - permet de définir le format d'une ligne de log

TALK IS CHEAP SHOW ME THE CODE

```python
import logging

# on instancie un objet logger avec un nom arbitraire
# on peut donc en créer autant qu'on veut, qui feront des logs différents
meow_log = logging.getLogger('meow')

# un format pour les logs
meow_format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

# on crée un handler qui va gérer la sortie console
console_handler = logging.StreamHandler()
# on indique quel format doit utiliser ce handler
console_handler.setFormatter(meow_format) 

# un deuxième handler pour AUSSI log dans un fichier
file_handler = logging.FileHandler("./meow.log")
file_handler.setFormatter(meow_format)

# ajout des deux handlers au logger
meow_log.addHandler(console_handler)
meow_log.addHandler(file_handler)

# log something
meow_log.debug("meo")
meow_log.info("meo")
meow_log.warning("meo")
meow_log.error("meo")
```

### Mention sur les couleurs

➜ Attention les **couleurs** ne sont pas une feature des logs ou quoique ce soit, c'est une feature de votre **terminal**.

Il est donc préférable de gérer des logs en couleur uniquement en sortie console et pas dans des fichiers, pitié.

## 2. Niveaux de log

Il existe des niveaux de log, plutôt standards, on note en particulier :

- **Debug** : message pour le dév. Généralement, on log pas en debug par défaut, juste si on a besoin de... debug.
- **Info** : message pour le dév/l'admin qui héberge le truc. L'app indique verbeusement ce qu'elle fait (chaque opération réalisée par exemple)
- **Warning** : signalement d'un problème potentiel. C'est pas bloquant, mais c'est chiant.
- **Error** : un problème a eu lieu. Ca peut être bloquant. Le programme est susceptible d'avoir quitté/crashé après avoir généré cette ligne suivant la gravité de l'erreur.

> [Cette section de la doc Python en parle.](https://docs.python.org/3/library/logging.html#logging-levels)

## 3. Format standard d'une ligne de log

Il existe plusieurs standards concernant les lignes de logs.

Un qui est particulièrement utilisé est le standard Syslog :

```
1 2023-10-11T22:14:15.003Z it4.nowhere test.py 35432 test app says hello
```

➜ on repère quelques éléments essentiels :

- le niveau de log, c'est le `1` tout au début
- le timestamp (la date quoi) dans un format standard `2023-10-11T22:14:15.003Z`
- la machine qui a généré la ligne `it4.nowhere`
- le programme qui a généré la ligne `test.py`
- le PID du programme `35432`
- le message de log `test app says hello`

➜ libre à vous d'en utiliser un autre mais garder à l'esprit :

- **le minimum syndical**
  - un timestamp
  - un message de log
  - un niveau de log
- **un jour peut-être ces logs seront récupérés et centralisés**
  - important de respecter un format standard
  - sinon les mecs qui centralisent les logs ils sont pas heureux
- **pour s'y retrouver, communiquer et faire les choses de façon élégantes**
  - respectez les standards ;)
