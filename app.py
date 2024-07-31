import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Path to the CSV file
ATTENDANCE_DIR = 'Attendance'

def load_attendance_data(date):
    file_path = os.path.join(ATTENDANCE_DIR, f"Attendance_{date}.csv")
    if os.path.isfile(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        st.error("No data available for the selected date.")
        return pd.DataFrame()

def plot_attendance_statistics(df):
    if df.empty:
        st.warning("No data to plot.")
        return
    
    # Plot 1: Attendance count per person
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='NAME', order=df['NAME'].value_counts().index, palette="viridis", hue='NAME', legend=False)
    plt.title("Attendance Count per Person")
    plt.xlabel("Name")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('attendance_count.png')
    plt.close()
    
    # Convert 'TIME' to hour and count attendance
    df['TIME'] = pd.to_datetime(df['TIME'], format='%H:%M:%S', errors='coerce')
    df = df.dropna(subset=['TIME'])
    df = df.copy()  # To avoid SettingWithCopyWarning
    df['Hour'] = df['TIME'].dt.hour
    hourly_counts = df.groupby('Hour').size().reset_index(name='Count')

    plt.figure(figsize=(12, 6))
    plt.plot(hourly_counts['Hour'], hourly_counts['Count'], marker='o', linestyle='-', color='b')
    plt.title("Attendance Count by Hour")
    plt.xlabel("Hour of the Day")
    plt.ylabel("Count")
    plt.xticks(range(24), [f"{h}:00" for h in range(24)], rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('attendance_by_hour.png')
    plt.close()

def show_plots():
    if os.path.isfile('attendance_count.png'):
        st.image('attendance_count.png', caption='Attendance Count per Person')
    
    if os.path.isfile('attendance_by_hour.png'):
        st.image('attendance_by_hour.png', caption='Attendance Count by Hour')

def show_data(df):
    st.dataframe(df)

def main():
    st.title("Real-Time Face Recognition")

    st.sidebar.title("Control Panel")

    # Select Date
    date = st.sidebar.date_input("Select Date", pd.to_datetime("today").date())
    date_str = date.strftime("%d-%m-%Y")

    # Load data
    df = load_attendance_data(date_str)

    # Separate Sections for Data and Plots
    section = st.sidebar.radio("Select Section", ["Attendance Data", "Plots"])

    if section == "Attendance Data":
        if not df.empty:
            show_data(df)
        else:
            st.write("No attendance data available for the selected date.")

    elif section == "Plots":
        if not df.empty:
            plot_attendance_statistics(df)
            show_plots()
        else:
            st.write("No data available to generate plots.")

if __name__ == '__main__':
    main()
