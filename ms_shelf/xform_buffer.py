# store transformations of selected object as matrix (xform attribute) until you clean it by yourself
# after that you may apply those transformations (translate, rotate, scale) to another object

from pymel.core import *
from os.path import join, normpath, exists
from os import remove
from ms_core.get_root_parent import *
from ms_core import json_manager
import json, sys
import tempfile


# create path to store json file
path_json = normpath(join(tempfile.gettempdir(), 'xform_buffer.json'))


def clear_data():
	''' Delete json file '''

	if exists(path_json):
		remove(path_json)

		inViewMessage(
			amg='now data is forgotten',
			pos='botCenter',
			fade=True
		)


def main(top_xform=False):
	'''
	Store transformations of selected object,
	after that apply those transformations to another object

	top_xform <type 'bool'>: If 'True' then get transformations from top parent of a selected object
	'''

	if not selected():
		sys.exit()

	# may get top parent of a selected object
	if top_xform:
		testee = get_root_parent(selected()[0])
	else:
		testee = selected()[0]

	# if transformations were saved then apply it
	data = json_manager.read(path_json)
	if data:

		# convert data to 16 float values and applies it
		data_floats = []
		for i in data:
			for x in i:
				data_floats.append(x)
		xform(testee, matrix=data_floats)

		inViewMessage(
			amg='xform have been applied and still are in memory',
			pos='botCenter',
			fade=True
			)

	# if no transformations were saved then save it
	else:
		xform_data = list(ls('{}.xformMatrix'.format(testee))[0].get())

		for num, i in enumerate(xform_data):
			xform_data[num] = list(i)

		if json_manager.write(path_json, xform_data):
			inViewMessage(
				amg='xform have been saved in memory',
				pos='botCenter',
				fade=True
				)


# these options are for _install_.py module

shelf_command = '''
from ms_shelf import xform_buffer
# reload(xform_buffer)
xform_buffer.main()
'''

double_command = '''
from ms_shelf import xform_buffer
# reload(xform_buffer)
xform_buffer.clear_data()
'''

install_options = dict(
	image1='xform_buffer.png',
	label='xform buffer',
	annotation='Store transformations of selected object, after that you may apply those transformations to another object',
	imageOverlayLabel='',
	command=shelf_command,
	doubleClickCommand=double_command
	)
