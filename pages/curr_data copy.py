import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from flask import render_template
from get_current_data import get_todays_data, get_metrics_data
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
  print("Dates")
  next_day = pd.DataFrame(next_day, columns = ['Datetime'])
  print(next_day)
  
  predict_data = prepare_data(next_day)
  print("Prepared data")
  print(predict_data)

  vali_X = predict_data[['Minute', 'Hour', 'Day', 'Month', 'Year', 'Weekday']]
  vali_y = None

  _, rf_pred_y, _ = get_model_predictions(train_X, train_y, vali_X, vali_y, type = "rf")

  return rf_pred_y

#Gets current data for all of campus
def app():
  total_energy = get_todays_data()
  total_energy.columns = ['datetime', 'location', 'power']
  
  datetimes_as_strings = total_energy['datetime']
  
  datetimes_replace = datetimes_as_strings.str.replace('T', '-')
  datetimes_split = datetimes_replace.str.split('-')
  datetimes_apply = datetimes_split.apply(pd.Series)
  datetimes_day = datetimes_apply.iloc[:,2]
  datetimes_month = datetimes_apply.iloc[:,1]
  datetimes_year = datetimes_apply.iloc[:,0]
  datetimes_time = datetimes_apply.iloc[:,3]
  total_energy["Time"] = datetimes_time 

  


  #print(len(total_energy['Date'].unique().tolist())) 

  #Commented out filter and group_by since it was already being filtered in get_todays_data
  #days_filter = datetimes_day.astype('int')%15 == 0
  #total_energy = total_energy[days_filter]
  
  #total_energy = total_energy.groupby('Date', group_keys=False).apply(lambda df: df.sample(1))

  _, day_diff, _, week_diff = get_metrics_data()

  if day_diff > 0:
    print("here")
    day_diff = "+" + str(day_diff)

  if week_diff > 0:
    print("here")
    week_diff = "+" + str(week_diff)

  return render_template('average_demand.html', title = 'Current Data', data = total_energy, times = total_energy["Time"], values = total_energy["power"],day_diff = day_diff, week_diff = week_diff)

if __name__ == "__main__":
  print(predict_today())