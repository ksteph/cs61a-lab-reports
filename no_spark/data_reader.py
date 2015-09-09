import re
import datetime
import os

class DataReader(object):
    class DataSet(list):
        def group_by(self, key_function):
            '''
                Similar to the semantics of spark

                Input: key

                Output: An new dataset of grouped data points based on key
            '''
            result = {}
            for item in self:
                key = key_function(item)
                if result.has_key(key):
                    result[key].append(item)
                else:
                    result[key] = [item]
            return DataReader.DataSet([(key, result[key]) for key in result])

        def get_element_count(self, key):
            '''
                Get a count number of distinct values for a given key

                Input: key

                Output: An integer of the number of distinct values. -1 if the key if wrong or data_set.
            '''
            if len(self) == 0:
                return 0
            if not self[0].has_key(key):
                return -1
            tem_value_list  = [item[key] for item in self]
            return len(set(tem_value_list))

        def sort_by(self, sort_func):
            '''
                Sort the dataset by given function

                Input: sorting function

                Output: A new dataset of sorted results
            '''
            return DataReader.DataSet(sorted(self, key=sort_func))

        def count(self):
            '''
                Return the total number of elements in dataset

                Output: interger
            '''
            return len(self)

        def filter_by(self, filter_func):
            '''
                Return a filtered dataset based on filter_func
                Semantics are similar to spark

                Input: filter function

                Output: filtered dataset
            '''
            return DataReader.DataSet(filter(filter_func, self))

        def map(self, map_func):
            '''
                Semantics are similar to spark

                Input: map function

                Output: dataset after applying map function for each item
            '''
            return DataReader.DataSet([map_func(item) for item in self])
        def distinct(self):
            '''
                Return a distinct element set

                Note: The order will be changed
            '''
            return DataReader.DataSet(list(set(self)))

    def __init__(self, data_base_directory, lab):
        self.DATA_FILE_PATH = os.path.join(data_base_directory, '{}.dat'.format(lab))
        self.MAP_FILE_PATH = os.path.join(data_base_directory, '{}_caseId_str2numId.map'.format(lab))
        self.DATA_BASE_DIRECTORY = data_base_directory
        self.LAB = lab
        self.data_set = DataReader.DataSet()
        self.sub_map = {}
        self.name_map = {}

        self._sort_map()
        with open(self.DATA_FILE_PATH, 'r') as f_in:
            for line in f_in:
                parsed = self._parse(line[:-1])
                if parsed:
                    self.data_set.append(parsed)

    def _sort_map(self):
        '''
            Read the map file. Make specifiers ordered and give a map between question name and specifier.

            Input: Map file
        '''
        map_items = []
        if '{}_order.map'.format(self.LAB) in os.listdir(self.DATA_BASE_DIRECTORY):
            print 'Ordered map file is used.'
            with open(os.path.join(self.DATA_BASE_DIRECTORY,'{}_order.map'.format(self.LAB)), 'r') as f_in:
                for index, line in enumerate(f_in):
                    tem_result = line[:-2].split('\t')
                    if index != int(tem_result[0])-1:
                        print 'ERROR::CASE_ID ORDER IS WRONG!'
                    self.sub_map[int(tem_result[1])] = index
                    self.name_map[index] = tem_result[2]
            return

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
        if not self.sub_map.has_key(int(parsed_data[2])):
            return
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
