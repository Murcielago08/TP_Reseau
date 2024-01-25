# Gestion d'erreurs

Dans ce doc, on va parler de gestion d'erreurs. On appelle *exceptions* les erreurs levées par Python.

On cherche à faire principalement deux choses :

➜ **Quand notre programme bug**, on veut gérer la situation

- quand une erreur est générée, si on ne fait rien, le programme arrête de s'exécuter et affiche l'erreur en sortie
- on peut **traiter** ces erreurs pour :
- par exemple que le programme continue de fonctionner malgré tout
- afficher un message d'erreur custom
- c'est avec les mots-clés `try` et `except`

➜ **Générer des erreurs propres** qui ressemblent à des erreurs Python

- ça facilite le débug et ça rend nos logs plus lisibles et standards
- c'est avec le mot-clé `raise`

> *Le nom des erreurs est écrit en `PascalCase`.*

Quand on parle d'erreur ou *exception* Python, on parle par exemple de `TypeError` dans l'exemple suivant :

```python
>>> print('coucou b2' + 3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: can only concatenate str (not "int") to str
```

## 1. Traiter les erreurs

L'idée est la suivante :

- on déclare un bloc `try` dans lequel on sait qu'il y a des lignes qui peuvent fail
- on va *catch* les erreurs avec un bloc `except`
- on peut exécuter une action spécifique quand...
  - une erreur spécifique est levée
  - n'importe quelle erreur est levée

Exeeeeeeemple en ~~image~~ lignes de code ?

### A. Gérer une exception spécifique

```python
a = "Coucou b2"
b = 3

try:
    c = a + b
except TypeError:  # on catch l'exception TypeError
    print("On dirait que les deux variables ne sont pas du même type, déso.")
```

### B. Gérer n'importe quelle exception

```python
a = "Coucou b2"
b = 3

try:
    c = a + b
except:  # on précise pas quelle exception, ça catch tout
    print("On dirait qu'il y a eu un soucis, déso.")
```

### C. Les deux

```python
a = "Coucou b2"
b = 3

try:
    c = a + b

except TypeError:  # on catch l'exception TypeError
    print("On dirait que les deux variables ne sont pas du même type, déso.")

except:  # on précise pas quelle exception, ça catch tout le reste
    print("On dirait qu'il y a eu un soucis, déso.")
```

> On peut déclarer autant de block `except` qu'on veut.

### D. Get informations

Quand on catch une exception, on reçoit un objet de type Exception, qui contient le message d'erreur natif de Python. On peut l'utiliser pour nous aider à débug par exemple !

```python
a = "Coucou b2"
b = 3

try:
    c = a + b

except TypeError:  # on catch l'exception TypeError
    print("On dirait que les deux variables ne sont pas du même type, déso.")

except Exception as e:  # on précise pas quelle exception, ça catch tout le reste
    print("On dirait qu'il y a eu un soucis, déso.")
    print(f"L'erreur native est : {e.message}")
```

## 2. Lever des erreurs

Pour ça, on utilise le mot-clé `raise`. Ca permet de lever des erreurs qui ressemblent aux erreurs natives de Python, et arrêter proprement l'exécution du programme si un problème est rencontré.

```python
a = "Coucou b2"
b = 3

if type(a) is not str:
    raise TypeError("Ici on veut que des strings !")

if type(b) is not str:
    raise TypeError("Ici on veut que des strings !")
```

> Ici, on lève une `TypeError`. **Quand on lève une exception, on fait en sorte d'utiliser celles qui existent déjà dans Python** (comme `TypeError`) et on évite de créer nos propres exceptions (car ui, c'est possible). [Liste des exceptions existantes ici](https://docs.python.org/3/library/exceptions.html#exception-hierarchy).
