import os
import json


def right_json(path_in):
	'''
	Make sure that input file is json format

	path_in <type 'str'>: Path to json file

	Return <type 'bool'>: Success of condition
	'''

	if os.path.splitext(path_in)[1] == '.json':
		return True


def read(path_in):
	'''
	Read data from json file

	path_in <type 'str'>: Path to json file

	Return <type 'dict'|'list'>: Data from json file
	'''

	# make sure that input path exists and is a json file
	# if all conditions is valid then get data from file
	if os.path.exists(path_in) and right_json(path_in):

		with open(path_in, 'r') as file_in:
			data = json.load(file_in)

			return data


def write(path_in, data):
	'''
	Write list or dictionary data to json file

	path_in <type 'str'>: Path to json file
	data <type 'dict'|'list'>: Data that will be saved to json file

	Return <type 'bool'>: Success of a record
	'''

	# make sure that input data is valid type
	right_data = False
	if isinstance(data, list) or isinstance(data, dict):
		right_data = True

	# if all conditions is valid then write data to file
	if right_data and right_json(path_in):

		with open(path_in, 'w') as file_in:
			json.dump(data, file_in, indent=4)

			return True
