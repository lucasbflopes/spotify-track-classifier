import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.utils import shuffle
from plot_learning_curve import plot_learning_curve

# Load dataset, shuffles it, and remove instances with 'nan' values
dataset = pd.read_csv('../dataset/dataset.csv')
dataset.dropna(axis=0, how='any', inplace=True)
dataset.drop('title', axis=1, inplace=True)
dataset = shuffle(dataset, random_state=42)

# Assign feature matrix and label vector
y = dataset['genre']
X = dataset.drop('genre', axis=1)

# Split data into a training and testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# K-Nearest Neighbour
knn = Pipeline([
	("scaler", StandardScaler()),
	("estimator", KNeighborsClassifier())
	])

knn.fit(X_train, y_train)
print("Cross validation mean score: ", cross_val_score(knn, X_train, y_train, cv=5).mean())

