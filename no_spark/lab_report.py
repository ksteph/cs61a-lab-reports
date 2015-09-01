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
    info += 'Usage: lab_report.py <data_file_directory> <lab_name>'
    return info

if len(sys.argv) < 3:
    print usage_information()
print 'Generate report for {}'.format(sys.argv[2])

os.chdir('../report')
if not os.path.exists('{}_report'.format(sys.argv[2])):
    os.makedirs('{}_report'.format(sys.argv[2]))
os.chdir('./{}_report'.format(sys.argv[2]))

################
### Get data ###
################
data = data_reader.SetupData(sys.argv[1], sys.argv[2])
data_set = data.data_set

#########################
### Basic information ###
#########################
NUM_STUDENT = data_set.get_element_count('student')
NUM_QUESTION = data_set.get_element_count('specifier')
NUM_SUBMISSION = data_set.count()
NUM_DISTINCT_ANSWER = data_set.get_element_count('answer')
NUM_WRONG_ANSWER = data_set.filter_by(lambda x: not x['result']).count()

######################################
### Number of sessions per student ###
######################################
session_counter = []
tem_data = data_set.sort_by(lambda x: x['a_time']).group_by(lambda x: x['student'])
for item in tem_data:
    # WARNING: This may throw an exception!
    session_cnt = toolkit.get_session_info(item[1])
    if session_cnt == 0:
        continue
    while session_cnt > len(session_counter):
        session_counter.append(0)
    session_counter[session_cnt-1] += 1

# Print it out
fig, ax = toolkit.prepare_plot(gridWidth=0)
x = np.arange(len(session_counter))
width = 0.5
rects = plt.bar(x, session_counter, width, color='gray', alpha=0.7, edgecolor="gray")
plt.ylabel('Number of students')
plt.xticks(x + width/2., ["{:,} session(s)".format(item+1) for item in range(len(session_counter))])
toolkit.autolabel(rects, ax)
plt.savefig('session_cnt.png')

########################################
### Number of submissions per prompt ###
########################################
submission_counter = [0] * NUM_QUESTION
for prompt in range(NUM_QUESTION):
    submission_counter[prompt] = data_set.filter_by(lambda x: x['specifier']==prompt).count()

# Print it out
width = 0.5
fig, ax = toolkit.prepare_plot(gridWidth=0)
x = np.arange(NUM_QUESTION)
rects = plt.bar(x, submission_counter, width, color='gray', alpha=0.7, edgecolor="gray")
plt.ylabel('Number of submissions')
plt.xticks(x + width/2., [item for item in range(NUM_QUESTION)])
plt.xlabel('Prompt ID')
toolkit.autolabel(rects, ax, 2)
plt.savefig('submission_per_prompt.png')

#################################################
### Number of unique wrong answers per prompt ###
#################################################
unique_answer_counter = [0] * NUM_QUESTION
for prompt in range(NUM_QUESTION):
    unique_answer_counter[prompt] = data_set.filter_by(lambda x: x['specifier']==prompt and not x['result']).get_element_count('answer')
# Print it out
width = 0.5
fig, ax = toolkit.prepare_plot(gridWidth=0)
x = np.arange(NUM_QUESTION)
rects = plt.bar(x, unique_answer_counter, width, color='gray', alpha=0.7, edgecolor="gray")
plt.ylabel('Number of unique answers')
plt.xticks(x + width/2., [item for item in range(NUM_QUESTION)])
plt.xlabel('Prompt ID')
toolkit.autolabel(rects, ax, 2)
plt.savefig('unique_answer_per_prompt.png')

#####################################
### Number of attempts per prompt ###
#####################################
attempt_counter = [[0 for i in xrange(10)] for j in xrange(NUM_QUESTION)]
for prompt in range(NUM_QUESTION):
    tem_data = data_set.filter_by(lambda x: x['specifier']==prompt)
    tem_data = tem_data.group_by(lambda x: x['student']).map(lambda x: len(x[1]))
    for item in tem_data:
        attempt_counter[prompt][np.min([item-1, 9])] += 1
attempt_counter = np.array(attempt_counter).T
# print result
ind = np.arange(NUM_QUESTION)
width = 0.5
fig, ax = toolkit.prepare_plot(gridWidth=0)
tem_bottom = [0]*NUM_QUESTION
color = plt.cm.Blues(np.linspace(0, 1, 10))
p = []
for i in range(10):
    bar = plt.bar(ind, attempt_counter[i], width, color=color[i], bottom=tem_bottom, edgecolor=color[i])
    p.append(bar)
    for j in range(NUM_QUESTION):
        tem_bottom[j] += attempt_counter[i][j]
