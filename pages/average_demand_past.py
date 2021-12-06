#import streamlit as st
import pandas as pd
#import altair as alt
from flask import render_template

from shared import get_energy_dataframe, pie_chart
from get_current_data import get_metrics_data


def app():
  total_energy = pd.read_csv('campus_past.csv')
  return render_template('average_demand.html', title = 'Average Demand', data = total_energy, times = total_energy["Date"], values = total_energy["Average Demand"])


