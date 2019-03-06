# from ms_shelf import _install_
# # reload(_install_)
# _install_.scripts()

from pymel.core import *
from os.path import dirname, normpath, join, splitext
from os import listdir


# get directory of this file
this_dir = dirname(__file__)


# get shelfLayout to add buttons
custom_layout = "<class 'pymel.core.uitypes.ShelfLayout'>"
for i in lsUI(controlLayouts=True):
	if [i.type(), i.shortName()] == ['shelfLayout', 'Custom']:
		custom_layout = i


# create list of all button scripts in this directory
script_files = []
for i in listdir(this_dir):
	if i[0] != '_' and i[-2:] == 'py':
		script_files.append(splitext(i)[0])


def icon_path(name_in):
	'''
	Return full relative path of input icon name
	depending on directory of this file
	'''

	return normpath(join(dirname(this_dir), 'icons', name_in))


def add_button(options_in):
	'''
	Add button to the shelf if it hasn't been installed yet

	options_in <type 'dict'>: Options for shelfButton command
	'''

	# make sure that button hasn't been installed yet
	has_button = False
	for i in custom_layout.getChildren():
		if i.type() == 'shelfButton':

			if options_in['label'] == i.getLabel():
				has_button = True

	if not has_button:

		# add button
		shelfButton(
			parent=custom_layout,
			image1=icon_path(options_in['image1']),
			label=options_in['label'],
			annotation=options_in['annotation'],
			imageOverlayLabel=options_in['imageOverlayLabel'],
			command=options_in['command'],
			doubleClickCommand=options_in['doubleClickCommand']
			)
	else:
		inViewMessage(
			amg='This button has been added already',
			pos='botCenter',
			fade=True
			)


def scripts():
	'''	Creates UI to add linked with scripts buttons to the 'Custom' shelf '''

	# create list of install options
	install_items = []
	for i in script_files:

		exec("from ms_shelf import {}".format(i))
		exec("# reload({})".format(i))
		exec("install_items.append({}.install_options)".format(i))

	# create UI
	main_window = window(title='Add Shelf Buttons')
	main_layout = columnLayout(adjustableColumn=True)

	# generate buttons to add scripts to shelf
	for i in install_items:

		iconTextButton(
			parent=main_layout,
			style='iconAndTextHorizontal',
			image1=icon_path(i['image1']),
			label=i['label'],
			annotation=i['annotation'],
			command=Callback(add_button, i)
			)

	# run
	showWindow(main_window)
