import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.metrics import accuracy_score


def predict_for_handle():
	handle = input("Enter the Codeforces handle:    ")
	link = 'https://codeforces.com/api/user.rating?handle=' + handle
	response = requests.get(link)
	obj1 = response.json()

	usr_rating = -1;
	for data in obj1['result']:
		usr_rating = data['newRating']

	print("User Rating:  ",usr_rating)

	x = int(len(obj1['result']))
	crating = obj1['result'][x-1]['newRating']
	r1 = obj1['result'][x-2]['newRating']
	r2 = obj1['result'][x-3]['newRating']
	r3 = obj1['result'][x-4]['newRating']
	r4 = obj1['result'][x-5]['newRating']
	r5 = obj1['result'][x-6]['newRating']

	max_rat = -1
	for i in range(0,len(obj1['result'])):
		if max_rat < int(obj1['result'][i]['newRating']):
			max_rat = int(obj1['result'][i]['newRating'])

	link = 'https://codeforces.com/api/user.status?handle=' + handle + '&from=1&count=3000'
	response = requests.get(link)
	obj = response.json()

	contest = []
	practice = []
	for i in range(0,len(obj['result'])):
		if obj['result'][i]['verdict'] == 'OK':
			if obj['result'][i]['author']['participantType'] == 'CONTESTANT':
				if 'rating' in obj['result'][i]['problem']:
					contest.append(int(obj['result'][i]['problem']['rating']))
			else:
				if 'rating' in obj['result'][i]['problem']:
					practice.append(int(obj['result'][i]['problem']['rating']))
	
	contest_avg = sum(contest) / len(contest)
	practice_avg = sum(practice) / len(practice)

	no_of_problems = len(contest) + len(practice)

	df2 = pd.DataFrame({
		"max_rating": [max_rat],
		"r1": [r1],
		"r2": [r2],
		"r3": [r3],
		"r4": [r4],
		"r5": [r5],
		"no_of_problems": [no_of_problems],
		"contest_avg": [contest_avg],
		"practice_avg": [practice_avg]
		})
	print(df2)

	dataset = pd.read_csv("finaldata1.csv")

	x = dataset[['max_rating', 'r1','r2','r3','r4','r5','no_of_problems','contest_avg','practice_avg']]
	y = dataset['rating']

	x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 100)


	mlr = LinearRegression()  
	mlr.fit(x_train, y_train)

	list(zip(x, mlr.coef_))

	x_test = df2
	y_pred_mlr= mlr.predict(x_test)

	print("Prediction for test set: {}".format(y_pred_mlr))



	pass

dataset = pd.read_csv("finaldata1.csv")

# dataset.head()

x = dataset[['max_rating', 'r1','r2','r3','r4','r5','no_of_problems','contest_avg','practice_avg']]
y = dataset['rating']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 100)


mlr = LinearRegression()  
mlr.fit(x_train, y_train)

list(zip(x, mlr.coef_))

#Prediction of test set
y_pred_mlr= mlr.predict(x_test)
#Predicted values
print("Prediction for test set: {}".format(y_pred_mlr))

mlr_diff = pd.DataFrame({'Actual value': y_test, 'Predicted value': y_pred_mlr})
print(mlr_diff.head())

# meanAbErr = metrics.mean_absolute_error(y_test, y_pred_mlr)
# meanSqErr = metrics.mean_squared_error(y_test, y_pred_mlr)
rootMeanSqErr = np.sqrt(metrics.mean_squared_error(y_test, y_pred_mlr))
# print('R squared: {:.2f}'.format(mlr.score(x,y)*100))
# print('Mean Absolute Error:', meanAbErr)
# print('Mean Square Error:', meanSqErr)
print('Root Mean Square Error:', rootMeanSqErr)
predict_for_handle()
# for i,j in zip(y_pred_mlr,y_test):
	# print(i,j)
# print(metrics.accuracy_score(y_pred_mlr,y_test))	
# accuracy_score(y_test,y_pred_mlr)

# print("Test set: ",y_test)
# print("Prediction: ",y_pred_mlr)