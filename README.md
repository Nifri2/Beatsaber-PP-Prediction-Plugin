# Work in progress project

* [About](#beatsaber-pp-prediction-plugin)
* [Installation](#installation)
  * [Different modes](#different-modes)


# Beatsaber PP Prediction Plugin
Plugin to Predictlive PP Values using a [RandomForestRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html) weightned on 112302 scores from [Scoresaber](https://www.scoresaber.com/).   
This mod also requires [Counters++](https://github.com/Caeden117/CountersPlus) for the menu options.

The RandomForestRegressor runs at about 300 Iterarions (Messured on a Ryzen 5900x) a second while the trained Keras Model runs at 30 Iterations (ong gpu taking up 5 gigs of vram!) a second.   

# Installation
Drag the `PPP.dll` into your BeatSaber mods folder.   
An automatic installation routine will download missing parts.

## Different Modes
In the configuration file ((OR COUNTERS++ SETTIGNS)) `path/to/config.json`, you can choose one of 2 modes. (NAME OF MODE 1) will take your current accuracy `current_points / max_points_until_now` (`max_points_until_now += 115 * max_possible_combo # for every notehit`) to predict scores, (NAME OF MODE 2) will use `current_points / max_points` to get a PP curve like those in Osu! Plugins that builds up over time. that means your PP score will be low for most of the song and climb towards teh end of the song.

# Nerd Stuff
## How it works
The Plugin starts a Flask API written in Python that has been Compiled with [Pyinstaller](https://www.pyinstaller.org/) on Port 8080.   
The API has one endpoint called `/predict` which accepts GET requets and URL the parameters `stars` and  `acc` like `/predict?stars=5&acc=0.9000` to predict the PP of a 5 star map with an accuracy of 90%.   
The plugin sends this data to the API on each note hit and displays the predicted PP.   

On ever note hit event this API is called and the value displayed. Thats it.

## Digging Deeper
Using the data blocks we fitted a RandomForestRegressor and found out that it sucks. Like seriously look at these predicitons.  

The lines are Stars (1-14), X = Acc and Y = PP   

![PP Prediction](https://github.com/Nifri2/Beatsaber-PP-Prediction-Plugin/blob/main/assets/randomforest.png?raw=true)


So we used the dataset to train an AI in Tensorflow that had a WAY better prediciton, but it was slow so we used it to predict a new dataset of 140100 entries. And this one is really accurate.   

![PP Prediction](https://github.com/Nifri2/Beatsaber-PP-Prediction-Plugin/blob/main/assets/Ai-Graph.png?raw=true)
