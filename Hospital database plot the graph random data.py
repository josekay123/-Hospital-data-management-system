!pip install faker
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from faker import Faker
import random

# Generate random data for hospital admissions
fake = Faker()
def generate_random_data(n=1000):
    data = {
        'admission_date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(n)],
        'recovery_date': [fake.date_between(start_date='-1y', end_date='today') for _ in range(n)],
        'patient_id': [fake.uuid4() for _ in range(n)],
        'age': [random.randint(1, 100) for _ in range(n)],
        'gender': [random.choice(['Male', 'Female']) for _ in range(n)],
        'diagnosis': [random.choice(['Flu', 'COVID-19', 'Fracture', 'Heart Disease', 'Diabetes']) for _ in range(n)],
        'status': [random.choice(['Recovered', 'Deceased', 'Under Treatment']) for _ in range(n)]
    }
    data['recovery_date'] = [
        rec if rec >= adm else adm + pd.Timedelta(days=random.randint(1, 20))
        for adm, rec in zip(data['admission_date'], data['recovery_date'])
    ]
    return pd.DataFrame(data)

# Replace 'hospital_data.csv' with generated random data
data = generate_random_data(1000)

# Display the first few rows to understand the structure of the dataset
if not data.empty:
    print("Dataset Preview:")
    print(data.head())
else:
    print("The dataset is empty. Skipping preview.")

# Check for missing values and handle them
def handle_missing_data(df):
    if df.empty:
        print("The dataset is empty. No missing data to handle.")
        return df
    print("Missing values per column:")
    print(df.isnull().sum())
    df = df.fillna(0)  # Example: Replace missing values with 0
    return df

data = handle_missing_data(data)

# Basic descriptive statistics
if not data.empty:
    print("Descriptive Statistics:")
    print(data.describe())
else:
    print("The dataset is empty. Skipping descriptive statistics.")

# Select relevant columns for analysis (ensure the columns exist)
required_columns = ['admission_date', 'patient_id', 'age', 'gender', 'diagnosis', 'recovery_date', 'status']
if not data.empty and not all(col in data.columns for col in required_columns):
    print("Error: One or more required columns are missing from the dataset.")
    data = pd.DataFrame()  # Reset to empty to avoid further processing

if not data.empty:
    data = data[required_columns]

# Convert 'admission_date' and 'recovery_date' columns to datetime format
if not data.empty:
    try:
        data['admission_date'] = pd.to_datetime(data['admission_date'])
        data['recovery_date'] = pd.to_datetime(data['recovery_date'])
    except Exception as e:
        print(f"Error converting date columns to datetime: {e}")
        data = pd.DataFrame()  # Reset to empty to avoid further processing

# Calculate hospital stay duration
if not data.empty:
    data['stay_duration'] = (data['recovery_date'] - data['admission_date']).dt.days
    print("Updated Data with Stay Duration:")
    print(data.head())

# Group by diagnosis and calculate statistics
if not data.empty:
    diagnosis_stats = data.groupby('diagnosis').agg({
        'stay_duration': ['mean', 'median'],
        'patient_id': 'count'
    }).reset_index()
    diagnosis_stats.columns = ['diagnosis', 'mean_stay_duration', 'median_stay_duration', 'patient_count']
    print("Diagnosis-level Aggregated Data:")
    print(diagnosis_stats.head())
else:
    print("The dataset is empty. Skipping diagnosis-level aggregation.")

# Visualization: Top 10 diagnoses by patient count
if not data.empty:
    top_diagnoses = diagnosis_stats.sort_values(by='patient_count', ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x='patient_count', y='diagnosis', data=top_diagnoses, palette='viridis')
    plt.title('Top 10 Diagnoses by Patient Count')
    plt.xlabel('Patient Count')
    plt.ylabel('Diagnosis')
    plt.show()
else:
    print("The dataset is empty. Skipping top diagnoses visualization.")

# Trend analysis: Admissions over time
if not data.empty:
    admissions_trend = data.groupby('admission_date').size().reset_index(name='admissions')
    plt.figure(figsize=(12, 6))
    plt.plot(admissions_trend['admission_date'], admissions_trend['admissions'], label='Admissions', color='blue')
    plt.title('Hospital Admissions Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Admissions')
    plt.grid()
    plt.show()
else:
    print("The dataset is empty. Skipping admissions trend analysis.")

# Additional Visualization: Stay duration distribution
if not data.empty:
    plt.figure(figsize=(10, 6))
    sns.histplot(data['stay_duration'], bins=20, kde=True, color='green')
    plt.title('Distribution of Hospital Stay Duration')
    plt.xlabel('Stay Duration (days)')
    plt.ylabel('Frequency')
    plt.show()
else:
    print("The dataset is empty. Skipping stay duration distribution visualization.")

# Recovery status breakdown
if not data.empty:
    recovery_status = data['status'].value_counts().reset_index()
    recovery_status.columns = ['status', 'count']
    plt.figure(figsize=(8, 6))
    sns.barplot(x='count', y='status', data=recovery_status, palette='coolwarm')
    plt.title('Recovery Status Breakdown')
    plt.xlabel('Count')
    plt.ylabel('Status')
    plt.show()
else:
    print("The dataset is empty. Skipping recovery status breakdown visualization.")
