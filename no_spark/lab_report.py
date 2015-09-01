import sys
import numpy as np
import datetime

import data_reader
import toolkit

def usage_information():
    info = 'Lab report generator for CS61a\n'
    info += 'Usage: lab_report.py <data_file_directory> <lab_name>'
    return info

if len(sys.argv) < 3:
    print usage_information()

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
session_counter = [0] * 6
tem_data = data_set.sort_by(lambda x: x['a_time']).group_by(lambda x: x['student'])
for item in tem_data:
    # WARNING: This may throw an exception!
    session_cnt = toolkit.get_session_info(item[1])
    if session_cnt > 5:
        session_counter[5] += 1
    else:
        session_counter[session_cnt] += 1

########################################
### Number of submissions per prompt ###
########################################
submission_counter = [0] * NUM_QUESTION
for prompt in range(NUM_QUESTION):
    submission_counter[prompt] = data_set.filter_by(lambda x: x['specifier']==prompt).count()

#################################################
### Number of unique wrong answers per prompt ###
#################################################
unique_answer_counter = [0] * NUM_QUESTION
for prompt in range(NUM_QUESTION):
    unique_answer_counter[prompt] = data_set.filter_by(lambda x: x['specifier']==prompt and not x['result']).get_element_count('answer')

#####################################
### Number of attempts per prompt ###
#####################################
attempt_counter = [[0 for i in xrange(10)] for j in xrange(NUM_QUESTION)]
for prompt in range(NUM_QUESTION):
    tem_data = data_set.filter_by(lambda x: x['specifier']==prompt)
    tem_data = tem_data.group_by(lambda x: x['student']).map(lambda x: len(x[1]))
    for item in tem_data:
        attempt_counter[prompt][np.min([item-1, 9])] += 1


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

time_info_counter = [[0 for j in range(len(buckets))] for i in range(NUM_QUESTION)]
for prompt in range(NUM_QUESTION):
    tem_data = data_set.filter_by(lambda x: x['specifier']==prompt)
    for item in tem_data.map(lambda x: x['a_time']):
        for index in range(len(buckets)):
            if item < buckets[index]:
                break
        time_info_counter[prompt][index] += 1

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
print response_time_counter
