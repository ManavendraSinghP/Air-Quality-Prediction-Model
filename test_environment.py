#!/usr/bin/env python3
"""
Test script to verify that the conda environment is properly set up
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import sys

print("Python version:", sys.version)
print("NumPy version:", np.__version__)
print("Pandas version:", pd.__version__)

# Create a simple dataset
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])

# Fit a linear regression model
model = LinearRegression()
model.fit(X, y)

print("Linear regression model trained successfully!")
print(f"Coefficient: {model.coef_[0]}")
print(f"Intercept: {model.intercept_}")

# Create a simple plot
plt.figure(figsize=(8, 6))
plt.scatter(X, y, color='blue', label='Data points')
plt.plot(X, model.predict(X), color='red', label='Linear fit')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Simple Linear Regression Example')
plt.legend()
plt.grid(True)
plt.savefig('test_plot.png')
plt.close()

print("Plot saved as 'test_plot.png'")

# Create a simple DataFrame
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 6, 8, 10],
    'predicted': model.predict(X).flatten()
})

print("\nDataFrame with actual and predicted values:")
print(df)

print("\nEnvironment test completed successfully!")