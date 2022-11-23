# Stage de Loris

## Introduction

Le but de cette page est de laisser quelques notes sur des points que nous allons aborder ensemble durant le stage.

Le but du stage est de faire un petit jeu sympa en python. Bien sur, on ne va pas developper un jeu compliqué qui demande beaucoup de travail et de temps. On fait un jeu faisable en 5 jours. Ce sera de la 2D, et on va utiliser une librairie de jeu en python simple à utiliser. J'ai fait des tests avec plein de lib et je propose qu'on utilise `pyglet`. C'est une librairie pas très puissante mais assez simple pour notre besoin


PS: je n'ai pas l'habitude de faire des doc en Francais, du coup désolé pour le manque d'accents/cédilles... sur les mots francais


 -----------


## Installation des outils
Afin de rendre le travail le plus ergonomique possible, on va utiliser les meme outils pour ce projet.


### **IDE**
  * Nom: `vscode`
  * Download: https://code.visualstudio.com/ 
  * Plugins:
     * `pylance` (Microsoft)
     * `python` (Microsoft)


  * Il faut installer `vscode`. Ca ne devrait pas etre difficile pour toi, meme sous windows. 
  * En revanche pour installer les plugins, dans `vscode`, il te faudra appuyer sur `Ctrl+Maj+x` et tapper `pylance` et cliquer sur `installer`. Faire de meme pour le plugin `python`

*   Checklist:
     - [] Download `vscode`
     - [] Installation `vscode`
     - [] Installation plugin `pylance`
     - [] Installation plugin `python`

 

### **Language**
  * **Nom**:  `Python`:
  * **Installation**: je te laisse faire, choisis la derniere version de python 3.x
  * Une fois l'installation de python faite: 
      * lance `vscode`, 
      * presse `Ctrl+Maj+²`, 
      * Un terminal apparait, vérifie que python est bien installé en tappant
        * ```bash
          python3 --version
          ```
        * La console devrait afficher quelque chose du genre `Python 3.10.6`
  
### **Installation de pyglet**
  * On va se passer d'environnement virtuel pour le moment, et on va installer la lib `pyglet` de facon globale.
  * Pour installer la librairie `pyglet`, on va utiliser `pip` (= `Prefered Installer Program`), l'installeur standard des packages `python`. Du coup, pour instaler `pyglet` tapper dans le terminal de vscode:
    * ```bash
      pip install pyglet --user
      ```
     Vu que tu es sous windows, si ca marche pas, essaie
    * ```bash
      pip3 install pyglet --user
      ```
    si ca marche toujours pas essaye
    * ```bash
      python3 -m pip install pyglet --user
      ```
    * Normalement tout devrait bien se passer, vérifie bien que qu'il est écrit que le package est bien installé.

-----------
## Construction du projet

Maintenant que la partie "`dev-ops`" est faite, on va pouvoir se consacrer à la partie programmation.




# Stage de Loris

## Introduction

Le but de cette page est de laisser quelques notes sur des points que nous allons aborder ensemble durant le stage.

Le but du stage est de faire un petit jeu sympa en python. Bien sur, on ne va pas developper un jeu compliqué qui demande beaucoup de travail et de temps. On fait un jeu faisable en 5 jours. Ce sera de la 2D, et on va utiliser une librairie de jeu en python simple à utiliser. J'ai fait des tests avec plein de lib et je propose qu'on utilise `pyglet`. C'est une librairie pas très puissante mais assez simple pour notre besoin

Dans chaque section, je mettrai une `checklist`, la liste des étapes que tu dois faire.

PS: je n'ai pas l'habitude de faire des doc en Francais, du coup désolé pour le manque d'accents/cédilles... sur les mots francais


 -----------


## Installation des outils
Afin de rendre le travail le plus ergonomique possible, on va utiliser les meme outils pour ce projet.


### **IDE**
  * Nom: `vscode`
  * Download: https://code.visualstudio.com/ 
  * Plugins:
     * `pylance`
     * `python`


  * Il faut installer `vscode`. Ca ne devrait pas etre difficile pour toi, meme sous windows. 
  * En revanche pour installer les plugins, il te faudra appuyer sur `Ctrl+Maj+x` et tapper `pylance` et cliquer sur `installer`. Faire de meme pour le plugin `python`

*   Checklist:
     - [] Download `vscode`
     - [] Installation `vscode`
     - [] Installation plugin `pylance`
     - [] Installation plugin `python`

 

### **Language**
  * **Nom**:  `Python`:
  * **Installation**: je te laisse faire, choisis la derniere version de python 3.x
  * Une fois l'installation de python faite: 
      * lance `vscode`, 
      * presse `Ctrl+Maj+²`, 
      * Un terminal apparait, vérifie que python est bien installé en tappant
        * ```bash
          python3 --version
          ```
        * La console devrait afficher quelque chose du genre `Python 3.10.6`
  
