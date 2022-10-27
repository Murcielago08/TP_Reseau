# Serveur VPN

Le but de ce sujet est de monter votre propre serveur VPN.

Il est possiiiible de faire ça avec des VMs, mais c'est vraiment + intéressant si vous avez une serveur distant, disponible sur internet.

Pour ça :

- avoir un PC ou une raspberry à la maison, accessible derrière votre box
- louer un serveur en ligne *(je vous recommande cette option, demandez-moi pour + d'infos)*

En plus de monter un serveur VPN, on va en profiter pour vitefé sécuriser la machine qui accueille le VPN.

> Vous pouvez utiliser n'importe quel OS GNU/Linux sur la machine distante, mais comme pour les cours, je vous recommande Rocky Linux. PAR CONTRE je vous recommande Rocky 8 (on a utilisé Rocky 9 en cours).

L'idée globale est la suivante :

- s'assurer qu'on peut joindre la machine à distance
- s'y connecter en SSH
- mettre en place quelques bonnes pratiques de sécurité
  - gestion d'utilisateurs
  - serveur SSH
- installer le serveur VPN sur la machine à distance
- s'y connecter avec un client adapté

# I. Setup machine distante

Assurez-vous d'être connecté SSH à la machine distante pour la suite.

Vous pouvez sauter cette section si vous voulez, c'est simplement le minimum syndical pour dormir sur ses deux oreilles quand vous avez un serveur en ligne.

## 1. Utilisateurs

➜ **Création d'utilisateur**

- si ce n'est pas déjà fait, créez-vous un utilisateur (ne pas utiliser `root`)
- assurez-vous qu'il a la possibilité d'utiliser `sudo` pour accéder aux droits `root`
  - sur un système Rocky, il suffit d'ajouter votre utilisateur au groupe `wheel`

> Suivant quel hébergeur vous avez choisi c'est possible que ce soit déjà fait.

## 2. Serveur SSH

### A. Connexion par clé

➜ **Génération d'une paire de clé** SUR LE CLIENT

- SUR LE CLIENT, sur votre PC
- je répète, c'est sur le client, sur votre PC
- vous allez générer une clé privée, qui sera un fichier sur votre PC, qui remplacera l'utilisation d'un mot de passe
- on considère que c'est + sécurisé que l'utilisation d'un mot de passe

```bash
# étape à réaliser sur VOTRE PC
$ ssh-keygen -t rsa -b 4096
```

➜ **Assurez-vous d'avoir une connexion sans mot de passe à la machine**

> Vraiment, faitez-le sinon vous bloquerez votre propre accès à l'étape suivante.

### B. SSH Server Hardening

Je vais pas ré-écrire la roue, y'a 10000 articles pour faire ça sur le web. Je vous link [**un fichier de conf**](https://gist.github.com/cig0/d769b26c5f8a79fbd2ff0e635ebe0846) qui contient les clauses importantes à changer dans votre fichier de conf.

> Vous pouvez google "ssh server hardening" et/ou me demander pour + de clarté.

# II. Serveur VPN

Il existe deux solutions de référence dans le monde open-source/Linux pour mettre en place un serveur VPN : OpenVPN et WireGuard. Je vous laisse faire vos propres recherches si vous voulez une idée de la diff

Là non plus je vais pas ré-écrire la roue, je vous renvoie vers [l'excellent **guide de Digital Ocean** pour mettre en place Wireguard sur une machine Rocky 8.](https://www.digitalocean.com/community/tutorials/how-to-set-up-wireguard-on-rocky-linux-8)

Si vous suivez ce guide, vous pouvez sautez la partie concernant l'IPv6, pour mieux maîtriser ce que vous faites.