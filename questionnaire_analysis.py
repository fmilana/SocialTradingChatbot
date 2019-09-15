# coding: utf-8
import sys
from itertools import product
import pandas as pd
import numpy as np
import ast

df = pd.read_csv(sys.argv[1])
print(df['answer'].head())

# this converts the strings to python lists and dictionaries
# storing the result in a new column 'decoded'
df['decoded'] = df['answer'].apply(ast.literal_eval)
print(df['decoded'].head())

# select chart tasks
#df = df.loc[type(df['decoded']) == type()]
df = df.loc[df['answer'].str.startswith('[')]
print(df['decoded'].head())

df.to_csv('tmp.csv')

# study_groups = ['group-A','group-B','group-C']

# # create new columns for each of the groups
# # each column will contain a python set
# for group_name in study_groups:
#     print(group_name)
#     df[group_name] = df['decoded'].apply(lambda x: set(x[group_name]))
    
#     # print(df[group_name])

# now you can select a subset of rows and then process them
# as a random example, I will select the even and odd numbered participants
# in reality you should select based on the task number
# you can check the django admin to see the ID of different tasks 
# and the better way to do this would be to use groupby
#groups = df.groupby('task')
groups = df.groupby('user__participant__condition_active')

all_dataframes = []

# for task_label, task_data in groups:
for index, row in df.iterrows():
    print('-----')
    #print("%s (N=%d tasks)" % (task_label, len(task_data)))
    task_label = row['user__participant__condition_active']
    # print(task_data['participant__task_list__name'])
    # print(task_data)
    # print(task_label)
    questions = []
    answers = []
    task_lists = []
    for item in row['decoded']:
        print (item)
        if item == '':
            continue
        questions.append(item['question'])
        answer = item['answer']
        answer = answer.strip().lstrip()
        if answer.startswith('1 -') or answer.startswith('5 - '):
            answer = answer[0]
        answers.append(answer)
    
    
    current = pd.DataFrame()
    current['questions'] = questions
    current['answers'] = answers
    #current['task'] = task_label
    current['user__participant__condition_active'] = row['user__participant__condition_active']
    current['participant'] = row['user']

    print(current.head())
    all_dataframes.append(current)

results = pd.concat(all_dataframes)
results.to_csv('questionnaire_data.csv', index=False)
