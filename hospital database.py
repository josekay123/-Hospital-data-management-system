import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Function to add new data based on user input
def add_new_record(df):
    # Prompt user for input
    admission_date = input("Enter admission date (YYYY-MM-DD): ")
    recovery_date = input("Enter recovery date (YYYY-MM-DD): ")
    patient_id = input("Enter patient ID: ")
    age = int(input("Enter patient's age: "))
    gender = input("Enter patient's gender (Male/Female): ")
    diagnosis = input("Enter diagnosis (Flu, COVID-19, Fracture, Heart Disease, Diabetes): ")
    status = input("Enter recovery status (Recovered, Deceased, Under Treatment): ")

    # Add the new record to the dataframe
    new_record = {
        'admission_date': pd.to_datetime(admission_date),
        'recovery_date': pd.to_datetime(recovery_date),
        'patient_id': patient_id,
        'age': age,
        'gender': gender,
        'diagnosis': diagnosis,
        'status': status,
        'stay_duration': (pd.to_datetime(recovery_date) - pd.to_datetime(admission_date)).days
    }
    df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True) 
    print("New record added successfully!")
    return df

# Function to modify existing data by patient_id based on user input
def modify_record(df):
    # Prompt user to enter the patient ID they want to modify
    patient_id = input("Enter the patient ID to modify: ")
    record = df[df['patient_id'] == patient_id]

    if record.empty:
        print(f"No record found with patient_id: {patient_id}")
        return df

    print(f"Current data for patient {patient_id}:")
    print(record)

    # Prompt for fields to modify
    admission_date = input(f"Enter new admission date (current: {record['admission_date'].values[0]}): ")
    recovery_date = input(f"Enter new recovery date (current: {record['recovery_date'].values[0]}): ")
    age = input(f"Enter new age (current: {record['age'].values[0]}): ")
    gender = input(f"Enter new gender (current: {record['gender'].values[0]}): ")
    diagnosis = input(f"Enter new diagnosis (current: {record['diagnosis'].values[0]}): ")
    status = input(f"Enter new status (current: {record['status'].values[0]}): ")

    # Update the record with new values
    df.loc[df['patient_id'] == patient_id, 'admission_date'] = pd.to_datetime(admission_date) if admission_date else record['admission_date'].values[0]
    df.loc[df['patient_id'] == patient_id, 'recovery_date'] = pd.to_datetime(recovery_date) if recovery_date else record['recovery_date'].values[0]
    df.loc[df['patient_id'] == patient_id, 'age'] = int(age) if age else record['age'].values[0]
    df.loc[df['patient_id'] == patient_id, 'gender'] = gender if gender else record['gender'].values[0]
    df.loc[df['patient_id'] == patient_id, 'diagnosis'] = diagnosis if diagnosis else record['diagnosis'].values[0]
    df.loc[df['patient_id'] == patient_id, 'status'] = status if status else record['status'].values[0]

    df['stay_duration'] = (df['recovery_date'] - df['admission_date']).dt.days
    print("Record updated successfully!")
    return df

# Function to save the dataset to a CSV file
def save_to_csv(df, filename='hospital_data.csv'):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Visualization: Top 10 diagnoses by patient count
def plot_top_diagnoses(df):
    diagnosis_stats = df.groupby('diagnosis').size().reset_index(name='patient_count')
    top_diagnoses = diagnosis_stats.sort_values(by='patient_count', ascending=False).head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='patient_count', y='diagnosis', data=top_diagnoses, palette='viridis')
    plt.title('Top 10 Diagnoses by Patient Count')
    plt.xlabel('Patient Count')
    plt.ylabel('Diagnosis')
    plt.show()

# Trend analysis: Admissions over time
def plot_admissions_trend(df):
    admissions_trend = df.groupby('admission_date').size().reset_index(name='admissions')
    
    plt.figure(figsize=(12, 6))
    plt.plot(admissions_trend['admission_date'], admissions_trend['admissions'], label='Admissions', color='blue')
    plt.title('Hospital Admissions Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Admissions')
    plt.grid(True)
    plt.show()

# Main menu loop
def main():
    # Initialize an empty dataframe to start
    data = pd.DataFrame(columns=['admission_date', 'recovery_date', 'patient_id', 'age', 'gender', 'diagnosis', 'status', 'stay_duration'])
    
    while True:
        print("\nMenu:")
        print("1. Add New Data")
        print("2. Modify Existing Data")
        print("3. Plot the Trends")
        print("4. Save Data and Exit")
        
        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            # Add new record
            data = add_new_record(data)
        elif choice == '2':
            # Modify existing record
            data = modify_record(data)
        elif choice == '3':
            # Plot the trends (top diagnoses & admissions trend)
            plot_top_diagnoses(data)
            plot_admissions_trend(data)
        elif choice == '4':
            # Save data and exit
            save_to_csv(data)
            print("Exiting program...")
            break
        else:
            print("Invalid choice! Please choose a valid option.")

# Run the main function
if __name__ == "__main__":
    main()
