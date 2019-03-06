# from ms_script import locators_to_pivots
# reload(locators_to_pivots)
# locators_to_pivots.main()

from pymel.core import *
from ms_core.get_root_parent import *


def main():
	''' Create locator objects at positions of all visible objects '''

	# get transformation nodes
	roots = []
	for i in ls(type='mesh'):
		root = get_root_parent(i)
		if root not in roots:
			roots.append(root)

	for i in roots:

		# for all visible object get pivot attribute
		root_vis = getAttr('{}.visibility'.format(i))
		if root_vis:
			root_pos = getAttr('{}.scalePivot'.format(i))

			# create new locator object in the XY-plane
			root_pos[2] = 0.0
			new_locataor = spaceLocator(
				name='loc_{}'.format(i),
				position=root_pos
			)

			# center pivot and clear history
			new_locataor.centerPivots()
			makeIdentity(new_locataor, apply=True)

			# show me creation
			select(i, new_locataor)
			pause(sec=1)
			refresh()

	select(clear=True)
