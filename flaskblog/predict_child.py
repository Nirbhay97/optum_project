import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import warnings
import pickle
warnings.filterwarnings("ignore")

data = pd.read_csv("finaldata.csv")
#data = np.array(data)

X = data[['mom_level', 'data_level']]
Y = data['Child']
y = Y.astype('float')
X = X.astype('float')
# print(X,y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)

#inputt = [float(x) for x in "1 .8".split(' ')]
#final = [np.array(inputt)]

#b = regr.predict(final)

pickle.dump(regr, open('model.pkl', 'wb'))
model = pickle.load(open('model.pkl', 'rb'))
#print(regr.predict([[.7, 1]]))
#print(model.predict([[.7, 1]]))