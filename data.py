'''
	Name: R.Shyam Sundar
	Roll: CS20B1029
	Date: 26/11/2022
	Data Science Project - 5th Semester

	Codeforces Rating Predictor
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import os.path
from matplotlib import style
from datetime import datetime
import random
import time

def print_json(obj):
	obj1 = json.dumps(obj)
	parsed = json.loads(obj1)
	print(json.dumps(parsed, indent=4))
	pass

def create_data():
	response = requests.get('https://codeforces.com/api/user.ratedList?activeOnly=true&includeRetired=false')
	obj = response.json()
	print_json(obj)

	file1 = open("profiles.csv","w")
	file1.write("handle,rating,maxrating\n")
	for data in obj['result']:
		file1.write(data['handle'])
		file1.write(',')
		file1.write(str(data['rating']))
		file1.write(',')
		file1.write(str(data['maxRating']))	
		file1.write('\n')
	pass

def print_time(A):
	ts = int(str(A))
	print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
	pass

def submission_data(name):
	link = 'https://codeforces.com/api/user.status?handle=' + handle + '&from=1&count=3000'
	response = requests.get(link)
	obj = response.json()
	print_json(obj)

	for data in obj['result']:
		pdata = data['problem']
		if 'rating' in pdata:
			print(pdata['name'],'\t',pdata['rating'],'\t',data['verdict'])
			print_time(data['creationTimeSeconds'])
		else:
			print(pdata['name'],'\t','NULL','\t',data['verdict'])
	pass
		# https://codeforces.com/api/user.status?handle=Fefer_Ivan&from=1&count=10

def get_similar_handles(name):
	df = pd.read_csv('profiles.csv')
	df1 = df
	df1.drop('handle',axis=1)
	print(df.corr())
	pass

def create_rating_change_dataset(usr_handle):
	datacnt = int(input("Enter the number of sample to be collected from API:  "))
	df = pd.read_csv('profiles.csv')
	upper_bound = -1
	lower_bound = -1

	# link = 'https://codeforces.com/api/user.rating?handle=' + j
	# response = requests.get(link)
	# obj1 = response.json()
	# # print_json(obj)

	# print('Length = ',len(obj['result']));

	# usr_rating = -1;
	# for data in obj1['result']:
	# 	usr_rating = data['newRating']

	# print("User Rating:  ",usr_rating)

	# for i in range(0,len(df)):
		# if (lower_bound == -1) and (df.rating[i] >)
	

	st = set()
	while len(st) <= datacnt:
		val = random.randint(0,25000)
		time.sleep(2)
		link = 'https://codeforces.com/api/user.rating?handle=' + str(df.handle[val])
		response = requests.get(link, headers={'Content-Type': 'application/json'})
		print(st)
		obj2 = response.json()
		if(len(obj2['result']) > 10):
			st.add(str(df.handle[val]))
		else:
			pass
		# print(df.handle[val],df.rating[val])
		pass

	print(st)
	lst = list(st)


	# for i in range(0,len)
	
	# rating,r5,r4,r3,r2,r1,no_of_problems_solved,avg_problem_rating_contest,avg_problem_rating_practice,

	# print_json(obj1)
	# max_rat = -1
	# for i in range(0,len(obj1['result'])):
	# 	if max_rat < int(obj1['result'][i]['newRating']):
	# 		max_rat = int(obj1['result'][i]['newRating'])



	
	
	# print(r1,r2,r3,r4,r5)

	
	# print_json(obj)

	finaldata = pd.DataFrame({})
	print(finaldata)

	for j in lst:
		link = 'https://codeforces.com/api/user.rating?handle=' + j
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

		time.sleep(2)
		link = 'https://codeforces.com/api/user.status?handle=' + j + '&from=1&count=3000'
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
		print(contest_avg,practice_avg)
		print(contest)
		print(practice)

		no_of_problems = len(contest) + len(practice)

		df2 = pd.DataFrame({
			"rating" : [crating],
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
		finaldata = finaldata.append(df2)


	print(finaldata)
	# finaldata.to_csv('finaldata1.csv',index=False)
	finaldata.to_csv('finaldata1.csv', mode='a', index=False, header=False)
	# for i in range(0,len(lst)):


	# 100 profiles with rating +100

	# 25 profiles with rating +200
	# 5 profiles with rating +300
	# 100 profiles with rating -100
	# 25 profiles with rating -200
	# 5 profiles with rating -300
	pass

handle = input("Enter the user handle:  ")
# submission_data(handle)

# get_similar_handles(handle)

create_rating_change_dataset(handle);