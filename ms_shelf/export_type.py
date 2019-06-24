# creates dockable Maya window for managing hierarchy item types

from PySide2 import QtWidgets, QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from pymel.core import *

from ms_core import type_control




class DockableWindow(MayaQWidgetDockableMixin, QtWidgets.QWidget):

    ''' Creates dockable Maya window for managing hierarchy item types '''


    def __init__(self):
        super(DockableWindow, self).__init__()


        # attach method for updating interface to SelectionChanged event
        self.selection_event = scriptJob(event=['SelectionChanged', self.update_interface])


        # create variable that will store type value
        self.attribute_name = "nodeSchema"

        # collect possible type values
        self.attribute_values = [
            ["polymesh",
            "subdmesh",
            "pointcloud"],
            ["group",
            "assembly",
            "component",
            "instance",
            "instance source",
            "instance array",
            "level-of-detail",
            "level-of-detail group"]]


        # create main layout
        self.mainLayout = QtWidgets.QVBoxLayout()


        # create tree widget to represent possible types
        self.type_tree = QtWidgets.QTreeWidget()

        selection_color = "#5d5d5d"
        self.tree_style = '''
            QAbstractItemView  { outline: none }
            QTreeWidget { border: none; font-size: 14px }
            QTreeWidget::branch:selected { background: %s }
            QTreeWidget::item:selected { background: %s }
            ''' % (selection_color, selection_color)
        self.type_tree.setStyleSheet(self.tree_style)

        self.type_tree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.type_tree.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.type_tree.setObjectName('tree')
        self.type_tree.setMinimumSize(QtCore.QSize(160, 160))
        self.type_tree.header().setVisible(False)
        self.type_tree.itemClicked.connect(self.update_type)

        self.build_tree()
        self.mainLayout.addWidget(self.type_tree)


        # adjust main window
        self.setWindowTitle('Type Tags')
        self.setLayout(self.mainLayout)


        # build interface depending on selected objects
        self.update_interface()



    def build_tree(self):

        ''' Fills tree widget to represent possible types '''


        # for each structure item
        for tag in self.attribute_values[0] + self.attribute_values[1]:

            # create new tree item
            item = QtWidgets.QTreeWidgetItem()


            # adjust item name, properties
            item.setText(0, tag)

            item.setFlags(
                QtCore.Qt.ItemIsEnabled |
                QtCore.Qt.ItemIsSelectable)


            # append the child item to the parent item
            self.type_tree.invisibleRootItem().addChild(item)



    def get_tree_items(self, root=None, items=None):

        ''' Creates list of all tree widget items

        :param root:    <class '... .QTreeWidgetItem'>  Parent item to find its children
        :param items:   <type 'list'>                   List of children of chosen parent

        :return:        <type 'list'>                   List of all tree widget items '''


        # define root item and children container for the first recursion level
        if not root:
            root = self.type_tree.invisibleRootItem()

        if not items:
            items = []


        # for each child (if there is any one)
        for index in range(root.childCount()):

            child = root.child(index)
            child_count = child.childCount()


            # add it to container
            items.append(child)

            # if child has children then start recursion with itself
            if child_count > 0:
                items = self.get_tree_items(child, items)


        # share link to the list of tree items
        return items



    def outliner_state(self):

        ''' Check if all selected Maya nodes are the same valid type

        :return: <type 'str'>  Selection information of Maya Outliner tab '''


        # create variable to store selection state
        state = None


        # check if there is selected objects
        selected_objects = selected()
        if selected_objects:

            # if all selected objects are mesh objects
            # update selection state
            if type_control.uniform_selection(selected_objects, "mesh"):
                state = "mesh"

            # if all selected objects are transform objects
            # update selection state
            if type_control.uniform_selection(selected_objects, "transform"):
                state = "transform"


        # share link to selection state
        return state



    def get_attribute_values(self):

        ''' Searches specific attribute in selected geometry objects,
        read value of those attribute and fill output list

        :return: <type 'list'> List of specific attribute values '''


        # create output list
        attribute_values = []


        # fill output list
        for geometry in selected():
            value = ""

            if hasAttr(geometry, self.attribute_name, checkShape=False):
                value = getAttr('{}.{}'.format(geometry.name(), self.attribute_name))

            attribute_values.append(value)


        # share link to output list
        return attribute_values



    def update_interface(self):

        ''' Clears interface to default state when selection in Maya is changed '''


        # deselects all selected items and lost the focus
        self.type_tree.clearSelection()
        self.type_tree.clearFocus()


        # get list of tree widget items
        tree_items = self.get_tree_items()

        # get information of Outliner selection
        selection_state = self.outliner_state()


        # hide all items in tree widget if nothing is selected
        if not selection_state:

            for item in tree_items:
                item.setHidden(True)


        # show possible attribute values for "mesh" nodes
        # and select tree widget item depending on existing attribute
        elif selection_state == "mesh":

            for item in tree_items:
                if item.text(0) in self.attribute_values[0]:
                    item.setHidden(False)
                else:
                    item.setHidden(True)

            self.select_tree_item(selection_state)


        # show possible attribute values for "transform" nodes
        # and select tree widget item depending on existing attribute
        elif selection_state == "transform":

            for item in tree_items:
                if item.text(0) in self.attribute_values[1]:
                    item.setHidden(False)
                else:
                    item.setHidden(True)

            self.select_tree_item(selection_state)



    def select_tree_item(self, selection_type):

        ''' Selects tree widget items depending on existing specific geometry attribute

        :param selection_type: <type 'str'> Type of selected nodes'''


        for attribute_value in self.get_attribute_values():

            tree_item = self.type_tree.findItems(attribute_value, QtCore.Qt.MatchExactly)
            if tree_item:
                tree_item[0].setSelected(True)

            elif selection_type == "mesh":
                self.type_tree.findItems(self.attribute_values[0][0],
                    QtCore.Qt.MatchExactly)[0].setSelected(True)

            elif selection_type == "transform":
                self.type_tree.findItems(self.attribute_values[1][0],
                    QtCore.Qt.MatchExactly)[0].setSelected(True)



    def update_type(self, tree_item):

        ''' Sets chosen new value for specific attribute

        :param tree_item: <type '... .QTreeWidgetItem'> Selected tree item '''


        self.delete_attributes()

        if tree_item.text(0) not in [self.attribute_values[0][0], self.attribute_values[1][0]]:

            for attribute_path in self.add_attributes():
                setAttr(attribute_path, tree_item.text(0))



    def delete_attributes(self):

        ''' Deletes specific attribute in selected geometry objects '''

        for geometry in selected():
            if hasAttr(geometry, self.attribute_name, checkShape=False):
                deleteAttr('{}.{}'.format(geometry, self.attribute_name))



    def add_attributes(self):

        ''' Add attribute for each selected geometry object

        :return: <type 'list'> List of string paths to geometry attributes '''


        # create container for attribute paths
        # collect names of selected geometry objects
        attribute_path_list = []
        selected_objects = [geometry.name() for geometry in selected()]


        # add attribute for each selected geometry object
        for geometry_name in selected_objects:
            select(geometry_name)

            addAttr(longName=self.attribute_name, dataType='string')
            attribute_path_list.append('{}.{}'.format(geometry_name, self.attribute_name))


        # select all collected previously geometry objects
        # share link to the list of attribute paths
        select(selected_objects)
        return attribute_path_list



    def dockCloseEventTriggered(self, *args, **kwargs):

        # detach method for updating interface from SelectionChanged event
        scriptJob(kill=self.selection_event)
        super(DockableWindow, self).dockCloseEventTriggered(*args, **kwargs)




def main():

    dockable_window = DockableWindow()
    dockable_window.show(dockable=True)




# these options are for _install_.py module

shelf_command = '''
from ms_shelf import export_type
# reload(export_type)
export_type.main()
'''

install_options = dict(
    image1='export_type.png',
    label='Type Manager',
    annotation='Run dockable Maya window for managing hierarchy item types',
    imageOverlayLabel='',
    command=shelf_command,
    doubleClickCommand='')
