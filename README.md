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









