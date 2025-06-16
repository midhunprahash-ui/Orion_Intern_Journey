import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create Dataframes for all the sheets

df1 = pd.read_excel('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_3/Files/10062025.xlsx')
df2 = pd.read_excel('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_3/Files/11062025.xlsx')
df3 = pd.read_excel('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_3/Files/12062025.xlsx')
df4 = pd.read_excel('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_3/Files/13062025.xlsx')
df5 = pd.read_excel('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_3/Files/14062025.xlsx')
df6 = pd.read_excel('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_3/Files/15062025.xlsx')

# Extract the rquired coloumns alone

c1=df1['Execution Status']
c2=df2['Execution Status']
c3=df3['Execution Status']
c4=df4['Execution Status']
c5=df5['Execution Status']
c6=df6['Execution Status']

# Getting the count of values in the required coloumn

count1 = df1['Execution Status'].value_counts()
count2 = df2['Execution Status'].value_counts()
count3 = df3['Execution Status'].value_counts()
count4 = df4['Execution Status'].value_counts()
count5 = df5['Execution Status'].value_counts()
count6 = df6['Execution Status'].value_counts()


