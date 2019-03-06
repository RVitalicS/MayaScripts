def get_root_parent(node_in):
	'''
	Gets a root parent node of hierarchy

	node_in <class '... .Transform'>: Child node
	Return  <class '... .Transform'>: Root parent node
	'''

	node_parent = node_in.getParent()

	if node_parent:
		return get_root_parent(node_parent)
	else:
		return node_in
