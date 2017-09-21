import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

def plot_learning_curve(estimator, X, y, title="", cv=None,
                        train_sizes=np.linspace(0.01, 1, num=5)):

	plt.figure()
	plt.xlabel('# of training samples')
	plt.ylabel('Score')
	plt.ylim((0, 1))
	plt.title(title)

	train_sizes, train_scores, test_scores = learning_curve(estimator, X, y, cv=cv, train_sizes=train_sizes)
	train_scores_mean = train_scores.mean(axis=1)
	test_scores_mean = test_scores.mean(axis=1)

	plt.plot(train_sizes, train_scores_mean, 'o-', color='r', label='Training set score')
	plt.plot(train_sizes, test_scores_mean, 'o-', color='b', label='Cross validation set score')
	plt.legend(loc='best')
	plt.grid()
	
	return plt

