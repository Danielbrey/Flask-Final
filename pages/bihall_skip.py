import pandas as pd
from flask import render_template

#from shared import get_energy_dataframe, pie_chart
from get_current_data import get_metrics_data


def app():
  #print('test')
  total_energy = pd.read_csv('all-mbh.csv')
  print(total_energy)
  print("1")

  datetimes_as_strings = total_energy["datetime"]
  #print(type(datetimes_as_strings))
  
  datetimes_replace = datetimes_as_strings.str.replace('T', '-')
  datetimes_split = datetimes_replace.str.split('-')
  datetimes_apply = datetimes_split.apply(pd.Series)
  datetimes_day = datetimes_apply.iloc[:,2]
  datetimes_month = datetimes_apply.iloc[:,1]
  datetimes_year = datetimes_apply.iloc[:,0]
  total_energy["Date"] = datetimes_year + '-' + datetimes_month + '-' + datetimes_day 
  #print(len(total_energy['Date'].unique().tolist())) 
  days_filter = datetimes_day.astype('int')%15 == 0
  total_energy = total_energy[days_filter]
  #print(total_energy)
  print("2")
  
  total_energy = total_energy.groupby('Date', group_keys=False).apply(lambda df: df.sample(1))
  print("3")
  #print(total_energy)
  return render_template('average_demand.html', title = 'Bihall', data = total_energy, times = total_energy["Date"], values = total_energy["power"])
