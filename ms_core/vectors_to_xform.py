def vectors_to_xform(x_in, y_in, z_in, pos_in):
	'''
	Creates array of xform values from input vectors

	x_in   <class '... .Vector'>: vector array for X axis
	y_in   <class '... .Vector'>: vector array for Y axis
	z_in   <class '... .Vector'>: vector array for Z axis
	pos_in <class '... .Vector'>: array of position coordinates

	Return <type 'list'>: Array of grouped floats values
	'''

	# defines length of the output array
	indexes = len(pos_in)

	# add output array variable and default matrix item variable
	xform_out = []
	xform_default = [
		1.0, 0.0, 0.0, 0.0,
		0.0, 1.0, 0.0, 0.0,
		0.0, 0.0, 1.0, 0.0,
		0.0, 0.0, 0.0, 1.0
		]

	# filling the output array variable
	for i in range(indexes):

		# copy default matrix
		xform_item = xform_default[:]

		# X vector
		x_item = x_in[i]
		xform_item[0] = x_item[0]
		xform_item[1] = x_item[1]
		xform_item[2] = x_item[2]

		# Y vector
		y_item = y_in[i]
		xform_item[4] = y_item[0]
		xform_item[5] = y_item[1]
		xform_item[6] = y_item[2]

		# Z vector
		z_item = z_in[i]
		xform_item[8] = z_item[0]
		xform_item[9] = z_item[1]
		xform_item[10] = z_item[2]

		# Position
		pos_item = pos_in[i]
		xform_item[12] = pos_item[0]
		xform_item[13] = pos_item[1]
		xform_item[14] = pos_item[2]

		# add matrix item to the output array
		xform_out.append(xform_item)

	return xform_out
