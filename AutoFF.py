import pandas as pd

print("type csv file name")
importFile = input()
df = pd.read_csv(importFile)
answers = df.iloc[23]
my_dict={}
for index, row in df.iterrows():
    if row[0] == "ans":
        break
    userPointList = []
    userPoints = 0
    username = row[1]
    for i in range(2, 12): 
        userPred = row[i]
        ans = answers[i]
        if userPred == ans:
            matchPoints = 7
        elif int(ans[0]) - int(ans[2]) == int(userPred[0]) - int(userPred[2]):
            matchPoints = 4
        elif (int(ans[0]) - int(ans[2]))*(int(userPred[0]) - int(userPred[2])) > 0:
            matchPoints = 3
        userPointList.append(matchPoints)
        userPoints += matchPoints
    userPointList.append(userPoints)
    my_dict[username] = userPointList

collumnList = list(df.columns.values)
collumnList. pop(0)
collumnList. pop(0)
collumnList.append("Total Points")

finalData = pd.DataFrame.from_dict(my_dict, orient='index', columns=collumnList)
finalData.to_csv('out.csv')