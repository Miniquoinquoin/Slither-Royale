# Slither-Royale

## Contexte et définition du projet

### Objectif

Notre objectif est de réaliser un projet qui implique le développement d'un modèle de reinforcement learning (apprentissage par renforcement).

### Critères du projet

Les critères attendus sont les suivants :

- Un résultat visuel, qui peut être facilement présenté à l'oral
- Utilisation de Django
- Implémentation d'un composant réseau
- Un projet réaliste

Notre projet consiste donc à créer un jeu vidéo (visuel) multijoueur (composant réseau).

### Ressources

On dispose de 12 séances de 3h15 pour réaliser le projet, soit environ 36h de travail au total. Le projet sera réalisé en groupe de 3 personnes, ce qui donne une petite centaine d'heures allouées en tout pour le projet.

Les ressources nécessaires au projet sont :

| Ressource | Solution choisie |
| --- | --- |
| Hébergement Django | Une VM hosting de Minet sera privilégiée, pour des raisons de coût : l'hébergement est gratuit pour les adhérents Minet. |
| Librairies utilisées | Nous avons choisi d'utiliser uniquement des librairies sous licence MIT (à compléter avec d'autres licences à droit d'utilisation gratuit), afin de ne pas avoir de problème de droit d'auteur. |
| Entraînement des modèles | L'utilisation de Google Colab est privilégiée pour l'entraînement des modèles, afin de ne pas avoir de problème de ressources matérielles, et de profiter d'infrastructures puissantes mises à disposition gratuitement. |

## Principe du jeu

Slither Royale est une adaptation façon remix de Slither.io en battle royale.

16 joueurs incarnent un serpent (abstrait) vu de dessus, sur une carte circulaire en 2D. Le serpent avance continuellement vers l'avant, et le joueur peut le diriger vers la droite ou la gauche, en direction du curseur de la souris.

Lorsqu'un serpent entre dans un autre serpent (sa tête touche l'autre serpent), il disparaît et perd la partie. L'objectif des joueurs est d'être le dernier serpent sur la carte.

Le joueur est récompensé pour l'élimination d'autres serpents, et un système de zone de jeu est mis en place pour forcer les joueurs à se rapprocher les uns des autres au fur et à mesure que le temps passe.
