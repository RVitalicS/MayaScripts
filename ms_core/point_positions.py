from pymel.core import *


def point_pos_nurbs_curve(nurbs_in):
	'''
	Gets point positions of chosen NurbsCurve
	and convert those to vector type

	nurbs_in <class '... .NurbsCurve'>: NurbsCurve node

	Return <type 'list'>: List of point position values as <class '... .Vector'>
	'''

	pt_position = [datatypes.Vector(i) for i in nurbs_in.getCVs()]
	return pt_position
