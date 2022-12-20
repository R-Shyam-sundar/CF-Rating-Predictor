import pandas as pd 
from matplotlib import pyplot as plt

df = pd.read_csv('finaldata1.csv')
print(df)

max_rat = []
crat = []

for i in range(0,len(df)):
	max_rat.append(df.max_rating[i])
	crat.append(df.rating[i])

plt.plot(crat,max_rat)
plt.show()