# from ms_script import dna_bend
# reload(dna_bend)
# dna_bend.main()

from pymel.core import *


# xform for a mesh object
mesh_xform = [
	53.16349530376159, 0.0, 90.42685132261258, 0.0,
	-0.0, 104.8969621725766, 0.0, 0.0,
	-90.42685132261258, -0.0, 53.16349530376159, 0.0,
	-0.9395439633873868, -7.965, 3.147358554409238, 1.0
	]

# xform for a bend deformer
bend_xform = [
	46.31382283267719, 0.0, -26.60502165060984, 0.0,
	0.0, 53.41158453375101, 0.0, 0.0,
	26.60502165060984, 0.0, 46.31382283267719, 0.0,
	-2.3357428897608914, 44.99141056294097, 0.8863150285011283, 1.0
	]

# xform for a whole group
group_xform = [
	1.0, 0.0, 0.0, 0.0,
	0.0, 1.0, 0.0, 0.0,
	0.0, 0.0, 1.0, 0.0,
	-3.8272055275369325, -3.3795101947948325, 2.373558929671759, 1.0
	]


def main():
	''' Apply right transformations and deformations to newly imported object '''

	if selected():

		# Apply transformation to imported object
		imported_object = selected()[0]
		xform(imported_object, matrix=mesh_xform)

		# Apply transformation to bend object and set curvature attribute
		new_bend = nonLinear(imported_object, type='bend')
		setAttr('{}.curvature'.format(new_bend[0]), -71.047)
		xform(new_bend, matrix=bend_xform)

		# Group all together and apply another transformation
		new_group = group(
			imported_object,
			new_bend[1],
			name='{}_bended'.format(imported_object)
			)
		xform(new_group, matrix=group_xform)
