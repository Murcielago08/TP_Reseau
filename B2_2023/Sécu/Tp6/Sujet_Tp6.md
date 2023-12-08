# TP6 : Un peu de root-me

P'tit sujet de TP autour de **plusieurs épreuves [root-me](https://www.root-me.org)**.

**But du TP** : vous pétez les épreuves, je vous accompagne pour le faire, et en rendu je veux un ptit write-up.

> *Un write-up c'est la démarche technique pour arriver à l'objectif avec un peu de blabla pour expliquer ladite démarche.*

Chaque partie correspond à un chall root-me. Je compléterai un peu le sujet de TP au fur et à mesure que vous avancez.

## Sommaire

- [TP6 : Un peu de root-me](#tp6--un-peu-de-root-me)
  - [Sommaire](#sommaire)
  - [I. DNS Rebinding](#i-dns-rebinding)
  - [II. Netfilter erreurs courantes](#ii-netfilter-erreurs-courantes)
  - [III. ARP Spoofing Ecoute active](#iii-arp-spoofing-ecoute-active)
  - [IV. Trafic Global System for Mobile communications](#iv-trafic-global-system-for-mobile-communications)

## I. DNS Rebinding

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/HTTP-DNS-Rebinding)

- utilisez l'app web et comprendre à quoi elle sert
- lire le code ligne par ligne et comprendre chaque ligne
  - en particulier : comment/quand est récupéré la page qu'on demande
- se renseigner sur la technique DNS rebinding

🌞 **Write-up de l'épreuve**

## II. Netfilter erreurs courantes

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/Netfilter-erreurs-courantes)

- à chaque paquet reçu, un firewall parcourt les règles qui ont été configurées afin de savoir s'il accepte ou non le paquet
- une règle c'est genre "si un paquet vient de telle IP alors je drop"
- à chaque paquet reçu, il lit la liste des règles **de haut en bas** et dès qu'une règle match, il effectue l'action
- autrement dit, l'ordre des règles est important
- on cherche à match une règle qui est en ACCEPT

🌞 **Write-up de l'épreuve**

## III. ARP Spoofing Ecoute active

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/ARP-Spoofing-Ecoute-active)

🌞 **Write-up de l'épreuve**

## IV. Trafic Global System for Mobile communications

> [**Lien vers l'épreuve root-me.**](https://www.root-me.org/fr/Challenges/Reseau/Trafic-Global-System-for-Mobile-communications)

🌞 **Write-up de l'épreuve**
