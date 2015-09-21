import sys
import numpy as np
import datetime
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import data_reader
import toolkit

def usage_information():
    info = 'Lab report generator for CS61a\n'
    info += 'Usage: cross_lab_report.py <data_file_directory>'
    return info

if len(sys.argv) < 2:
    print usage_information()
print 'Generate cross-lab report'

os.chdir('../report')
if not os.path.exists('cross_lab_report'):
    os.makedirs('cross_lab_report')
os.chdir('./cross_lab_report')

LABS = ['lab01', 'lab02', 'lab03']
LAB_NUMBER = len(LABS)
################
### Get data ###
################
data_list = [data_reader.SetupData(sys.argv[1], lab) for lab in LABS]
data_set_list = [data.data_set for data in data_list]

##################################
### Initialize latex formatter ###
##################################
formatter = toolkit.LatexFormatter(os.getcwd()+'/../template/', 'cross_lab_report.tex')

################################
### Participation infomation ###
################################
participation_table = {}
for index, data_set in enumerate(data_set_list):
    selected_data = data_set.map(lambda x: x['student']).distinct()
    for student in selected_data:
        if participation_table.has_key(student):
            participation_table[student].append(index)
        else:
            participation_table[student] = [index]
# print participation_table
################################################
### Figure for number of labs joined per lab ###
################################################
plot_data = [[0 for i in xrange(LAB_NUMBER)] for j in xrange(LAB_NUMBER)]
for student in participation_table:
    status = participation_table[student]
    for lab in status:
        plot_data[LAB_NUMBER-len(status)][lab] += 1
fig, ax = toolkit.prepare_plot(gridWidth=0)
tem_bottom = [0] * LAB_NUMBER
color = plt.cm.Blues_r(np.linspace(.2, .8, LAB_NUMBER))
p = []
ind = np.arange(LAB_NUMBER)
width=.5
for i in range(LAB_NUMBER):
    bar = plt.bar(ind, plot_data[i], width, color=color[i], bottom=tem_bottom, edgecolor=color[i])
    p.append(bar)
    for j in range(LAB_NUMBER):
        tem_bottom[j] += plot_data[i][j]
plt.ylabel('Number of students')
plt.title('Number of other labs a student has participated in')
plt.xticks(ind+width/2., LABS)
# plt.yticks(np.arange(0,81,10))
plt.legend(p, ('{} other lab(s)'.format(LAB_NUMBER-x-1) for x in range(LAB_NUMBER)))
plt.savefig('lab_cnt.png')

############################################
### Figure for participation information ###
############################################
plot_data = [0] * LAB_NUMBER
for student in participation_table:
    num = len(participation_table[student])-1
    plot_data[num] += 1
fig, ax = toolkit.prepare_plot(gridWidth=0)
rects = plt.bar(np.arange(LAB_NUMBER), plot_data, color='gray', edgecolor='gray')
plt.xticks(ind+width/2., ['{} Labs'.format(x+1) for x in range(LAB_NUMBER)])
plt.title("Number of labs a student has participated in")
toolkit.autolabel(rects, ax)
plt.savefig('participation.png')

#############################################
### Heatmap for participation information ###
#############################################
heat_map = []
for student in participation_table:
    student_record = [0] * LAB_NUMBER
    for lab in participation_table[student]:
        student_record[lab] = len(participation_table[student]) / float(LAB_NUMBER)
    heat_map.append(student_record)
for i in reversed(range(LAB_NUMBER)):
    heat_map = sorted(heat_map, key=lambda x: -x[i])
heat_map = sorted(heat_map, key=lambda x: -toolkit.get_length(x))
heat_map = np.array(heat_map)
fig, ax = toolkit.prepare_plot(gridWidth=0)
ax.pcolor(heat_map, cmap=plt.cm.Blues)
plt.ylim([0, len(heat_map)])
plt.xticks(np.arange(LAB_NUMBER)+0.5, LABS)
plt.ylabel("Students")
patches = []
for i in range(LAB_NUMBER):
    patches.append(mpatches.Patch(color=plt.cm.Blues((i+1)/float(LAB_NUMBER)), label='{} Labs'.format(i+1)))
plt.legend(handles=patches)
plt.savefig('heatmap.png')


###########################
### Render latex report ###
###########################
formatter.render('cross_lab_report.tex')
