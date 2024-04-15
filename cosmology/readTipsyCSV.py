import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from math import sqrt

#returns a dictionary of particles
def read_full_csv(file_name):
    with open(file_name, "r") as file:
        df = pd.read_csv(file)
        df.dropna(how='all')
        df = df.drop(df.columns[[-1]], axis=1)
    return df 

#func to extract target variables from a row (a single particle)
def extract_variables(row):
    return [
        row.get('particle mass', 0.0), row.get('v_x', 0.0), row.get('v_y', 0.0),
        row.get('v_z', 0.0), row.get('eps', 0.0),
        row.get('x', 0.0), row.get('y', 0.0), row.get('z', 0.0)
    ]

# Get target variables
def parse_row(row): 
    return [
        row[0], row[1], row[2], row[3], row[4], row[5], row[7], row[8], row[9]
    ] 

#csv_input_full = path to dataset 1
#csv_output_full = path to dataset 2

data = np.genfromtxt(csv_input_full, delimiter=",", skip_header=1)
X = np.apply_along_axis(parse_row, axis=1, arr=data)

data = np.genfromtxt(csv_output_full, delimiter=",", skip_header=1)
y = np.apply_along_axis(parse_row, axis=1, arr=data)
