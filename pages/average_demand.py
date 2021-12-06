#import streamlit as st
import pandas as pd
#import altair as alt
from flask import render_template

from shared import get_energy_dataframe, pie_chart
from get_current_data import get_metrics_data


def app():
  total_energy = get_energy_dataframe()
  

  datetimes_as_strings = total_energy["Time"]
  #print(type(datetimes_as_strings))
  datetimes_replace = datetimes_as_strings.str.replace(' ', '-')
  datetimes_split = datetimes_replace.str.split('-')
  datetimes_day = datetimes_split.apply(pd.Series)[2]
  datetimes_month = datetimes_split.apply(pd.Series)[1]
  datetimes_year = datetimes_split.apply(pd.Series)[0]

  total_energy["Date"] = datetimes_year + '-' + datetimes_month + '-' + datetimes_day 
  #print(len(total_energy['Date'].unique().tolist())) 
  days_filter = datetimes_day.astype('int')%15 == 0
  total_energy = total_energy[days_filter]
  
  total_energy = total_energy.groupby('Date', group_keys=False).apply(lambda df: df.sample(1))
  print(total_energy)
  total_energy.to_csv('campus_past')
  return render_template('average_demand.html', title = 'Average Demand', data = total_energy, times = total_energy["Date"], values = total_energy["Average Demand"])




