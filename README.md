# Slither-Royale

## Contexte et définition du projet

Notre objectif est de réaliser un projet qui implique le développement d'un modèle de reinforcement learning (apprentissage par renforcement).

Les critères attendus sont les suivants :

- Un résultat visuel, qui peut être facilement présenté à l'oral
- Utilisation de Django
- Implémentation d'un composant réseau
- Un projet réaliste

Notre projet consiste donc à créer un jeu vidéo (visuel) multijoueur (composant réseau).

## Principe du jeu

Slither Royale est une adaptation façon remix de Slither.io en battle royale.

16 joueurs incarnent un serpent (abstrait) vu de dessus, sur une carte circulaire en 2D. Le serpent avance continuellement vers l'avant, et le joueur peut le diriger vers la droite ou la gauche, en direction du curseur de la souris.

Lorsqu'un serpent entre dans un autre serpent (sa tête touche l'autre serpent), il disparaît et perd la partie. L'objectif des joueurs est d'être le dernier serpent sur la carte.

Le joueur est recompenser pour l'elimination d'autres serpents, et un system de zone de jeu est mis en place pour forcer les joueurs à se rapprocher les uns des autres, au fur et à mesure que le temps passe.
