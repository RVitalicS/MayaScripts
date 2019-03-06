# from ms_script import xform_slider_02_middle_curve
# reload(xform_slider_02_middle_curve)
# xform_slider_02_middle_curve.main(selected()[0])

from pymel.core import *
from ms_core.vectors_to_xform import *
from ms_core.point_positions import point_pos_nurbs_curve
from ms_tool import xform_slider
reload(xform_slider)


def main(node_in):
	''' Moves selected object along Imported Spiral '''

	if node_in:

		# there are tree grouped curves with equal quantity of points
		# that twisted into spiral and grow along world Y axis
		pos_01 = point_pos_nurbs_curve(ls('Curve_Transform_02_2')[0])
		pos_02 = point_pos_nurbs_curve(ls('Curve_Transform_02_1')[0])

		# define quantity of points
		index_length = len(pos_01)

		# adjust scale of a transformed object
		scale_multiplier = 0.77

		# vector array variables for local axes for a middle curve
		x_01 = []
		y_01 = []
		z_01 = []

		# almost like using Houdini Wrangler node
		for i in range(index_length):

			# X vectors
			x_01_item = pos_01[i] - pos_02[i]
			x_01_item = x_01_item.normal()

			# Y vectors
			if i+1 < index_length:
				y_01_item = pos_01[i] - pos_01[i+1]
			else:
				y_01_item = pos_01[i-1] - pos_01[i]

			y_01_item = y_01_item.normal() * (-1)

			# Z vectors
			z_01_item = x_01_item.cross(y_01_item)
			z_01_item = z_01_item.normal()

			# correct Y vectors
			y_01_item = z_01_item.cross(x_01_item.normal())
			y_01_item = y_01_item.normal()

			# write values
			x_01.append(x_01_item*scale_multiplier)
			y_01.append(y_01_item*scale_multiplier)
			z_01.append(z_01_item*scale_multiplier)

		# get matrices from vectors
		xform_01 = vectors_to_xform(x_01, y_01, z_01, pos_01)

		# show slider and apply transformations to it
		xform_slider.show_slider(
			node_in,
			xform_01,
			step=6,
			subslider=4,
			run_offset=1,
			save_index=True
			)
