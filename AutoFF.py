import pandas as pd

print("type csv file name")
importFile = input()
df = pd.read_csv(importFile)
answers = df.iloc[23]
weeklyDict={}
sum_dict={}
username_list=[]
for index, row in df.iterrows():
    if row[0] == "ans":
        break
    userPointList = []
    userPoints = 0
    username = row[1]
    username_list.append(username)
    for i in range(2, 12): 
        userPred = row[i]
        ans = answers[i]
        if userPred == ans:
            matchPoints = 7
        elif int(ans[0]) - int(ans[2]) == int(userPred[0]) - int(userPred[2]):
            matchPoints = 4
        elif (int(ans[0]) - int(ans[2]))*(int(userPred[0]) - int(userPred[2])) > 0:
            matchPoints = 3
        else:
            matchPoints = 0
        userPointList.append(matchPoints)
        userPoints += matchPoints
    userPointList.append(userPoints)
    weeklyDict[username] = userPointList
    sum_dict[username] = userPoints

collumnList = list(df.columns.values)
collumnList. pop(0)
collumnList. pop(0)
collumnList.append("Total Points")

weeklyData = pd.DataFrame.from_dict(weeklyDict, orient='index', columns=collumnList)

totals_df = pd.read_csv('total.csv', keep_default_na=False)
totals_dict = totals_df.to_dict('list')

for x in username_list:
    if x not in totals_dict['username']:
        totals_dict['username'].append(x)

for key, value in totals_dict.items():
    if value == ['']*30:
        totals_dict[key] = []

for key, value in totals_dict.items():
    if value == []:
        week_index = key
        break

totals_dict[week_index] = ['']*30

for index, user in enumerate(totals_dict['username']):
    if user in sum_dict.keys():
        totals_dict[week_index][index] = sum_dict[user]

weeklyData.to_csv('weekly.csv')
totals_data = pd.DataFrame({ key:pd.Series(value) for key, value in totals_dict.items() })
totals_data.to_csv('total.csv', index=False)