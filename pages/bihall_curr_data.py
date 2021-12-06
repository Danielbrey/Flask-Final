import pandas as pd
from flask import render_template
from get_current_data import get_todays_data

#Gets current data for all of campus
def app():
  total_energy = get_todays_data('mbh')
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

  return render_template('average_demand.html', title = 'Current Data', data = total_energy, times = total_energy["Time"], values = total_energy["power"])

