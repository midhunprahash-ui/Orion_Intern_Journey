import pandas as pd
# Read the CSV file
df =pd.read_csv('employees.csv')

# Convert to JSON file
df.to_json('employees.json',orient='records',lines=True)
