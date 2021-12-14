# Beatsaber PP Prediction Plugin
Plugin to Predictlive PP Values using a[RandomForestRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html) weightned on 112302 scores from [Scoresaber](https://www.scoresaber.com/).   

The RandomForestRegressor runs at about 300 Iterarions a second while a trained Keras Model runs at 30 Iterations a second (Messured on a Ryzen 5900x).   

## Installation
add shit here   

## How it works
The Plugin starts a Flask API written in Python that has been Compiled with [Pyinstaller](https://www.pyinstaller.org/) on Port 5000.   
The API has one endpoint called `/predict` which only accepts POST requets with a data structure like `{"stars": 6.68, "acc": 0.8943}`   
The plugin sends this data to the API on each note hit and displays the Predicted PP.

## Digging Deeper
Using the 112302 data blocks we trained a RandomForestRegressor and found out that it sucks. Like seriosly look at these predicitons.   

![PP Prediction](https://github.com/Nifri2/Beatsaber-PP-Prediction-Plugin/blob/main/assets/randomforest.png?raw=true)


So we used the dataset to train an AI in Tensorflow that had a WAY better prediciton, but it was slow so we used it to predict a new dataset of 140100 entries. And this one is really accurate.
![PP Prediction](https://github.com/Nifri2/Beatsaber-PP-Prediction-Plugin/blob/main/assets/Ai-Graph.png?raw=true)
