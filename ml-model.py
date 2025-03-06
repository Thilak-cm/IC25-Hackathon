import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

# Load the dataset
data = pd.read_csv('data/Lots_Permissions_CH5_fakedata (1).csv')

# Define input features
input_features = ['Lot Type', 'Physical Location (Yes/No)', 'Lot Name', 'Posted Restrictions', 'Enforcement Days', 'Start Time - Daily', 'End Time - Daily']

# Determine the output columns
start_col = data.columns.get_loc('17FAE')
output_columns = data.columns[start_col:]
print(output_columns)
output_size = len(output_columns)

# Handle missing values
data['Posted Restrictions'].fillna('None', inplace=True)

# Convert time columns to numerical values (e.g., seconds since midnight)
def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

data['Start Time - Daily'] = data['Start Time - Daily'].apply(time_to_seconds)
data['End Time - Daily'] = data['End Time - Daily'].apply(time_to_seconds)

# Prepare input and output data
X = data[input_features]
y = data[output_columns].fillna(0).astype(int)

# One-hot encode categorical features
categorical_features = ['Lot Type', 'Physical Location (Yes/No)', 'Lot Name', 'Posted Restrictions', 'Enforcement Days']
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), categorical_features)
    ],
    remainder='passthrough'
)

# Create a pipeline
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42)))
])

# Train the model on the entire dataset
pipeline.fit(X, y)

# Select 20% of the data for testing accuracy
test_size = int(0.2 * len(X))
test_indices = np.random.choice(len(X), size=test_size, replace=False)
X_test = X.iloc[test_indices]
y_test = y.iloc[test_indices]

# Evaluate the model on the test set
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy}")

# Select a random test example for inference
random_index = np.random.choice(test_indices)
X_single_test = X.iloc[[random_index]]
y_single_test = y.iloc[[random_index]]

# Predict for the random test example
y_single_pred = pipeline.predict(X_single_test)

# Display the inputs
print("\nRandom Test Input:")
print(X_single_test)

# Display the predicted outputs
predicted_permits = [output_columns[i] for i, val in enumerate(y_single_pred[0]) if val == 1]
print("\nPredicted Permits:")
print(predicted_permits)

# Display the number of valid permits
num_valid_permits = sum(y_single_pred[0])
print(f"\nNumber of Valid Permits: {num_valid_permits}")