plt.ylabel('Number of students')
plt.xticks(ind+width/2., [x for x in range(NUM_QUESTION)])
plt.xlabel('Prompt ID')
plt.gcf().subplots_adjust(right=0.8)
plt.legend(p, (x+1 for x in range(10)), loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('attempt_cnt.png')

########################
### Time information ###
########################
selected_data = data_set.sort_by(lambda x: x['a_time'])
start_time = selected_data[0]['a_time']
end_time = selected_data[-1]['a_time']
tem_lmt = start_time
buckets = []
while tem_lmt < end_time:
    tem_lmt += datetime.timedelta(0, 3600)
    buckets.append(tem_lmt)

time_info_counter = [[0 for j in range(len(buckets)+1)] for i in range(NUM_QUESTION)]
for prompt in range(NUM_QUESTION):
    tem_data = data_set.filter_by(lambda x: x['specifier']==prompt)
    for item in tem_data.map(lambda x: x['a_time']):
        for index in range(len(buckets)):
            if item < buckets[index]:
                break
        if index==len(buckets)+1 and item>buckets[idnex]:
            index += 1
        time_info_counter[prompt][index] += 1

# Print it out
plot_data = [np.array([0]*(len(buckets)+1))]
for item in time_info_counter:
    plot_data.append(plot_data[-1]+np.array(item))
x_ax = np.arange(len(buckets)+1)
fig, ax = toolkit.prepare_plot(gridWidth=0.5, figsize=(10.5, 8))
c_patches = []
for i in range(NUM_QUESTION):
    plt.fill_between(x_ax, plot_data[i+1], plot_data[i], facecolor=plt.cm.rainbow_r(0.1*i), label='Prompt {}'.format(i))
    c_patches.append(mpatches.Patch(color=plt.cm.rainbow_r(0.1*i), label=data.name_map[i]))
# plt.legend(handles=c_patches)
plt.legend()
plt.xticks(x_ax[1::2], [(time-datetime.timedelta(0, 4200)).strftime('%m-%d %H:%M') for time in buckets[0::2]], rotation='40', ha='right')
plt.xlabel("Timestamp (mm-dd hh:mm)")
plt.ylabel("Number of submissions")
plt.savefig('time_info.png')

#########################################################
### Most common wrong answers and first wrong answers ###
#########################################################
wrong_answers_counter = [[] for i in range(NUM_QUESTION)]
first_answers_counter = [[] for i in range(NUM_QUESTION)]
tem_data_set = data_set.filter_by(lambda x: not x['result'])
for prompt in range(NUM_QUESTION):
    selected_data = tem_data_set.filter_by(lambda x: x['specifier']==prompt)
    selected_data = selected_data.group_by(lambda x: x['answer']).map(lambda x: (x[0], len(x[1])))
    selected_data = selected_data.sort_by(lambda x: -x[1])
    if selected_data.count() > 10:
        wrong_answers_counter[prompt] = selected_data[:10]
    else:
        wrong_answers_counter[prompt] = selected_data

    selected_data = tem_data_set.sort_by(lambda x: x['a_time']).group_by(lambda x: x['student']).map(lambda x: x[1][0])
    selected_data = selected_data.group_by(lambda x: x['answer']).map(lambda x: (x[0], len(x[1])))
    selected_data = selected_data.sort_by(lambda x: -x[1])
    if selected_data.count() > 10:
        first_answers_counter[prompt] = selected_data[:10]
    else:
        first_answers_counter[prompt] = selected_data

#################################
### Response time information ###
#################################
RESPONSE_BUCKETS = [60, 120, 300, 600]
response_time_counter = [[0 for i in range(len(RESPONSE_BUCKETS)+1)] for j in range(NUM_QUESTION)]
for prompt in range(NUM_QUESTION):
    selected_data = data_set.filter_by(lambda x: x['specifier']==prompt)
    selected_data = selected_data.sort_by(lambda x: x['a_time']).group_by(lambda x: x['student'])
    selected_data = selected_data.map(lambda x: toolkit.get_time_information(x[1]).total_seconds())
    for item in selected_data:
        for index in range(len(RESPONSE_BUCKETS)):
            if item < RESPONSE_BUCKETS[index]:
                break
        if index == 3 and item > RESPONSE_BUCKETS[3]:
            index = 4
        response_time_counter[prompt][index] += 1
    ind = np.arange(len(RESPONSE_BUCKETS)+1)
    width = 1
    fig, ax = toolkit.prepare_plot(gridWidth=0)
    rects = plt.bar(ind, response_time_counter[prompt], width, color='gray', edgecolor='gray')
    plt.ylabel('#Students')
    plt.xlabel('Time point (min)')
    plt.ylim([0, 180])
    plt.xticks([loc+width for loc in ind[:len(ind)-1]], [t/60 for t in RESPONSE_BUCKETS])
    toolkit.autolabel(rects, ax)
    plt.savefig('response_time_{}'.format(prompt))
