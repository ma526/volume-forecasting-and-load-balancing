import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Constants
NUM_SKUS = 50
NUM_ZIPCODES = 10
NUM_DAYS = 180
START_DATE = datetime(2024, 11, 1)

# Generate SKU and Zipcode combinations
skus = [f'SKU_{i:03d}' for i in range(1, NUM_SKUS + 1)]
zip_codes = [f'{random.randint(10000, 99999)}' for _ in range(NUM_ZIPCODES)]

# Generate historical order data
dates = [START_DATE + timedelta(days=i) for i in range(NUM_DAYS)]
data = []

for date in dates:
    day_of_week = date.weekday()
    for sku in skus:
        for zip_code in zip_codes:
            base = random.randint(5, 50)
            seasonal = 5 if day_of_week in [4, 5] else 0  # spike on Fri/Sat
            noise = np.random.poisson(10)
            volume = base + seasonal + noise
            data.append([date.strftime("%Y-%m-%d"), sku, zip_code, volume])

df_orders = pd.DataFrame(data, columns=["date", "sku", "zip_code", "volume"])

# Generate delivery partner profiles
partner_ids = [f'Partner_{i:02d}' for i in range(1, 16)]
partner_data = []

for pid in partner_ids:
    capacity = random.randint(600, 3000)
    on_time_perf = round(random.uniform(85, 99), 2)
    cost = round(random.uniform(0.5, 2.0), 2)
    partner_data.append([pid, capacity, on_time_perf, cost])

df_partners = pd.DataFrame(partner_data, columns=["partner_id", "daily_capacity", "on_time_percent", "cost_per_package"])

# Calendar features
holidays = pd.date_range(start=START_DATE, periods=NUM_DAYS, freq='7D').to_list()
calendar_data = []

for date in dates:
    dow = date.weekday()
    is_weekend = 1 if dow in [5, 6] else 0
    is_holiday = 1 if date in holidays else 0
    calendar_data.append([date.strftime("%Y-%m-%d"), dow, is_weekend, is_holiday])

df_calendar = pd.DataFrame(calendar_data, columns=["date", "day_of_week", "is_weekend", "is_holiday"])

# Save to /mnt/data for download
base_path = "data/"
os.makedirs(base_path, exist_ok=True)

df_orders.to_csv(f"{base_path}/generated_orders.csv", index=False)
df_partners.to_csv(f"{base_path}/delivery_partners.csv", index=False)
df_calendar.to_csv(f"{base_path}/calendar_features.csv", index=False)

f"Data generated and saved to {base_path}"
