# Enumération Linux

➜ **Un petit doc écrit qui répertorie quelques bons réflexes à avoir pour faire de l'énumération en local sur un système Linux**

Ce qu'on entend par "énumération" c'est : prendre un maximum d'informations sur la machine.

➜ **C'est dans un contexte où on arrive (légitimement ou non) sur une machine inconnue, et qu'on aimerait prendre des infos** en local pour savoir ce qu'il est possible de réaliser

> Dans notre cours, on pense au TP5 où il était possible de récolter des infos sur la machine une fois que vous aviez un shell. TP6 pour l'épreuve root-me ARP poisoning c'est pareil. On se retrouve sur une machine inconnue.

## 1. Basics

```bash
# on est loggés avec quel user ?
whoami
id -un
sudo -l # est-ce qu'on a le droit d'utiliser sudo ?
env # y'a des variables d'environnements définies ?

# d'autres users ?
cat /etc/passwd # liste users
cat /etc/shadow # liste hashes des password des users
who # voir les autres sessions utilisateur
w # voir les autres sessions utilisateur
last # voir les dernières connexions
ls /home

# c'est quel OS ?
cat /etc/issue
cat /etc/os-release
cat /etc/*-release # parfois y'a des /etc/debian-release par ex

# quel kernel ?
uname
uname -ar

# quelques infos sur le système
cat /proc/cpuinfo # infos CPU
free -mh # infos RAM
mount # infos sur les partitions montées
df -h # infos sur les partitions montées
lsblk # infos sur les périphériques de stockage dispos
ip a  # infos sur le réseau
ifconfig # infos sur le réseau
ss -lantu # infos sur les ports en écoute
ss -antu # infos sur les connexions client
ps -ef # processus en cours d'utilisation

# systemd
systemctl list-units --all # liste toutes les unités
systemctl list-units --all -t service # uniquement les services

# liste des paquets installés
dpkg -l # systèmes debian
rpm -qa # systèmes redhat

# liste des tâches planifiées
crontab -l
ls -al /etc/crontab*
systemctl list-timers

# firewall
iptables -vnL # iptables ?
nft tables list # nftables (remplaçant d'iptables) ?

ufw status # ufw ajouté ?
firewall-cmd --list-all # firewalld ajouté ?

# langages : quels langages sont installés ?
bash
python
php
perl
node
[...]
```

## 2. Privilege escalation

➜ **On appelle *privilege escalation* le fait de passer d'un utilisateur qui a des droits restreints à un utilisateur qui a des droits moins restreints**

Evidemment, la *privilege escalation* qui permet de devenir `root` est la plus recherchée quand on accès à un système.

> Il suffit par exemple d'avoir accéder à `sudo` sans password et on peut considérer qu'on a une *privilege escalation*.

➜ **C'est dans un contexte où vous avez un utilisateur restreint sur la machine où vous vous trouvez**

Et vous aimeriez obtenir + de droits, dans l'idéal accéder aux soirts de `root`.

Je vous redirige vers [ce très bon doc sur HackTricks](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/) une fois de plus pour avoir une liste assez conséquente d'une myriade de méthodes pour effectuer une *privilege escalation* sous un système GNU/Linux.

Ils ont aussi dév [un ptit script `LinPEAS`](https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS) qui permet d'automatiquement détecter sur une machine si l'une des méthodes listées sur HackTricks est disponible  pour avoir une *privilege escalation*.

> Un puit sans fond pour apprendre de nouvelles choses purement techniques sur la sécu d'un système GNU/Linux ce p'tit lien !

## 3. Scan externe

S'il y a possibilités, on va pouvoir effectuer des scans NMAP depuis cette machine pour éventuellement en trouver d'autres autour et pouvoir basculer.

Là encore, je vous renvoie vers [le très bon Hacktricks qui répertorie un bon florilège de scans utiles](https://book.hacktricks.xyz/generic-methodologies-and-resources/pentesting-network), ou [directement la doc de NMAP rédigée en français pour votre plus grand plaisir](https://nmap.org/man/fr/index.html) et qui est plutôt cool.
