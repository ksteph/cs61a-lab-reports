import datetime
import matplotlib.pyplot as plt

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

def prepare_plot(figsize=(8.5, 4), hideLabels=False, gridColor='#999999', gridWidth=1.0):
    '''
        Template to generate plot figure
    '''
    plt.close()
    fig, ax = plt.subplots(figsize=figsize, facecolor='white', edgecolor='white')
    ax.set_frame_on(True)
    # ax.lines[0].set_visible(False)
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')
    # ax.get_yaxis().set_visible(False)
    ax.axes.tick_params(labelcolor='black', labelsize='10')
    plt.grid(color=gridColor, linewidth=gridWidth, linestyle='-')
    # plt.gcf().subplots_adjust(bottom=0.5)
    # map(lambda position: ax.spines[position].set_visible(False), ['bottom', 'top', 'left', 'right'])
    return fig, ax

def autolabel(rects, ax, h=2, t="{0}"):
    '''
        Label the bar chart.
    '''
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., height+h, t.format(height),
                ha='center', va='bottom', color="black")
