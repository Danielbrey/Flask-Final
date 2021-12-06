import pandas as pd
from flask import render_template
from get_current_data import get_todays_data
from ml_models import load_data, prepare_data, get_model_predictions
from datetime import datetime, timedelta

def predict_today():
  data = load_data()
  data = prepare_data(data)

  train_X = data[['Minute', 'Hour', 'Day', 'Month', 'Year', 'Weekday']]
  train_y = data['Power']
  
  today = datetime.now().date()
  tomorrow = today + timedelta(days=1)
  next_day = pd.date_range(today,tomorrow, 
              freq='10T').strftime("%Y-%m-%dT%H-%M-%S").tolist()
  print("hello")
  next_day = pd.DataFrame(next_day, columns = ['Datetime'])
  
  
  predict_data = prepare_data(next_day)
  print("Prepared data")
  print(predict_data)

  vali_X = predict_data[['Minute', 'Hour', 'Day', 'Month', 'Year', 'Weekday']]
  vali_y = None

  _, rf_pred_y, _ = get_model_predictions(train_X, train_y, vali_X, vali_y, type = "rf")

  return [rf_pred_y, next_day['Datetime'].values]

#Gets current data for all of campus
def app(total_energy, location):
  [predicted, x_predicted] = predict_today()
  # total_energy = get_todays_data()
  # total_energy.columns = ['datetime', 'location', 'power']
  
  # datetimes_as_strings = total_energy['datetime']
  
  # datetimes_replace = datetimes_as_strings.str.replace('T', '-')
  # datetimes_split = datetimes_replace.str.split('-')
  # datetimes_apply = datetimes_split.apply(pd.Series)
  # datetimes_day = datetimes_apply.iloc[:,2]
  # datetimes_month = datetimes_apply.iloc[:,1]
  # datetimes_year = datetimes_apply.iloc[:,0]
  # datetimes_time = datetimes_apply.iloc[:,3]
  # total_energy["Time"] = datetimes_time 
  #print(len(total_energy['Date'].unique().tolist())) 

  #Commented out filter and group_by since it was already being filtered in get_todays_data
  #days_filter = datetimes_day.astype('int')%15 == 0
  #total_energy = total_energy[days_filter]
  
  #total_energy = total_energy.groupby('Date', group_keys=False).apply(lambda df: df.sample(1))
  print(total_energy['datetime'])
  return render_template('average_demand.html', title = 'Current Data for ' + location.title(), data = total_energy, times = total_energy["datetime"], values = total_energy["power"], times_future = x_predicted, values_predicted = predicted)

