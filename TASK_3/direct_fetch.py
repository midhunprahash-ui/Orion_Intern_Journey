import pandas as pd
import matplotlib.pyplot as plt


df1 = pd.read_excel('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_3/Files/10062025.xlsx')
df2 = pd.read_excel('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_3/Files/11062025.xlsx')
df3 = pd.read_excel('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_3/Files/12062025.xlsx')
df4 = pd.read_excel('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_3/Files/13062025.xlsx')
df5 = pd.read_excel('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_3/Files/14062025.xlsx')
df6 = pd.read_excel('/Users/midhun/Developer/Git/Orion_Intern_Journey/TASK_3/Files/15062025.xlsx')

c1=df1['Execution Status']
c2=df2['Execution Status']
c3=df3['Execution Status']
c4=df4['Execution Status']
c5=df5['Execution Status']
c6=df6['Execution Status']

co1 = c1.value_counts()
co2 = c2.value_counts()
co3 = c3.value_counts()
co4 = c4.value_counts()
co5 = c5.value_counts()
co6 = c6.value_counts()



counts_df = pd.DataFrame({
    '10-06-2025': co1,
    '11-06-2025': co2,
    '12-06-2025': co3,
    '13-06-2025': co4,
    '14-06-2025': co5,
    '15-06-2025': co6
}).fillna(0) 

counts_df = counts_df.T


counts_df.plot(kind='bar', stacked=True, figsize=(10,6))

plt.title('Trend of Execution Status Counts Over Dates')
plt.xlabel('Date')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.legend(title='Execution Status')
plt.tight_layout()
plt.show()
