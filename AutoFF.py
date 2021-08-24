import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def pl_week(importFile, week_number,total='total.csv'):
    #print("type csv file name")
    #importFile = input()
    df = pd.read_csv(importFile)
    answers = df.iloc[-1]
    number_of_games = answers.size
    weeklyDict={}
    sum_dict={}
    username_list=[]
    for index, row in df.iterrows():
        if row[0] == "ans":
            break
        userPointList = []
        userPoints = 0
        username = row[1].lower()
        username_list.append(username)
        for i in range(2, number_of_games): 
            userPred = row[i].replace(" ","");
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
    #week_number = int(input("Week #? "))
    week_index = "W{}".format(week_number)
    #for key, value in totals_dict.items():
    #    if value == []:
    #        week_index = key
    #        break
    if week_index not in totals_df.columns:
        totals_df.insert(week_number, week_index, 0)
    totals_dict = totals_df.to_dict('list')
    
    for x in username_list:
        if x not in totals_dict['username']:
            totals_dict['username'].append(x)
    
    for key, value in totals_dict.items():
        if value == ['']*30:
            totals_dict[key] = []
    
    
    ##totals_dict[week_index] = ['']*30
    
    for index, user in enumerate(totals_dict['username']):
        if user.lower() in sum_dict.keys():
            print(user,index,week_index)
            totals_dict[week_index][index] = sum_dict[user]
    
    for key,value in totals_dict.items(): 
            for index, item in enumerate(totals_dict[key]):
                if item == '':
                    totals_dict[key][index] = 0
                    
    ##totals_dict["Total"] = ['']*30
    
    # calculate total
    for index, user in enumerate(totals_dict['username']):
        #if totals_dict["Total"][index] == '':
        totals_dict["Total"][index] = 0
        for i in range(1,week_number+1):
            totals_dict["Total"][index]  += totals_dict["W{}".format(i)][index]        
    
    weeklyData = weeklyData.sort_values(by=["Total Points"],ascending=False)
    #weeklyData.reset_index(drop=True,inplace=True)
    weeklyData.to_csv('weekly.csv')
    totals_data = pd.DataFrame({ key:pd.Series(value) for key, value in totals_dict.items() })
    totals_data = totals_data.sort_values(by=["Total"],ascending= False)
    totals_data['Rank'] =  np.array(totals_data['Total'].rank(method='min',ascending = False).tolist(),dtype=int)
    totals_data.reset_index(drop=True,inplace=True)
    totals_data.to_csv('total.csv', index=False)
    totals_data = totals_data.set_index("username")
    
    normal = np.array(weeklyData.values - weeklyData.values.min(0),dtype=np.float) / np.array(weeklyData.values.max(0) - weeklyData.values.min(0),dtype=np.float)
    #normal[:,0:-2] = 0
    #cellColours=normal
    #cellColours[:,-2:-1] = plt.cm.RdYlGn(normal[:,-2:-1])
    #fig = plt.figure()
    fig, ax = plt.subplots(1,1)
    ax.axis('tight')
    ax.axis('off')
    #print(normal)
    rlab = weeklyData.index.tolist()
    clab = weeklyData.columns.tolist()
    vals = weeklyData.values.tolist()
    the_table=ax.table(cellText=vals, rowLabels=rlab, colLabels=clab, 
                       loc='center', cellColours=plt.cm.RdYlGn(normal))
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)
    the_table.auto_set_column_width(col=list(range(len(weeklyData.columns))))
    #the_table.scale(2, 2)
    #ax.set_xlim(-10, 10)
    #plt.subplots_adjust(bottom=0.2)
    the_table.scale(1,2)
    fig.savefig("weektable.pdf",bbox_inches="tight", pad_inches=0.25)
    plt.show()
    #normals = np.zeros(totals_data.shape)
    normal = np.array(totals_data.values - totals_data.values.min(0),dtype=np.float) / np.array(totals_data.values.max(0) - totals_data.values.min(0),dtype=np.float)
    #print(totals_data.values)
    #print(totals_data.values - totals_data.values.min(0))
    #print(totals_data.values.max(0))
    normals = normal
    fig2, ax2 = plt.subplots(1,1)
    ax2.axis('tight')
    ax2.axis('off')
    
    the_table=ax2.table(cellText=totals_data.values, rowLabels=totals_data.index, colLabels=totals_data.columns, 
                       loc='center', cellColours=plt.cm.RdYlGn(normals))
    the_table.auto_set_font_size(False)
    the_table.set_fontsize(10)
    the_table.auto_set_column_width(col=list(range(len(weeklyData.columns))))
    the_table.scale(1,2)
    #print(totals_data.values)
    fig2.savefig("totaltable.pdf",bbox_inches="tight", pad_inches=0.25)
    plt.show()