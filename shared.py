import pandas as pd
import os
import matplotlib.pyplot as plt

# Load the dataframe from the csv files
def get_energy_dataframe():
  # Get the directory and the subfolders in the directory
  cur_dir = os.getcwd()
  data_dir = cur_dir + "/data"
  folders = next(os.walk(data_dir))[1]
  df_list = []
  for curr_year_folder in folders:
    file_name = data_dir + '/' + curr_year_folder + '/' + curr_year_folder + '.csv'
    #print(file_name)
    df = pd.read_csv(file_name)
    df_list.append(df)

  total_energy = pd.concat(df_list)
  return total_energy


def pie_chart():
  # Pie chart, where the slices will be ordered and plotted counter-clockwise:
  labels = 'Bicentennial Hall', 'Davis Library', 'Proctor', 'McCullough'
  sizes = [15, 30, 45, 10]

  fig1, ax1 = plt.subplots()
  fig1.patch.set_facecolor('#EBEBEB')

  ax1.pie(sizes,labels=labels
          )
  ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
  return fig1