# Gestion d'arguments et options

Même les programmes les plus évolués se lancent en ligne de commande pour permettre de modifier leur comportement. Ce document vise à présenter brièvement la lib `argparse` prévue à cet effet.

Ici on va survoler, pour avoir les basics, bien comprendre les bases pour construire avec, mais il existe comme toujours [de très bonnes ressources sur le sujet en ligne](https://realpython.com/command-line-interfaces-python-argparse/).

> *Perso j'ai déjà lancé Steam en ligne de commande pour préciser des vilaines options au lancement. Chrome aussi, c'est nécessaire pour lui faire utiliser certaines features. Même des jeux. Juste pour dire que c'est pas un truc sombre d'admin système qui lance des commandes avec 40 options à longueur de journée.*

## 1. Intro

`argparse` permet donc de gérer facilement les options et arguments passés à notre programme.

Tout de suite un exemple, SHOW ME THE CODE :

```python
# On importe la lib argparse
import argparse

# Création d'un objet ArgumentParser
parser = argparse.ArgumentParser()

# On ajoute la gestion de l'option -n ou --name
# "store" ça veut dire qu'on attend un argument à -n
# on va stocker l'argument dans une variable
parser.add_argument("-n", "--name", action="store")

# Permet de mettre à jour notre objet ArgumentParser avec les nouvelles options
args = parser.parse_args()

print(args.name)
```

Et on peut ensuite faire :

```bash
$ python test.py -n meo
meo

$ python test.py
None

$ python test.py -n WOAW
WOAW
```

## 2. Plusieurs arguments

Il est aussi possible de traiter plusieurs arguments

```python
# On importe la lib argparse
import argparse

# Création d'un objet ArgumentParser
parser = argparse.ArgumentParser()

# On ajoute la gestion de l'option -n ou --name
# "store" ça veut dire qu'on attend un argument à -n
# on va stocker l'argument dans une variable
parser.add_argument("-n", "--name", action="store")

# On ajoute la gestion de l'option -s ou --is-set
# "store_true" indique qu'on attend pas d'argument à -s
# on va juste stocker une variable à True si l'option est positionnée
parser.add_argument("-s, --set", action="store_true")

# Permet de mettre à jour notre objet ArgumentParser avec les nouvelles options
args = parser.parse_args()

print(args["name"])
print(args["set"])
```

Bien d'autres tricks sont possibles, parmi lesquels :

- forcer le type d'un argument (entier, string, etc)
- définir une valeur par défaut pour une option si elle n'est pas précisée
- définir des options exclusives l'une de l'autre (si on n'utilie une, l'autre peut pas être utilisée en même temps)
