# Utilisation ARP poisoning

Tout d'abord, il faut commencer le cloner le programme depuis git à l'aide de la commande :
```
git clone https://github.com/MrZerkeur/TP_reseau.git
```

Mais avant de lancer quoi que ce soit, il faut télécharger le bibliothèque scapy avec :
```
pip3 install scapy
```

Puis, il faut se placer dans le bon dossier avec :
```
cd TP5_offensif/
```

Enfin, lancer le porgramme avec :
```
sudo python3 offense.py
```

Il suffit ensuite de suivre les instructions données dans le programme : Le programme va scanner le réseau puis demander à l'utilisateur de choisir sa victime, ainsi que d'indiquer quelle machine est le routeur.

Et voilà ! Les informations envoyées par la victime au routeur et inversement passent maintenant par l'utilisateur ! Il est donc possible d'espionner le trafic.

Bonne utilisation !

*Seulement l'ARP poisoning est présent parce que je n'arrive pas à faire fonctionner netfilterqueue, donc pas de DNS spoofing*

FAIT PAR Axel BROQUAIRE et Joris PELLIER