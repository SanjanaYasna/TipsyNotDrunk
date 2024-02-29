import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from math import sqrt

# Parse the particle information from the input and output strings
def parse_particle_info(line):
    info = line.split(", ")
    particle_data = {}
    for item in info:
        key, value = item.split("=")
        value = value.strip()
        #Handle N/A value
        if value != 'N/A':
            particle_data[key.strip()] = float(value)
        else:
            particle_data[key.strip()] = 0  
    return particle_data

# Load data from input.txt
# Replace route with your own
with open("/Users/lucyvivienne/Desktop/2023FallResearch/code/decoding_tipsy_input_c.txt", "r") as file:
    input_lines = file.readlines()

input_data = [parse_particle_info(line) for line in input_lines]

# Load data from output.txt
# Replace route with your own
with open("/Users/lucyvivienne/Desktop/2023FallResearch/code/decoding_tipsy_all_1.txt", "r") as file:
    output_lines = file.readlines()

output_data = [parse_particle_info(line) for line in output_lines]

# Extract target variables
X = np.array([
    [
        particle.get('mass', 0.0), particle.get('vx', 0.0), particle.get('vy', 0.0), 
        particle.get('vz', 0.0), particle.get('eps', 0.0),
        particle.get('x', 0.0), particle.get('y', 0.0), particle.get('z', 0.0)
    ] 
    for particle in input_data
])

y = np.array([
    [
        particle.get('x', 0.0), particle.get('y', 0.0), particle.get('z', 0.0)
    ] 
    for particle in output_data
])

# Remove rows with NaN or infinite values 
valid_rows = np.all(np.isfinite(X), axis=1) & np.all(np.isfinite(y), axis=1) 
X = X[valid_rows] 
y = y[valid_rows]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Remove rows with NaN or infinite values in the standardized data 
valid_rows_train = np.all(np.isfinite(X_train_scaled), axis=1) & np.all(np.isfinite(y_train), axis=1) 
X_train_scaled = X_train_scaled[valid_rows_train] 
y_train = y_train[valid_rows_train]

# Initialize SVR model 
svr_model = SVR(kernel='linear', C=1.0) 

# Train the model 
svr_model.fit(X_train_scaled, y_train) 

# Make predictions on the test set 
y_pred = svr_model.predict(X_test_scaled) 

# Evaluate the model 
mse = mean_squared_error(y_test, y_pred) 
rmse = sqrt(mse) 
print("Root Mean Squared Error (RMSE): {}".format(rmse))