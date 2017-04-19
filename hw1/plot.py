'''
Some plot function sketchs
'''
import problem1

# subtypes of interests from 311 requests by category.

requests_types_response = ['graffitti', 'pothole', 'sanitation']

# for generating subtype information
from pprint import pprint
with open('subtype_table.txt', 'wt') as out:
    pprint('What Type of Surface is the Graffiti on?', stream=out)
    pprint(graffitti['What Type of Surface is the Graffiti on?'].value_counts(), stream=out)
    pprint('What is the Nature of this Code Violation?', stream=out)
    pprint(sanitation['What is the Nature of this Code Violation?'].value_counts(), stream=out)
    pprint('NUMBER OF POTHOLES FILLED ON BLOCK', stream=out)
    pprint(pothole['NUMBER OF POTHOLES FILLED ON BLOCK'].value_counts(), stream=out)
    pprint('ANY PEOPLE USING PROPERTY? (HOMELESS, CHILDEN, GANGS)', stream=out)
    pprint(building['ANY PEOPLE USING PROPERTY? (HOMELESS, CHILDEN, GANGS)'].value_counts(), stream=out)

avg_response_time = []
for i in requests_types_response:
    avg_response_time.append(requests_2016[i]['by response time']['average'])

import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style = 'whitegrid')

# 1. total requests by category graph
total_by_cat = []
for i in requests_2016:
    total_by_cat.append(requests_2016[i]['total'])

TOTAL = 178831

total_by_cat_percent = []
for i in total_by_cat:
    total_by_cat_percent.append(i/TOTAL)
# Initialize the matplotlib figure
x = graffitti['What Type of Surface is the Graffiti on?'].value_counts()
y = graffitti['What Type of Surface is the Graffiti on?'].value_counts().index

plot = sns.barplot(x,y)
plt.xlabel('count')
plt.ylabel('subtype')
sns.despine(top=True, bottom=True, left=True)
plt.title('Number of graffiti removal requests by subtype', x=300, y=200)
plt.show()
# fig = plot.get_figure()
# fig.savefig("output.png")

# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns
# #
# x = graffitti['What Type of Surface is the Graffiti on?'].value_counts()
# y = graffitti['What Type of Surface is the Graffiti on?'].value_counts().index
# sns.set_context(rc={"figure.figsize": (8, 77)})
# nd = np.arange(3)
# width=0.8
# # plt.xticks(nd+width/2., ('1','1000','1001'))
# plt.xlim(-0.15,3)
# fig = plt.bar(nd, y, color=sns.color_palette("Blues",77))
# plt.legend(fig, ['First','Second','Third'], loc = "upper left", title = "cat")
