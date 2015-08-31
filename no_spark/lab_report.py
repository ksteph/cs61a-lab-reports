import sys
import numpy as np

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
