# add separator to the shelf tab

from pymel.core import *


def main():

	# find shelfLayout for 'Custom' tab
	for layout_item in lsUI(controlLayouts=True):
		if [layout_item.type(), layout_item.shortName()] == ['shelfLayout', 'Custom']:

			# add separator item
			separator(parent=layout_item, horizontal=False)


# these options are for _install_.py module

shelf_command = '''
from ms_shelf import add_separator
# reload(add_separator)
add_separator.main()
'''

install_options = dict(
	image1='add_separator.png',
	label='Add Separator',
	annotation='Adds separator to the shelf tab',
	imageOverlayLabel='',
	command=shelf_command,
	doubleClickCommand=''
	)
