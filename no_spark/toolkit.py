import datetime

SESSION_THRESHOLD = datetime.timedelta(0, 30 * 60)

def get_session_info(item_list):
    '''
        Generate session information for a given student

        Input: A ordered list of logs for a student

        Output: Session number

        Raise Exception when unordered item appears
    '''
    if len(item_list) == 0:
        return 0
    tem_max = datetime.datetime.fromtimestamp(0)
    session_cnt = 0
    for item in item_list:
        a_time = item['a_time']
        q_time = item['q_time']
        if q_time > tem_max + SESSION_THRESHOLD:
            tem_max = q_time
            session_cnt += 1
        elif q_time >= tem_max:
            tem_max = q_time
        elif a_time > tem_max:
            raise Exception(item)
    return session_cnt

def get_time_information(item_list):
    '''
        Get time needed to solve the question

        Input: an ordered list of logs of a student

        Output: total time needed to solve the question
    '''
    result = datetime.timedelta(0, 0)
    tem_max = datetime.datetime.fromtimestamp(0)
    for item in item_list:
        a_time = item['a_time']
        q_time = item['q_time']
        if q_time > tem_max + SESSION_THRESHOLD:
            tem_max = q_time
        result += a_time - tem_max
        tem_max = a_time
    return result
