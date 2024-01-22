# Description du projet

Ce projet consiste à créer une simulation des populations de lapins et de carottes dans un jardin sur une période de six ans, avec des règles spécifiques régissant la durée de vie des lapins, la reproduction et la croissance des carottes. L'objectif est de suivre et de tracer les changements de population chaque semaine à l'aide de Python.


Nous avons utilisé plusieurs fichiers pour ce projet. Le fichier animals.py contient la classe Rabbit la classe Fox et la classe Hunter. Le fichier garden.py contient la classe Carrot et Garden. Le fichier main.py contient le code principal pour exécuter la simulation. Le fichier requirements.txt contient les dépendances du projet. Le fichier README.md contient des informations sur le projet.

# Animals.py

## Gender 

C'est une énumération qui représente le genre. Elle a deux valeurs possibles : MALE et FEMALE.

## Rabbit 

Cette classe représente un lapin. Chaque instance de cette classe a plusieurs attributs, tels que le genre, l'âge, l'état de faim, le nombre de semaines sans nourriture et la dernière semaine de reproduction. Elle a aussi plusieurs méthodes pour vieillir le lapin, le faire manger, vérifier s'il peut se reproduire, s'il est malade ou s'il est mort.


## Fox 

Cette classe représente un renard. Chaque instance de cette classe a une image et un niveau de faim. Elle a une méthode pour chasser les lapins. Si le renard ne mange pas, son niveau de faim augmente. Si le renard mange, son niveau de faim est réinitialisé à zéro.

## Hunter

Cette classe représente un chasseur. Chaque instance de cette classe a une image, un certain nombre de munitions, un intervalle de chasse et la dernière semaine de chasse. Elle a une méthode pour chasser les renards. Si le chasseur peut chasser et qu'il y a des renards, il chasse un renard au hasard, utilise une munition et met à jour la dernière semaine de chasse.

# Garden.py

## La classe Carrot
Pour représenter des carottes individuelles. Cette classe peut être simple car les carottes n'ont pas de comportements complexes.

## La classe Garden

Pour représenter l'environnement du jardin, contenant des lapins et des carottes, et des méthodes pour simuler les activités hebdomadaires (par exemple, faire pousser des carottes, nourrir les lapins).


# Logique de simulation :

Mises à jour hebdomadaires pour le vieillissement, l'alimentation et la reproduction des lapins.
Cycle de croissance et de récolte des carottes.
Suivi des décès de lapins dus à l'âge ou à la faim.
Ajustement des populations de lapins et de carottes en conséquence.


# Visualisation des données :

Utilisation de matplotlib pour représenter graphiquement les populations de lapins et de carottes au fil du temps.

# Bonnes pratiques :

Code propre et lisible avec des conventions de dénomination appropriées.
Documentation et commentaires pour plus de clarté.
Utilisation efficace des structures de données.
Conception modulaire pour faciliter la maintenance et les mises à jour.

Commençons par écrire la structure de base des classes Rabbit, Carot et Garden, ainsi que la boucle de simulation principale. Je fournirai le code de ces composants. Ensuite, nous pourrons discuter et affiner les détails de l'implémentation, tels que la logique de reproduction et d'alimentation.


La structure de base de la simulation du lapin et de la carotte est établie. Les classes Rabit, Carrot et Garden sont définies avec des fonctionnalités de base :


Classe Lapin : Gère le vieillissement, l'alimentation, l'éligibilité à la reproduction et les conditions de mort.
Classe Carotte : Représente les carottes individuelles, actuellement sans attributs spécifiques.
Classe Jardin : Gère la population de lapins et de carottes, y compris les processus d'alimentation et de vieillissement.
La simulation montre une semaine d'activité : les deux lapins initiaux vieillissent d'une semaine, chacun consomme une carotte, ce qui réduit le nombre de carottes de 200 à 198.


Les prochaines étapes sont les suivantes


Implémenter la logique de reproduction pour les lapins, basée sur les critères donnés (âge, disponibilité du partenaire, et mois spécifiques pour la portée).
Implémenter le cycle de croissance des carottes, en s'alignant sur le semis en mars et la récolte en juin.
Je vais procéder à ces implémentations. Une fois qu'elles seront terminées, nous intégrerons le tracé matplotlib et nous peaufinerons les détails supplémentaires. 




La simulation de l'écosystème des lapins et des carottes sur six ans montre un état final avec zéro lapin et zéro carotte au 24 décembre 2028. Ce résultat suggère que la population de lapins pourrait avoir été menacée d'extinction en raison d'un manque de nourriture.

Ce projet consiste à créer une simulation des populations de lapins et de carottes dans un jardin sur une période de six ans, avec des règles spécifiques régissant la durée de vie des lapins, la reproduction et la croissance des carottes. L'objectif est de suivre et de tracer les changements de population chaque semaine à l'aide de Python.

