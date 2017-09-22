import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.svm import SVC
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

# SVM classifier
svc = Pipeline([
	("scaler", StandardScaler()),
	("estimator", SVC(C=10, gamma=0.1))
	])

# svc.fit(X_train, y_train)
# print("Cross validation mean score: ", cross_val_score(svc, X_train, y_train, cv=5).mean())

# grid_search = GridSearchCV(svc, dict(estimator__C=[0.01, 0.1, 1, 10], estimator__gamma=[0.01, 0.1, 1, 10])
# 	)
# grid_search.fit(X_train, y_train)
# print(grid_search.best_params_)

#print("Testing set score: ", svc.score(X_test, y_test))

svc.fit(X, y)

with open('../model_trained.pkl', 'wb') as fout:
	pickle.dump(svc, fout)