import pickle
from sklearn.preprocessing import LabelEncoder
import pandas as pd

data = pd.read_csv('Train.csv')
data.drop(columns=['ID'],inplace=True)
# Encode categorical features
label_encoders = {}
for column in ['Warehouse_block', 'Mode_of_Shipment', 'Product_importance', 'Gender']:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

x=data.drop(columns=['Reached.on.Time_Y.N'])
y = data['Reached.on.Time_Y.N']

#split the data set
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=.70)

#Using decision tree algorithm
from sklearn import tree
classifier=tree.DecisionTreeClassifier()
classifier.fit(x_train,y_train)


#export the model
pickle.dump(classifier, open('model.pkl','wb'))
pickle.dump(label_encoders, open('encoders.pkl', 'wb'))
#load the model and test with a custom input
model = pickle.load( open('model.pkl','rb'))
