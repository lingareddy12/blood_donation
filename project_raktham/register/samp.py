from datetime import datetime


specific_date = '2023-10-22'

# Get the current date
today = datetime.now()


difference = today - specific_date


days_difference = difference.days
print(days_difference)




