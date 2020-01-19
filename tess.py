from sklearn.cluster import KMeans
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot as plt
df = pd.read_csv("income.csv")
plt.scatter(df.Age,df['Income($)'])
plt.xlabel('Age')
plt.ylabel('Income($)')

km = KMeans(n_clusters=5)
y_predicted = km.fit_predict(df[['Age','Income($)']])
df['cluster']=y_predicted
km.cluster_centers_

# data = pd.read_csv('income.csv', nrows=1).columns get only column
df1 = df[df.cluster==0]
df2 = df[df.cluster==1]
df3 = df[df.cluster==2]
df4 = df[df.cluster==3]
print(df)
plt.scatter(df1.Age,df1['Income($)'],color='green')
plt.scatter(df2.Age,df2['Income($)'],color='red')
plt.scatter(df3.Age,df3['Income($)'],color='black')
plt.scatter(df4.Age,df4['Income($)'],color='yellow')
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='blue',marker='*',label='centroid')
# plt.scatter(km.cluster_centers_[:,1],km.cluster_centers_[:,1],color='green',marker='^',label='Age')
# plt.xlabel('Age')
# plt.ylabel('Income ($)')
plt.legend()
plt.savefig('foo.png')
plt.show()