### **Environement virtuel**
  * On va se passer d'environnement virtuel pour le moment, et on va installer la lib `pyglet` de facon globale.
  * Pour installer la librairie `pyglet`, on va utiliser `pip` (= `Prefered Installer Program`), l'installeur standard des packages `python`. Du coup, pour instaler `pyglet` tapper dans le terminal:
    * ```bash
      pip install pyglet --user
      ```
    * Normalement tout devrait bien se passer, vérifie bien que qu'il est écrit que le package est bien installé.

-----------
## Construction du projet

Maintenant que la partie "`dev-ops`" est faite, on va pouvoir se consacrer à la partie programmation.


### Construction du squelette de travail
On va commencer par créer le squelette pour notre jeu. On va avoir besoin de créer une fenetre, afficher des images/animations, recupérer les evenements de la souris, et des infos de debuggage
On a le choix entre `programmation orienté objet`, et `programmation fonctionelle`. Vu que la `programmation orienté objet` demande des connaissances en architecture, on va commencer avec de la `programmation fonctionnelle`.


Dans n'importe qu'elle situation, tu peux (et tu dois) consulter la documentation de `pyglet`, très bien faite, ici:
https://pyglet.readthedocs.io/en/latest/


### 1er exercice: 
 * Lire la doc de Hello World ici:
   * https://pyglet.readthedocs.io/en/latest/programming_guide/quickstart.html#hello-world
   * Créer un script qui
      * crée une fenetre
      * affiche dans la console la position de la souris, a chaque fois que celle ci bouge:
      ```mouse event: positionX=xxx, positionY=xxx``` avec xxx a remplacer bien sur par la vraie position de la souris
      * ainsi que les evenements click gauche et droit:
      ```mouse event: click.LEFT``` ou ```mouse event: click.RIGHT```
  * Tu devrais avoir quelque chose qui ressemble a ceci: ![Exercice1.py](images/exercice1.png)
  * Bien sur, quand tu bouges la souris ou que tu clicks sur la souris, l'evenement doit etre affiché dans le terminal
  * Nomme le fichier `exercice1.py` et envoie le moi sur discord.

----------
### 2eme exercice:
 * En lisant la doc sur les images et les sprites ici: https://pyglet.readthedocs.io/en/latest/programming_guide/image.html
 * En partant de `exercice1.py`
 * Récupere cette image ![resources](images/neon_version.png)
   * Alors cette image peut paraitre assez bizzare, mais si tu regardes bien, elle contient plein de sous images qui representent des éléments du jeu. C'est notre base de données d'images en quelque sorte.
 * La copier dans le meme repertoire que ton script python
 * Afficher cette image en utilisant `pyglet`. Pour cela tu devras créer une image, puis un sprite qui utilise cette image créé
 * Tu devrais avoir quelque chose du genre ![exercice2](images/exercice2.png)
 * Nomme le fichier `exercice2.py` et envoie le moi sur discord

----------
### 3eme exercice:
 * L'idée de cet exercice, c'est d'afficher juste un morceau de l'image de l'exercice2, notre raquette. Cela doit ressembler a ceci ![exercice3](images/exercice3.png)
 * Ceci represente la raquette dans le jeu
 * Pour cette exercice, cherche ou se trouve la raquette dans l'image `neon_version.png`
    * Tu peux lancer l'exercice2, et regarder les coordonnées de la souris pour connaitre les coordonnées et les dimensions de la raquette, tu en auras besoin pour recuperer la bonne region de l'image.
    * Le sprite qui contient la raquette doit s'appeler `racket` (on en aura besoin plus tard)

-----------
### 4eme exercice:
 * Ca y est, on va commencer a interagir avec le jeu.
 * L'idée, c'est que, quand tu bouges la souris, la raquette bouge sur l'axe horizontal
 * Dans la methode `on_mouse_motion`, rajouter la ligne
    * ```racket.x = x```
    * Lancer le script et bouger la souris
    * Normalement, ca y est, tu bouges la racket dans le jeu
----------
### 5eme exercice:
 * On va rajouter la balle
 * Choisis une balle dans l'image `neon_version.png`.
 * Créé son sprite correspondant. Appelle le sprite `ball`
 * Affiche le sprite `ball` pile poil au milieu de la raquette
 * Bien sur, quand la raquette bouge, la balle doit rester au milieu de la raquette.
 * Tu devrais avoir quelque chose qui ressemble a ceci ![exercice5](/images/exercice5.png)

 ### 6eme exercice:
  * On va faire bouger la balle.
  * L'idée, c'est que, quand on click souris gauche, ça lance la balle vers le haut et vers la gauche
  * Quand la balle arrive au coté gauche de la fenetre, il faut qu'elle rebondisse vers la droite.
    * Idem pour en haut, ca doit rebondir vers le bas
    * Idem pour la droite, ca doit rebondir vers la gauche
    * Idem pour quand la balle touche la raquette















