import pandas as pd

importFile = input()
df = pd.read_csv(importFile)
answers = df.iloc[100]
my_dict={}
for index, row in df.iterrows():
    username = row['B'].to_string()
    userPoints
    for i in range(2, 12):
        matchPoints
        userPred = row[i].to_string()
        ans = answers[i].to_string()
        if userPred == ans:
            matchPoints = 7
        elif ans[0] - ans[2] == userPred[0] - userPred[2]:
            matchPoints = 4
        elif (ans[0] - ans[2])*(userPred[0] - userPred[2]) > 0:
            matchPoints = 3
        userPoints += matchPoints
    my_dict[username] = userPoints

for key,val in my_dict.items():
    print(key, "=>", val)
input()