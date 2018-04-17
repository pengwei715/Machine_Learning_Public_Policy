import pandas as pd 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


def accuracy(y_true, y_pred, normalize=True, sample_weight=None):
    '''
    Calculates accuracy of model
    Inputs:
        y_true (dataframe): containing y (label) values for test set from data
        y_pred (dataframe): containing predicted y values generated by model
        normalize (boolean)
        sample_weight:
    Returns:
        accuracy score (float)
    '''
    return accuracy_score(y_true, y_pred, normalize, sample_weight)

def knn_eval_table(y_test, x_test, x_train, y_train, n_neighbors, metric, weight):
	'''
	Trains and tests multiple k-nearest neighbor models using each combination of parameters
	provided in the function parameters and returns table containing accuracy for each 
	combination of parameters
	Inputs:
		y_test (dataframe): containing y (label) values for test set from data
		x_test (dataframe): containing factor values for test set from data
		y_train (dataframe): containing y (label) values for train set from data
		x_train (dataframe): containing factor values for train set from data
		n_neighbors (list): containing the numbers of neighbors (int) to test
		metric (list): containing the metrics (str) to test
		weight (list): containing the weights (str) to test
	Returns:
		eval_table (dataframe): containing parameter values and accuracy for the model
			representing each ocmbination of parameters tested


	'''

	eval_table = []

	for n in n_neighbors:
		for m in metric:
			for w in weight:
				knn = KNeighborsClassifier(n_neighbors = n, metric = m, 
					weights = w, algorithm = 'brute')
				knn.fit(x_train, y_train)
				y_pred = knn.predict(x_test)
				acc = accuracy(y_test, y_pred)
				eval_table.append([n, m, w, acc])

	return pd.DataFrame(eval_table, columns = ['n_neighbors', 'metric', 
		'weight', 'accuracy'])


def accuracy_table(x_test, y_test, x_train, y_train, n_neighbors, metric, weights):
	knn = KNeighborsClassifier(n_neighbors = n_neighbors, metric = metric, 
		weights = weights, algorithm = 'brute')
	knn.fit(x_train, y_train)
	y_pred = knn.predict(x_test)
	tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
	return pd.DataFrame.from_items([('Actual_True', [tp, fn]), ('Actual_False', [fp, tn])],
                      orient='index', columns=['Predict_True', 'Predict_False'])
