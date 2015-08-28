import re
import datetime

class DataReader(object):
    def __init__(self, data_base_directory, lab):
        self.DATA_FILE_PATH = data_base_directory + '/{}.dat'.format(lab)
        self.MAP_FILE_PATH = data_base_directory + '/{}_caseId_str2numId.map'.format(lab)
        self.data_set = []
        self.sub_map = {}
        self.name_map = {}

        self._sort_map()
        with open(self.DATA_FILE_PATH, 'r') as f_in:
            for line in f_in:
                self.data_set.append(self._parse(line[:-1]))

    def _sort_map(self):
        '''
        Read the map file. Make specifiers ordered and give a map between question name and specifier.

        Input: Map file
        '''
        map_items = []
        with open(self.MAP_FILE_PATH, 'r') as f_in:
            for line in f_in:
                tem_result = line[:len(line)-2].split('\t')
                n_suite = tem_result[1].split(" > ")[1]
                n_suite = re.sub(r'Suite ', "", n_suite)

                n_case = tem_result[1].split(" > ")[2]
                n_case = re.sub(r'Case ', "", n_case)

                n_prompt = tem_result[1].split(" > ")[3]
                n_prompt = re.sub(r'Prompt ', "", n_prompt)
                n_prompt = n_prompt[1:]
                if len(n_prompt) < 2:
                    n_prompt = '0' + n_prompt

                map_items.append((int(tem_result[0]), n_suite, n_case, n_prompt))

        map_items = sorted(map_items, key=lambda x: x[3])
        map_items = sorted(map_items, key=lambda x: x[2])
        map_items = sorted(map_items, key=lambda x: x[1])

        for i in range(len(map_items)):
            self.sub_map[map_items[i][0]] = i
            self.name_map[i] = 'Suite ' + str(map_items[i][1]) + ' > Case '+ str(map_items[i][2]) + ' > Prompt ' + str(map_items[i][3])

    def _parse(self, data):
        '''
            Parse raw input data

            Input: A string of one log item

            Output: Parsed data
        '''
        parsed_data = data.split('\t')
        return {'q_time': datetime.datetime.fromtimestamp(int(parsed_data[0])),
                'a_time': datetime.datetime.fromtimestamp(int(parsed_data[1])),
                'specifier': self.sub_map[int(parsed_data[2])],
                'c_specifier': int(parsed_data[3]),
                'student': parsed_data[4],
                'result': parsed_data[5] == 'True',
                'answer': parsed_data[6]}

def SetupData(data_base_directory, lab):
    '''
        Get data set and case id map.

        Input: Base directory of the data file and lab

        Output: An object containing the data set and maps
    '''
    return DataReader(data_base_directory, lab)
