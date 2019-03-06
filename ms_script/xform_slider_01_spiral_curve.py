# from ms_script import xform_slider_01_spiral_curve
# reload(xform_slider_01_spiral_curve)
# xform_slider_01_spiral_curve.main()

from pymel.core import *
from ms_core.vectors_to_xform import *
from ms_core.point_positions import point_pos_nurbs_curve
from ms_tool import xform_slider
reload(xform_slider)


def main():
	''' Moves selected object along Imported Spiral '''

	if selected():

		# there are two grouped curves with equal quantity of points
		# that twisted into spiral and grow along world Y axis
		pos_01 = point_pos_nurbs_curve(ls('Curve_Transform0')[0])
		pos_02 = point_pos_nurbs_curve(ls('Curve_Transform1')[0])

		# define quantity of points
		index_length = len(pos_01)

		# adjust scale of a transformed object
		scale_multiplier = 1

		# vector array variables for local axes for the first curve
		x_01 = []
		y_01 = []
		z_01 = []

		# vector array variables for local axes for the second curve
		x_02 = []
		y_02 = []
		z_02 = []

		# almost like using Houdini Wrangler node
		for i in range(index_length):

			# X vectors
			x_01_item = pos_01[i] - pos_02[i]
			x_01_item = x_01_item.normal()

			x_02_item = x_01_item * (-1)

			# Y vectors
			if i+1 < index_length:
				y_01_item = pos_01[i] - pos_01[i+1]
				y_02_item = pos_02[i] - pos_02[i+1]
			else:
				y_01_item = pos_01[i-1] - pos_01[i]
				y_02_item = pos_02[i-1] - pos_02[i]

			y_01_item = y_01_item.normal() * (-1)
			y_02_item = y_02_item.normal() * (-1)

			# Z vectors
			z_01_item = x_01_item.cross(y_01_item)
			z_01_item = z_01_item.normal()

			z_02_item = x_02_item.cross(y_02_item)
			z_02_item = z_02_item.normal()

			# correct Y vectors
			y_01_item = z_01_item.cross(x_01_item.normal())
			y_01_item = y_01_item.normal()

			y_02_item = z_02_item.cross(x_02_item.normal())
			y_02_item = y_02_item.normal()

			# write values
			x_01.append(x_01_item*scale_multiplier)
			y_01.append(y_01_item*scale_multiplier)
			z_01.append(z_01_item*scale_multiplier)

			x_02.append(x_02_item*scale_multiplier)
			y_02.append(y_02_item*scale_multiplier)
			z_02.append(z_02_item*scale_multiplier)

		# get matrices from vectors
		xform_01 = vectors_to_xform(x_01, y_01, z_01, pos_01)
		xform_02 = vectors_to_xform(x_02, y_02, z_02, pos_02)

		# show slider and apply transformations to it
		xform_slider.show_slider(selected()[0], xform_01 + xform_02)
