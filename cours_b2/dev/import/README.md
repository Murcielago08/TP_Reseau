# `import` et librairies

- [`import` et librairies](#import-et-librairies)
  - [import simple](#import-simple)
  - [import spécifique](#import-spécifique)
    - [Syntaxe](#syntaxe)
    - [Bénéfices](#bénéfices)
  - [Librairies Python](#librairies-python)
    - [Librairies natives](#librairies-natives)
    - [Librairies externes](#librairies-externes)

## import simple

En Python il est possible d'utiliser des librairies externes avec le mot clé `import`.

La syntaxe est la suivante :

```python
import lib
```

La librairie `lib` est ensuite accessible partout dans le code. Si la méthode `lib` contient une fonction `coucou()`, vous pourrez utilisez la fonction avec la syntaxe :

```python
lib.coucou()
```

**Les `import` sont généralement réalisés sur les premières lignes d'une feuille de code Python.**

**Cette syntaxe est pratique pour tester des choses rapidement.** Pour écrire du code sérieux on va voir qu'on préfère une autre syntaxe.

## import spécifique

### Syntaxe

Une librairie peut comporter plusieurs fonctions (et d'autres trucs). Quand on sait à l'avance quelle fonction on va utiliser, on préférera importer comme ceci :

```python
from lib import coucou
```

Ainsi, la fonction `coucou()` sera accessible avec la syntaxe suivante :

```
coucou()
```

Il est possible d'importer plusieurs choses d'une même lib en une seule ligne :

```python
from lib import coucou1, coucou2
```

Les fonctions `coucou1()` et `coucou2()` seront alors accesible dans votre code.

### Bénéfices

C'est juste **mieux** d'utiliser des imports spécifiques car :

- vous maîtrisez votre code : vous importez que ce que vous utilisez
- un `import` ça charge la librairie en mémoire RAM
  - avec la syntaxe `from lib import coucou` on ne charge que la fonction `coucou()` en RAM
  - la perf donc : on charge pas en RAM des trucs inutiles
- ça rend le code explicite : dès les premières lignes on a une idée de ce que la feuille de code va faire

## Librairies Python

On peut distinguer deux catégories de  librairies Python :

- celles qui sont natives
  - c'est à dire : t'installes Python, t'as la lib qui vient avec
- les librairies externes
  - c'est à dire : tu dois installer la lib pour qu'elle soit disponible

### Librairies natives

Les librairies natives ont plusieurs avantages :

- bah c'est natif !
  - rien à install, c'est là
  - très bonne garantie que ça fonctionne : c'est livré avec le langage lui-même
  - c'est stable, c'est beau, on aime
- pour Python qui est un langage cross-platform...
  - ça veut dire que la lib marchera aussi en corss-platform souvent !

### Librairies externes

Bon c'est chiant parce qu'il faut l'installer. Mais tout n'est pas fourni dans les librairies natives pour faire des trucs de ouf facilement.

C'est particulièrement vrai pour Python qui est un langage dont une des principales forces est sa communauté. Donc des libs stylées, y'en a plein.

C'est tellement répandu que comme beaucoup de langage modernes, il existe un gestionnaire de libs dédié au langage.  
Pour Python c'est `pip`. Il est généralement livré quand vous téléchargez Python lui-même.

La syntaxe est la suivante pour installer une lib. Ca s'utilise en ligne de commande :

```bash
# installer une lib Python qui s'appelle super_lib
$ pip install super_lib
```

Comment connaître les libs Python dispos ? T'as besoin de faire un truc en Python, tu demandes à Google comment, et tu verras quelle lib importer pour faire quoi. Une commande `pip install` télécharge la lib depuis les serveurs de gens qui hébergent gracieusement les libs pour tout le monde.

> Y'en a une liste là : http://packages.pypy.org/ pas forcément exhaustive.
