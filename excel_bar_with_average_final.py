import pandas as pd
import matplotlib.pyplot as plt
file_path = 'C:/Users/varsh/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Python 3.12/sample.xlsx'
df = pd.read_excel(file_path)
print("Column names:", df.columns)
print(df.head())
df['time'] = pd.to_datetime(df['time'])
df = df.sort_values(by=['user id', 'time'])
df['date'] = df['time'].dt.date
working_hours = []
total_in_out_times = []
for user_id, user_data in df.groupby('user id'):
    user_data = user_data.sort_values(by='time')
    for date, date_data in user_data.groupby('date'):
        if len(date_data) % 2 == 0:
            total_seconds = 0
            in_times = []
            out_times = []
            for i in range(0, len(date_data), 2):
                clock_in = date_data.iloc[i]['time']
                clock_out = date_data.iloc[i + 1]['time']
                total_seconds += (clock_out - clock_in).total_seconds()
                in_times.append(clock_in)
                out_times.append(clock_out)
            working_hours.append({'user id': user_id, 'date': date, 'working_hours': total_seconds / 3600 })
            total_in_out_times.append({'user id': user_id, 'date': date, 'in_times': in_times, 'out_times': out_times})
working_hours_df = pd.DataFrame(working_hours)
total_in_out_times_df = pd.DataFrame(total_in_out_times)
while True:
    user_date_input = input("Enter the date (YYYY-MM-DD) to display working hours and in andout times for each user: ")
    try:
        user_date = pd.to_datetime(user_date_input).date()
        break
    except ValueError:
        print("Invalid date format. Please enter the date in YYYY-MM-DD format.")
filtered_working_hours_df = working_hours_df[working_hours_df['date'] == user_date]
filtered_in_out_times_df = total_in_out_times_df[total_in_out_times_df['date'] == user_date]
if not filtered_in_out_times_df.empty:
    print(f"Total in and out times on {user_date}:")
    for index, row in filtered_in_out_times_df.iterrows():
        print(f"User ID: {row['user id']}")
        for in_time, out_time in zip(row['in_times'], row['out_times']):
            print(f"  In: {in_time}, Out: {out_time}")
    def convert_to_hours(time):
        return time.hour + time.minute / 60 + time.second / 3600
    in_times_data = []
    out_times_data = []
    for index, row in filtered_in_out_times_df.iterrows():
        for in_time in row['in_times']:
            in_times_data.append({'user id': row['user id'], 'time': convert_to_hours(in_time.time()), 'type': 'In Time'})
        for out_time in row['out_times']:
            out_times_data.append({'user id': row['user id'], 'time': convert_to_hours(out_time.time()), 'type': 'Out Time'})
        times_df = pd.DataFrame(in_times_data + out_times_data)
    times_df.pivot_table(index='user id', columns='type', values='time').plot(kind='bar')
    plt.xlabel('User ID')
    plt.ylabel('Time (hours since midnight)')
    plt.title(f'In and Out Times on {user_date}')
    plt.show()
    filtered_working_hours_df.plot(kind='bar', x='user id', y='working_hours')
    plt.xlabel('User ID')
    plt.ylabel('Working Hours')
    plt.title(f'Working Hours on {user_date}')
    plt.show()
else:
    print(f"No data available for the date: {user_date}")
average_hours_per_user = working_hours_df.groupby('user id')['working_hours'].mean()
print("Average working hours per user:")
print(average_hours_per_user)
average_hours_per_user.plot(kind='bar')
plt.xlabel('User ID')
plt.ylabel('Average Working Hours')
plt.title('Average Working Hours per User')
plt.show()
overall_average_hours = working_hours_df['working_hours'].mean()
print("\nOverall average working hours:", overall_average_hours)