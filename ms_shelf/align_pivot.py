# creates window to align pivot in local coordinates by bounding box of transform node

from pymel.core import *
from ms_core.type_control import *
from os.path import dirname, normpath, join


# define variables that will store radio button groups of UI
# to use them in another function
radio_01 = "<class 'pymel.core.uitypes.ColumnLayout'>"
radio_02 = "<class 'pymel.core.uitypes.ColumnLayout'>"
radio_03 = "<class 'pymel.core.uitypes.ColumnLayout'>"


def assign_pivot( transform_in, xAxis=None, yAxis=None, zAxis=None ):
	'''
	Sets value for chosen pivot axis

	transform_in <class '... .Transform'>: Selected transform node
	xAxis <type 'bool'>: If 'True' sets value for X axis
	yAxis <type 'bool'>: If 'True' sets value for Y axis
	zAxis <type 'bool'>: If 'True' sets value for Z axis
	'''

	# set X axis
	if isinstance(xAxis, float):
		transform_in.scalePivotX.set(xAxis)
		transform_in.rotatePivotX.set(xAxis)

	# set Y axis
	if isinstance(yAxis, float):
		transform_in.scalePivotY.set(yAxis)
		transform_in.rotatePivotY.set(yAxis)

	# set Z axis
	if isinstance(zAxis, float):
		transform_in.scalePivotZ.set(zAxis)
		transform_in.rotatePivotZ.set(zAxis)


def align_to( maxX=False, minX=False, maxY=False, minY=False, maxZ=False, minZ=False ):
	'''
	Align pivot for each selected object to chosen axis

	maxX <type 'bool'>: If 'True' aligns to maximum value for X axis of BoundingBox
	minX <type 'bool'>: If 'True' aligns to minimum value for X axis of BoundingBox
	maxY <type 'bool'>: If 'True' aligns to maximum value for Y axis of BoundingBox
	minY <type 'bool'>: If 'True' aligns to minimum value for Y axis of BoundingBox
	maxZ <type 'bool'>: If 'True' aligns to maximum value for Z axis of BoundingBox
	minZ <type 'bool'>: If 'True' aligns to minimum value for Z axis of BoundingBox
	'''

	# make sure that all selected nodes are transfrom nodes
	selected_nodes = transform_nodes_only(selected())

	for selected_transform in selected_nodes:

		# get xform from current transform nodepass
		xform_original = getAttr('{}.xformMatrix'.format(selected_transform))

		# set transformations to default values
		xform_default = [
			1.0, 0.0, 0.0, 0.0,
			0.0, 1.0, 0.0, 0.0,
			0.0, 0.0, 1.0, 0.0,
			0.0, 0.0, 0.0, 1.0
			]

		xform(selected_transform, matrix=xform_default)

		# get point values of a bounding box
		box_min = selected_transform.boundingBoxMin.get()
		box_max = selected_transform.boundingBoxMax.get()

		# move pivot along X axis and reselect button
		valXmax = box_max[0]
		valXmin = box_min[0]

		if maxX and not minX:
			assign_pivot(selected_transform, xAxis=valXmax)
			radioButton(radio_01.getChildArray()[0], edit=True, select=True)
		elif minX and not maxX:
			assign_pivot(selected_transform, xAxis=valXmin)
			radioButton(radio_01.getChildArray()[2], edit=True, select=True)
		elif minX and maxX:
			valX = valXmin + (valXmax - valXmin)/2
			assign_pivot(selected_transform, xAxis=valX)
			radioButton(radio_01.getChildArray()[1], edit=True, select=True)

		# move pivot along Y axis and reselect button
		valYmax = box_max[1]
		valYmin = box_min[1]

		if maxY and not minY:
			assign_pivot(selected_transform, yAxis=valYmax)
			radioButton(radio_02.getChildArray()[0], edit=True, select=True)
		elif minY and not maxY:
			assign_pivot(selected_transform, yAxis=valYmin)
			radioButton(radio_02.getChildArray()[2], edit=True, select=True)
		elif minY and maxY:
			valY = valYmin + (valYmax - valYmin)/2
			assign_pivot(selected_transform, yAxis=valY)
			radioButton(radio_02.getChildArray()[1], edit=True, select=True)

		# move pivot along Z axis and reselect button
		valZmax = box_max[2]
		valZmin = box_min[2]

		if maxZ and not minZ:
			assign_pivot(selected_transform, zAxis=valZmax)
			radioButton(radio_03.getChildArray()[0], edit=True, select=True)
		elif minZ and not maxZ:
			assign_pivot(selected_transform, zAxis=valZmin)
			radioButton(radio_03.getChildArray()[2], edit=True, select=True)
		elif minZ and maxZ:
			valZ = valZmin + (valZmax - valZmin)/2
			assign_pivot(selected_transform, zAxis=valZ)
			radioButton(radio_03.getChildArray()[1], edit=True, select=True)

		# apply original transformations back
		xform(selected_transform, matrix=matrix_to_list(xform_original))


