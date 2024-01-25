# Fonctions

J'vous épargne le blabla sur les fonctions ?

Pour déclarer une fonction, on utilise le mot-clé `def`. Et c'est `return` pour retourner une valeur.

Par exemple, une fonction nulle `sum()` qui additionne deux entiers passés en arguments :

```python
def sum(entier1, entier2):
    somme = entier1 + entier2
    return somme

cnullesexemplesdebase = sum(1,3)
print(cnullesexemplesdebase)
```

On peut *typer* les arguments :

- on précise explicitement que tel argument sera un entier, ou une string, ou autre
- code plus propre, plus lisible, plus clair, maîtrisé
- ça throw une erreur si on envoie le mauvais type en argument

```python
def sum(entier1: int, entier2: int):
    somme = entier1 + entier2
    return somme

cnullesexemplesdebase = sum(1,3)
print(cnullesexemplesdebase)
```

Et on peut aussi *typer* le retour de la fonction : indiquer dès la déclaration quel sera le type de la valeur retournée.

```python
def sum(entier1: int, entier2: int) -> int:
    somme = entier1 + entier2
    return somme

cnullesexemplesdebase = sum(1,3)
print(cnullesexemplesdebase)
```

La ligne `def sum(entier1: int, entier2: int) -> int:` ça s'appelle la **signature** de la fonction. Elle doit être unique dans votre code !