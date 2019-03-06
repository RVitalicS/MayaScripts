# apply transformations from xform attribute array
# to the first selected object through a slider widget

from pymel.core import *
from ms_core.array_into_groups import *
from ms_core import json_manager
from os.path import join, normpath, exists
import tempfile


# create path to store json file
path_json = normpath(join(tempfile.gettempdir(), 'xform_slider.json'))

# necessary global variables
xform_array = []
transform_node = None
index = 0

# create UI
main_window = window(title='xform slider')
columnLayout()
slider_value = intSliderGrp(
	field=True,
	label='Index',
	width=1000
	)


def xform_apply():
	''' Apply transformations from xform attribute array '''

	global index

	# get index value from slider widget
	index = intSliderGrp(slider_value, q=True, v=True)

	# apply transformation
	xform(
		transform_node,
		matrix=xform_array[index]
		)


def index_to_json():
	''' Write index to temp file '''
	json_manager.write(path_json, [index])


def index_from_json():
	''' Read index from temp file '''

	# load index if it was saved
	if exists(path_json):
		data = json_manager.read(path_json)
		return data[0]

	# default index if it wasn't saved
	else:
		return index


def show_slider(node_in, array_in, step=1, save_index=False, run_offset=0, subslider=0, grouped=True):
	'''
	If necessary changes an input array to required type,
	adjust slider widget and finally shows the main window

	node_in <class '... .Transform'>: Object that will be transformed
	array_in <type 'list'>: Matrix array

	step <type 'int'>: Use every other element after the first
	save_index <type 'bool'>: If True, then will save index of last xform item
	run_offset <type 'int'>: Offset xform index at run
	subslider <type 'int'>: Offset first xform index

	grouped <type 'bool'>: If False, then groups values of input array into packs of 16
	'''

	global xform_array
	global transform_node

	# adjust window option to save index on close
	if save_index:
		window(
			main_window,
			edit=True,
			closeCommand=Callback(index_to_json)
			)

	# main condition
	if node_in:

		# transmit input object to the global scope
		transform_node = node_in

		# convert one-level array to two-level array
		# with group of 16
		if not grouped:
			xform_array = array_into_groups(array_in, 16)
		else:
			xform_array = array_in

		# define start index
		xform_array = xform_array[subslider:]

		# define slider step
		xform_array = xform_array[::step]

		# adjust slider options depends on input array
		max_value = len(xform_array) - 1

		intSliderGrp(
			slider_value,
			edit=True,
			minValue=0,
			maxValue=max_value,
			fieldMinValue=0,
			fieldMaxValue=max_value,
			value=0 + run_offset,
			dragCommand=Callback(xform_apply),
			changeCommand=Callback(xform_apply)
			)

		# adjust slider option to load index from previous run
		if save_index:
			intSliderGrp(
				slider_value,
				edit=True,
				value=index_from_json() + run_offset
				)

			# apply previous transformations
			xform_apply()

		# run
		showWindow(main_window)
