import pandas as pd
from get_current_data import load_day_data
from datetime import datetime
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score, mean_squared_error


#Gets current data for all of campus
def load_data(all_data):

  #curr_date = datetime.now().date()


  #all_data = load_day_data(curr_date.day, curr_date.month, curr_date.year, "all")
  all_data.columns = ['Datetime', 'Location', 'Power']
  split = all_data['Datetime'].str.split('T').apply(pd.Series)
  dates = split.iloc[:,0]
  times = split.iloc[:,1]
  all_data["Time"] = times
  all_data["Date"] = dates
  all_data = all_data[all_data["Power"] > 100]
  #all_data.to_csv("curr_data.csv")
  return all_data

def prepare_data(all_data):
  all_data['Minute'] = pd.to_datetime(all_data['Datetime']).dt.minute
  all_data['Hour'] = pd.to_datetime(all_data['Datetime']).dt.hour
  all_data['Day'] = pd.to_datetime(all_data['Datetime']).dt.day
  all_data['Month'] = pd.to_datetime(all_data['Datetime']).dt.month
  all_data['Year'] = pd.to_datetime(all_data['Datetime']).dt.year
  all_data['Weekday'] = pd.to_datetime(all_data['Datetime']).dt.weekday
  return all_data

def split(all_data):
  train, test = train_test_split(all_data, test_size=0.25, random_state=42, shuffle=False)

  train_X = train[['Minute', 'Hour', 'Day', 'Month', 'Year', 'Weekday']]
  train_y = train['Power']

  vali_X = test[['Minute', 'Hour', 'Day', 'Month', 'Year', 'Weekday']]
  vali_y = test['Power']
  return train_X, train_y, vali_X, vali_y


def get_model_predictions(train_X, train_y, vali_X, vali_y, type = "all"):
  
  dt_pred_y = None
  rf_pred_y = None
  mlp_pred_y = None
  
  if (type == "dt" or type == "all"):
    dt = DecisionTreeRegressor()
    dt.fit(train_X, train_y)
    dt_pred_y = dt.predict(vali_X)

  if (type == "rf" or type == "all"):
    rf = RandomForestRegressor()
    rf.fit(train_X, train_y)
    rf_pred_y = rf.predict(vali_X)
    #print("R Squared: {}".format(r2_score(rf_pred_y, vali_y.values)))
    #print("Mean Squared Error: {}".format(mean_squared_error(rf_pred_y, vali_y.values)))

  if (type == "mlp" or type == "all"):
    mlp = MLPRegressor()
    mlp.fit(train_X, train_y)
    mlp_pred_y = mlp.predict(vali_X)

  return dt_pred_y, rf_pred_y, mlp_pred_y

if __name__ == "__main__":
  # all_data = load_data()
  all_data = pd.read_csv("curr_data.csv")
  all_data = prepare_data(all_data)

  train_X, train_y, vali_X, vali_y = split(all_data)
  dt_pred_y, rf_pred_y, mlp_pred_y = get_model_predictions(train_X, train_y, vali_X, vali_y)

  presentation_grey = 232/256
  rgb_color = (presentation_grey,presentation_grey,presentation_grey)

  plt.figure()
  plt.figure(facecolor=rgb_color)
  ax = plt.axes()
  ax.set_facecolor(rgb_color)
  plt.plot(train_X.index, train_y)
  plt.plot(vali_X.index, vali_y, color="cornflowerblue", label="Actual")
  plt.plot(vali_X.index, dt_pred_y, label="Decision Tree")
  plt.plot(vali_X.index, rf_pred_y, label="Random Forest")
  plt.plot(vali_X.index, mlp_pred_y, label="Multi Layer Perceptron")
  plt.xlabel("Time")
  plt.ylabel("Energy Usage (kW)")
  plt.title("Different Prediction Algorithms Regression")
  plt.legend()
  plt.show()
