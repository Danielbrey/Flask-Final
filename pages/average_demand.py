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



  # _, col2 = st.columns([.1, 4])

  # with col2:
  #   st.header('Average Energy Demand')
  # chart_line = alt.Chart(total_energy).mark_line().encode(
  #   alt.X('Date:T', timeUnit = 'yearmonthdate'),
  #   y='Average Demand'
  # )
  # st.altair_chart(chart_line, use_container_width=True)

  # metric1, metric2, metric3 = st.columns([8,8,8])

  # with metric1:
  #   day, day_diff, week, week_diff = get_metrics_data()
  #   st.metric('Usage: Today', "{} kW".format(day), "{}%".format(day_diff))
  # with metric2:
  #   st.metric('Usage: Past Week', "{} kW".format(week), "{}%".format(week_diff))
  # with metric3:
  #   st.metric('Usage: Past Month', 42, 2)

  # fig1 = pie_chart()
  # st.pyplot(fig1)
