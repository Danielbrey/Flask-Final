import pandas as pd
from flask import render_template
from get_current_data import get_todays_data
from ml_models import load_data, prepare_data, get_model_predictions
from datetime import datetime, timedelta

NUM_VALS_PER_DAY = 145

def predict_today(data):
  print(data)
  #data = load_data(energy)
  #data = prepare_data(data)

  train_X = data[['Minute', 'Hour', 'Day', 'Month', 'Year', 'Weekday']]
  train_y = data['Power']
  
  today = datetime.now().date()
  tomorrow = today + timedelta(days=1)
  next_day = pd.date_range(today,tomorrow, 
              freq='10T').strftime("%Y-%m-%dT%H:%M:%S").tolist()
  
  next_day = pd.DataFrame(next_day, columns = ['Datetime'])
  
  
  predict_data = prepare_data(next_day)

  vali_X = predict_data[['Minute', 'Hour', 'Day', 'Month', 'Year', 'Weekday']]
  vali_y = None

  _, rf_pred_y, _ = get_model_predictions(train_X, train_y, vali_X, vali_y, type = "rf")

  return (rf_pred_y, next_day['Datetime'].values)

#Gets current data for all of campus
def app(total_energy, ml_energy, location):
  num_append = NUM_VALS_PER_DAY - len(total_energy["power"].values)
  append_list = [0] * num_append
  print('ml2')
  print(ml_energy)
  y_predicted, times = predict_today(ml_energy)
  print("X Pred, length: {}".format(len(times)))
  print(times)
  print("Y Pred, length: {}".format(len(y_predicted)))
  print(y_predicted)
  print("Y Actual, length: {}".format(len(total_energy["power"].values)))
  y_actual = list(total_energy["power"].values) + append_list
  print(y_actual)
  
  return render_template('average_demand.html', title = 'Current Data for ' + location.title(), times = times, actual = y_actual, predicted = y_predicted)

