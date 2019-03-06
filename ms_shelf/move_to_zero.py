# move selected nodes to zero coordinates

from pymel.core import *
from ms_core.type_control import *


def main(y_only=False):
	'''
	Moves selected objects to zero coordinates

	y_only <type 'bool'>: if 'True' uses only Y axis
	'''

	if selected():

		# get from selection transformation nodes only
		selected_nodes = transform_nodes_only(selected())
		for selected_transform in selected_nodes:

			# get values for translate attribute
			move_vector = [
				-ls('{}.rotatePivot{}'.format(selected_transform, i))[0].get() for i in ['X', 'Y', 'Z']
				]

			# apply translation depending on input flag
			if not y_only:
				selected_transform.translate.set(move_vector)
			else:
				selected_transform.translateY.set(move_vector[1])

	else:
		inViewMessage(
			amg='Nothing selected',
			pos='botCenter',
			fade=True
			)


# these options are for _install_.py module

shelf_command = '''
from ms_shelf import move_to_zero
# reload(move_to_zero)
move_to_zero.main()
'''

double_command = '''
from ms_shelf import move_to_zero
# reload(move_to_zero)
move_to_zero.main(y_only=True)
'''

install_options = dict(
	image1='move_to_zero.png',
	label='Move to Zero',
	annotation='Move selected nodes to zero coordinates',
	imageOverlayLabel='',
	command=shelf_command,
	doubleClickCommand=double_command
	)
