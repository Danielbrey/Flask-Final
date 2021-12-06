from numpy import datetime_as_string
import requests
from datetime import date, datetime, timedelta
import pandas as pd
import io
import re

def get_url(curr_day, curr_month, curr_year, location = 'campus'):
  if(int(curr_day) < 10):
    curr_day = '0' + str(curr_day)
  return "https://observatory.middlebury.edu/campus/energy/archive/{}{}{}-{}.csv".format(curr_year, curr_month, curr_day, location)

def string_filter(df):
  datetimes_as_strings = df.iloc[:,0]
  datetimes_replace = datetimes_as_strings.str.replace(':', '-')
  datetimes_split = datetimes_replace.str.split('-')
  datetimes_minute = datetimes_split.apply(pd.Series)[3]
  minutes_filter = datetimes_minute.astype('int')%10 == 0
  
  return df[minutes_filter]
  
def load_day_data(curr_day, curr_month = "", curr_year = "", location = None):
  if(location):
    url = get_url(curr_day, curr_month, curr_year, location)
  else:
    url = get_url(curr_day, curr_month, curr_year)
  
  
  data = requests.get(url).content
  df = pd.read_csv(io.StringIO(data.decode('utf-8')), skiprows=1)
  return string_filter(df)


def get_week_data(location = None):
  datetime_rn = datetime.now()
  weekday = datetime_rn.strftime("%w")  
  if(location):
    df = load_day_data(datetime_rn.day, datetime_rn.month, datetime_rn.year, location)
  else:
    df = load_day_data(datetime_rn.day, datetime_rn.month, datetime_rn.year)
  #print(df)
  df.columns = ['datetime', 'location', 'power']
  #df["datetime"] = pd.to_datetime(df["datetime"])
  for i in range(int(weekday)):
    past_day_date = datetime_rn - timedelta(days = i+1)
    if(location):
      past_day = load_day_data(past_day_date.day, past_day_date.month, past_day_date.year, location)
    else:
      past_day = load_day_data(past_day_date.day, past_day_date.month, past_day_date.year)
    #print(past_day)
    past_day.columns = ['datetime', 'location', 'power']
    #past_day["datetime"] = pd.to_datetime(past_day["datetime"])
    #frames = [df, past_day]
    df = pd.merge(past_day, df, how = "outer", on = ['datetime', 'location', 'power'])
  return(df)
  
    
    
  

def get_metrics_data():
  curr_time = datetime.now()
  # Metric for past day
  today = load_day_data(curr_time.day, curr_time.month, curr_time.year)
  yesterday = load_day_data((curr_time + timedelta(days=-1)).day, curr_time.month, curr_time.year)
  
  todays_usage = int(today.sum()[2])
  yesterdays_usage = int(yesterday.head(len(today)).sum()[2])
  day_diff = round((((todays_usage / yesterdays_usage) - 1) * 100), 1)
  # Metric for past week
  all_data = load_day_data("all")
  num_datapoints = int(7 * 24 * 60 / 10) # 7 days, 24 hours, and one datapoint every ten minutes
  this_week_usage = int(all_data.tail(num_datapoints).sum()[2])
  last_week_usage = int(all_data.tail(num_datapoints*2).head(num_datapoints).sum()[2])
  week_diff = round((((this_week_usage / last_week_usage) - 1) * 100), 1)

  # Metric for past month


  return (todays_usage, day_diff, int(this_week_usage / 7), week_diff)



def get_todays_data(location = None):
  curr_time = datetime.now()
  print(curr_time)
  # Metric for past day
  if(location):
    today = load_day_data(curr_time.day, curr_time.month, curr_time.year, location)
  else:
    today = load_day_data(curr_time.day, curr_time.month, curr_time.year)
  
  return today
