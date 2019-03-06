from pymel.core import *
import sys


def transform_nodes_only(list_in, with_exit=False):
	'''
	Verifies that all items are transform nodes

	list_in <type 'list'>: List of selected nodes
	with_exit <type 'bool'>: Stop program if at least one item is invalid type

	Return <type 'list'>: List of transform nodes
	'''

	list_out = []
	valid_type = ['mesh', 'transform']

	for i, list_item in enumerate(list_in):

		if nodeType(list_in[i]) == valid_type[0]:
			list_out.append(list_in[i].getParent())

		elif nodeType(list_in[i]) == valid_type[1]:
			list_out.append(list_in[i])

		elif with_exit:
			sys.exit()

	return list_out


def matrix_to_list(matrix_in):
	'''
	Converts matrix attribute value to flat one level list of float values

	matrix_in <class '... .Matrix'>: Matrix attribute value

	Return <type 'list'>: List of 16 float values
	'''

	list_out = []

	for array_type in matrix_in:
		for i in array_type:

			list_out.append(i)

	return list_out
