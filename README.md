<h2> Classification of music by genre using Spotify's metrics and machine learning</h2>

<h3> Overview </h3>

This little personal project was designed solely to test the performance of some machine learning classification algorithms. In order to work with some original dataset (I'm growing tired of MNIST, IRIS, etc) I decided to use the nice Spotify's API to get a few features from some musics. Spotify provides a set of float metrics that describes some relevant characteristics of a music. They are:

1. Danceability;
2. Energy;
3. Key;
4. Loudness;
5. Mode;
6. Speechiness;
7. Acousticness;
8. Instrumentalness;
9. Liveness;
10. Valence;
11. Tempo.

The meaning of each feature can be found on [Spotify Audio Features](https://developer.spotify.com/web-api/get-several-audio-features/)

After deciding the features with which to work, it was time to gather some data and come up with some labels. Assuming there is a real relationship between this set of features and the genre of the music it is used to describe, I used the API to collect as many musics as possible for a pre-defined set of genres, or categories. The ones I've chosen were:

1. Pop;
2. Indie Alt;
3. Punk;
4. Funk;
5. Rock;
6. Hip-Hop;
7. Metal;
8. Country;
9. Jazz;
10. Reggae;
11. Classical;
12. Party;
13. Latin;
14. Romance;
15. Blue.

Due to some different responses in the API, the data collected was not uniform, i.e., some genres have way more instances than others.
The resulting dataset can be summarized as in the figure below.

<img src="https://github.com/lucasbflopes/spotify-api-track-classification/blob/master/dataset/dataset_view.png?raw=true" width="150" align="middle">

The machine learning algorithms selected to attack the aforementioned classification problem were:

* [SVM (Support Vector Machine) with RBF kernel](https://en.wikipedia.org/wiki/Support_vector_machine);
* [Polynomial Logistic Regression](https://en.wikipedia.org/wiki/Logistic_regression);
* [K-Nearest Neighbours](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm);

The [Scikit-Learn library](http://scikit-learn.org/stable/) was used for pre-processing the dataset as well as implementing said algorithms. 

After analyzing the cross validation error for each algorithm, in addition to performing a grid search to find the best suited hyperparameters, the SVM method was deemed as the best one, with an average score of **0.51** (percentage of correctly classified instances on the validation set). By looking at its learning curve, it is clear that the algorithm is still underfitting, thus it would benefit from more complex features other than the current set.

<img src="https://github.com/lucasbflopes/spotify-api-track-classification/blob/master/model-selection/learning-curves/svc-learningCurve.pdf"/>

<h3> How to run </h3>

You can play with the trained model by trying to make it predict the genre of some music.

First of all, you need to sign-up for the Spotify's API on their [website](https://developer.spotify.com/web-api/) and create an application. This is necessary because in order to obtain the features of the music you are trying to test an API request is needed. 

Then, go to the folder api/ and fill the file "client\_keys.json" with your keys from the last step.

All ready and set!

Run main.py from the command line with the name of your music as an argument. For instance:

`$ python main.py "in the end"`


