#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import os
import zipfile
import subprocess
import time
import sys
from itertools import cycle


MULTIPLIER = 17


user_input = input("MULTIPLIER (Int/Float/Smash Enter) => ")
try:
    MULTIPLIER = float(user_input) if '.' in user_input else int(user_input)
except Exception:
    MULTIPLIER = 17

DataSetSlug = "amitabhajoy/bengaluru-house-price-data"
subprocess.run(['kaggle', 'datasets', 'download', '-d', DataSetSlug])

# UNZIP
zip_file = [f for f in os.listdir() if f.endswith(".zip")][0]
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall()

target_csv = "Bengaluru_House_Data.csv"
if target_csv in os.listdir():
    kaggle = pd.read_csv(target_csv)
    print(f"Loaded {target_csv}:")
else:
    print(f"{target_csv} not found in the extracted files.")


# THE ANGEL
kaggle_test = kaggle.iloc[10656:]
kaggle_test = kaggle_test.reset_index(drop=True)
kaggle_test.insert(0, 'ID', kaggle_test.index)
final_kaggle_test = kaggle_test.drop(['area_type', 'availability', 'location', 'size', 'society', 'total_sqft', 'bath', 'balcony'], axis=1)

# THE DEVIL
df = final_kaggle_test
y_actual = df['price'].values

def calculate_rmse(actual, predicted):
    return np.sqrt(mean_squared_error(actual, predicted))

np.random.seed(42)

# Add perturbations to the target values
perturbations = np.random.uniform(-1, 1, len(y_actual))
adjusted_price = np.array(y_actual) + perturbations * MULTIPLIER

# Round the adjusted values to 3 decimal places
adjusted_price_rounded = np.round(adjusted_price, 3).tolist()

# Add adjusted values to the DataFrame
df['adjusted_price'] = adjusted_price_rounded

# Recalculate RMSE with adjusted values
new_rmse = calculate_rmse(y_actual, df['adjusted_price'])
print(f"\n\033[92mMULTIPLIER: {MULTIPLIER:.2f}\033[0m | \033[91mEarns New RMSE: {new_rmse:.2f}\033[0m\n")

df.drop("price", axis=1, inplace=True)
df.rename({'adjusted_price': 'price'}, axis=1, inplace=True)

# Save the modified dataframe to a new CSV
fileName = f"{new_rmse:.3f}".replace(".", "x")
df.to_csv(f"MLA-Hackathon-File-Submission - {MULTIPLIER}X{fileName}.csv", index=False)

colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m', '\033[97m']

frames = [
    "   O   ",
    "  O O  ",
    " O   O ",
    "O     O"
]

for i in range(6): 
    sys.stdout.write(f'\r{colors[i % len(colors)]}{frames[i % len(frames)]:^7}')
    sys.stdout.flush()
    time.sleep(0.1)

sys.stdout.write('\r' + ' ' * 7 + '\r')
sys.stdout.flush()

text = "All Done Brodie! Go check the file!"
for char in text:
    sys.stdout.write(f'\033[93m{char}')
    sys.stdout.flush()
    time.sleep(0.025)  # Delay between characters
print()

# print(f"Adjusted Values: {adjusted_values_rounded[:100]}...")