def main():
	'''
	Creates window with 'radioButtons' to align pivots of selected objects
	'''

	if selected():

		# create UI
		main_window = window(title='Align Pivot', sizeable=False, widthHeight=(150, 150))

		main_layout = formLayout(numberOfDivisions=100)

		this_dir = dirname(__file__)

		# add labels to axes
		text_layout = rowLayout(
			numberOfColumns=3,
			columnAttach=[
				(1, 'right', 13),
				(2, 'right', 13),
				]
			)
		text(parent=text_layout, h=25, w=15, label='X', font='boldLabelFont')
		text(parent=text_layout, h=25, w=15, label='Y', font='boldLabelFont')
		text(parent=text_layout, h=25, w=15, label='Z', font='boldLabelFont')
		setParent(main_layout)

		# add buttons to manage all axes
		buttons_layout = columnLayout(rowSpacing=11)
		iconTextButton(
			parent=buttons_layout,
			h=19, w=40,
			style='textOnly',
			label='max',
			command=Callback(align_to, maxX=True, maxY=True, maxZ=True)
			)

		iconTextButton(
			parent=buttons_layout,
			h=19, w=40,
			style='textOnly',
			label='min',
			command=Callback(align_to, maxX=True, minX=True, maxY=True, minY=True, maxZ=True, minZ=True)
			)

		iconTextButton(
			parent=buttons_layout,
			h=19, w=40,
			style='textOnly',
			label='mid',
			command=Callback(align_to, minX=True, minY=True, minZ=True)
			)

		setParent(main_layout)

		# space controllers
		cSpace  = 15
		cOffset = 5
		rSpace  = 17

		# make radio button groups visible to global scope
		global radio_01
		global radio_02
		global radio_03

		# add radio buttons for X axis
		radio_01 = columnLayout(rowSpacing=rSpace)
		radioCollection()
		radioButton(label='', onCommand=Callback(align_to, maxX=True))
		radioButton(label='', onCommand=Callback(align_to, minX=True, maxX=True))
		radioButton(label='', onCommand=Callback(align_to, minX=True))
		setParent(radio_01)
		setParent(main_layout)

		# add radio buttons for Y axis
		radio_02 = columnLayout(rowSpacing=rSpace)
		radioCollection()
		radioButton(label='', onCommand=Callback(align_to, maxY=True))
		radioButton(label='', onCommand=Callback(align_to, minY=True, maxY=True))
		radioButton(label='', onCommand=Callback(align_to, minY=True))
		setParent(radio_02)
		setParent(main_layout)

		# add radio buttons for Z axis
		radio_03 = columnLayout(rowSpacing=rSpace)
		radioCollection()
		radioButton(label='', onCommand=Callback(align_to, maxZ=True))
		radioButton(label='', onCommand=Callback(align_to, minZ=True, maxZ=True))
		radioButton(label='', onCommand=Callback(align_to, minZ=True))
		setParent(radio_03)
		setParent(main_layout)

		# adjust main layout
		formLayout(
			main_layout,
			edit=True,
			attachForm=[
				(text_layout, 'left', 40),
				(text_layout, 'top', 15)
				],
			attachControl=[
				(buttons_layout, 'top', 0, text_layout),
				(radio_01, 'top', cOffset, text_layout),
				(radio_01, 'left', 0, buttons_layout),
				(radio_02, 'top', cOffset, text_layout),
				(radio_02, 'left', cSpace, radio_01),
				(radio_03, 'top', cOffset, text_layout),
				(radio_03, 'left', cSpace, radio_02)
				]
			)

		showWindow(main_window)

	else:
		inViewMessage(
			amg='Nothing selected',
			pos='botCenter',
			fade=True
			)


# these options are for _install_.py module

shelf_command = '''
from ms_shelf import align_pivot
# reload(align_pivot)
align_pivot.main()
'''

double_command = '''
from pymel.core import *

if selected():
	for i in selected():
		i.centerPivots()
'''

install_options = dict(
	image1='align_pivot.png',
	label='Align Pivot',
	annotation='Creates window to align pivot by bounding box of transform node in local coordinates',
	imageOverlayLabel='',
	command=shelf_command,
	doubleClickCommand=double_command
	)
