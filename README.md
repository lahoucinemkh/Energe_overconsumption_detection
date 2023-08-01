# Chicken-Disease-Classification--Project


# Code Descreption 

Ce répertoire regroupe l'ensemble du code d'un projet ambitieux dont le but est de traiter et analyser les problèmes de surconsommation d'énergie. Pour parvenir à ce résultat, le projet s'appuie sur deux approches complémentaires : la programmation en Python traditionnelle et l'apprentissage automatique (machine learning).

Le "interpretation_model.ipynb" contient un code élaboré pour créer un modèle d'apprentissage automatique utilisant l'algorithme SVM (Support Vector Machine). Ce modèle est spécialement conçu pour anticiper et classifier les cas de surconsommation identifiés. Le processus commence par l'importation des données brutes, suivie d'une phase de prétraitement permettant de mettre en forme les informations de manière optimale. Ensuite, le modèle est entraîné et testé avec ces données prétraitées. Une fois que les performances du modèle ont été validées, il est sauvegardé sous forme d'un fichier .pkl, garantissant ainsi sa réutilisation ultérieure.

Le fichier "main.ipynb" représente quant à lui le pilier central de ce projet. Il importe le modèle d'interprétation préalablement entraîné dans "interpretation_model.ipynb". L'étape suivante consiste à créer des classes spécifiques pour regrouper les périodes de surconsommation similaires, tant en termes d'heures que de nuits. Le processus complet est ainsi constitué : à partir des données d'origine, le code détecte les heures de surconsommation pour ensuite les fusionner, permettant ainsi de créer un DataFrame (tableau de données) dans lequel chaque ligne nécessite une catégorisation précise. Pour accomplir cette tâche, le modèle d'apprentissage automatique SVM est de nouveau utilisé pour fournir des prévisions de catégorisation. Ce processus d'analyse est applicable également aux données des dimanches. Enfin, les résultats finaux sont sauvegardés dans un fichier Excel, fournissant ainsi une vue synthétique des résultats obtenus.

Pour faciliter l'interaction avec les utilisateurs, deux fichiers essentiels sont inclus dans le projet : "index.html" et "app.py". La première composante, "index.html", propose une interface utilisateur rudimentaire permettant à l'utilisateur de télécharger un fichier CSV (fichier de données tabulaires) et, une fois l'analyse effectuée, de télécharger le résultat obtenu. Le fichier "app.py" repose quant à lui sur le framework Python Flask, un outil puissant pour le développement web. Il assure la liaison entre la page web et le cœur du projet en prenant en charge le fichier CSV téléchargé par l'utilisateur sur la page web. Une fois le fichier récupéré, "app.py" déclenche l'exécution complète du processus d'analyse en se basant sur le contenu du fichier "main.ipynb". Enfin, le résultat final sous forme de fichier Excel est renvoyé sur la page web, prêt à être téléchargé par l'utilisateur.

Ce projet offre donc une solution complète et interactive pour analyser et anticiper les problèmes de surconsommation d'énergie, en combinant astucieusement la puissance de la programmation Python et l'efficacité de l'apprentissage automatique.


## Workflows

1. Update config.yaml
2. Update secrets.yaml [Optional]
3. Update params.yaml
4. Update the entity
5. Update the configuration manager in src config
6. Update the components
7. Update the pipeline 
8. Update the main.py
9. Update the dvc.yaml


# How to run?
### STEPS:

Clone the repository

```bash
https://github.com/lahoucinemkh/Energe_overconsumption_detection.git
```
### STEP 01- Create a conda environment after opening the repository

```bash
conda create -n suivi python=3.9 -y
```

```bash
conda activate suivi
```


### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```


```bash
# Finally run the following command
python app.py
```

Now,
```bash
open up you local host and port
```

