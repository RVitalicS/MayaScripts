def factors_of(array_in):
	'''
	Searches the most usable group types

	array_in <type 'list'>: List with array items

	Return <type 'list'>: List of factors for length of input array
	'''

	# define length of input array
	array_length = len(array_in)

	# define array variable for search result
	factors = []

	# compares with the most frequently used factors
	if array_length % 3 == 0:
		factors.append(3)

		if array_length % 9 == 0:
			factors.append(9)

	if array_length % 4 == 0:
		factors.append(4)

		if array_length % 16 == 0:
			factors.append(16)

	# output
	if factors:
		return factors


def array_into_groups(array_in, length):
	'''
	Divide array into groups

	array_in <type 'list'>: List with array items
	length <type 'int'>: Determines the quantity items in the group

	Return <type 'list'>: List divided into groups
	'''

	# output array
	grouped_array = []

	# loop item to fill output array
	group_buffer = []

	# add filled groups with required length to new array
	for i in array_in:

		if len(group_buffer) < length:
			group_buffer.append(i)
		else:
			grouped_array.append(group_buffer)
			group_buffer = [i]

	grouped_array.append(group_buffer)

	# output
	if len(group_buffer) == length:
		return grouped_array
	else:
		raise Exception(
			'Can not divide this float array with length={} to groups with length={}, factors={}'.format(
				len(array_in),
				length,
				factors_of(array_in)
				)
			)
