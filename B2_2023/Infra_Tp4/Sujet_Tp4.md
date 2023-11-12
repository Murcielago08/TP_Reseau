# TP4 : Router-on-a-stick

On va utiliser GNS3 dans ce TP pour se rapprocher d'un cas réel. La topologie qu vous mettez en place en fin de TP c'est tellement du classique qu'on lui a donné un nom : Router on a Stick.

Un seul routeur, plein de switches, plein de clients, plein de VLANs. Router on a Stick.

On va donc focus sur l'aspect routing/switching, avec du matériel Cisco. On va aussi mettre en place des VLANs, et du routage.

![Sounds be like](./img/cisco_switch.jpg)

# Sommaire

- [TP4 : Router-on-a-stick](#tp4--router-on-a-stick)
- [Sommaire](#sommaire)
- [0. Prérequis](#0-prérequis)
  - [Checklist VM Linux](#checklist-vm-linux)
- [I. VLAN et Routing](#i-vlan-et-routing)
- [II. NAT](#ii-nat)
- [III. Add a building](#iii-add-a-building)

# 0. Prérequis

➜ Les clients seront soit :

- VMs Rocky Linux
- VPCS
  - c'est un truc de GNS pour simuler un client du réseau
  - quand on veut juste un truc capable de faire des pings et rien de plus, c'est parfait
  - ça consomme R en ressources

> Faites bien attention aux logos des machines sur les schémas, et vous verrez clairement quand il faut un VPCS ou une VM.

➜ Les switches Cisco des vIOL2 (IOU)

➜ Les routeurs Cisco des c3640

➜ **Vous ne créerez aucune machine virtuelle au début. Vous les créerez au fur et à mesure que le TP vous le demande.** A chaque fois qu'une nouvelle machine devra être créée, vous trouverez l'emoji 🖥️ avec son nom.

## Checklist VM Linux

A chaque machine déployée, vous **DEVREZ** vérifier la 📝**checklist**📝 :

- [x] IP locale, statique ou dynamique
- [x] hostname défini
- [x] firewall actif, qui ne laisse passer que le strict nécessaire
- [x] on force une host-only, juste pour pouvoir SSH
- [x] SSH fonctionnel
- [x] résolution de nom
  - vers internet, quand vous aurez le routeur en place

**Les éléments de la 📝checklist📝 sont STRICTEMENT OBLIGATOIRES à réaliser mais ne doivent PAS figurer dans le rendu.**

# [I. VLAN et Routing](./1_routing_vlan/README.md)

# [II. NAT](./2_nat/README.md)

# [III. Add a building](./3_second_building/README.md)
