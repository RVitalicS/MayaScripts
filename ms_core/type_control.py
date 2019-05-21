from pymel.core import *
import sys


def transform_nodes_only(list_input, with_exit=False):

	''' Verifies that all items are transform nodes

	:param list_input:  <type 'list'>   List of selected nodes
	:param with_exit:   <type 'bool'>   Stop program if at least one item is invalid type

	:return:            <type 'list'>   List of transform nodes '''


	list_out = []
	valid_type = ['mesh', 'transform']

	for i, list_item in enumerate(list_input):

		if nodeType(list_input[i]) == valid_type[0]:
			list_out.append(list_input[i].getParent())

		elif nodeType(list_input[i]) == valid_type[1]:
			list_out.append(list_input[i])

		elif with_exit:
			sys.exit()

	return list_out



def uniform_selection(list_input, item_type):

	''' Verifies that all items are the same type

	:param list_input:  <type 'list'>       List of selected nodes
	:param item_type:   <type 'string'>     Name of target type

	:return:            <type 'bool'>       Condition result '''


	for i in list_input:

		if i.type() == item_type:
			continue
		else:
			return False

	return True



def matrix_to_list(matrix_in):

	''' Converts matrix attribute value to flat one level list of float values

	:param matrix_in:   <class '... .Matrix'>   Matrix attribute value
	:return:            <type 'list'>           List of 16 float values '''


	list_out = []

	for array_type in matrix_in:
		for i in array_type:

			list_out.append(i)

	return list_out
