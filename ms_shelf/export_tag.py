# creates dockable Maya window for managing shader tags

from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from pymel.core import *
import os

from ms_core import json_manager
from ms_core import type_control



class DockableWindow(MayaQWidgetDockableMixin, QtWidgets.QWidget):

    ''' Creates dockable Maya window for managing shader tags '''


    def __init__(self):
        super(DockableWindow, self).__init__()


        # attach method for updating interface to SelectionChanged event
        self.selection_event = scriptJob(event=['SelectionChanged', self.update_interface])

        # create variable that will store selected geometry names and its tags
        self.geometry_tags = None


        # collect names of renderman shader parameters
        self.shader_parameters = [
            "diffuseColor",
            "primSpecEdgeColor",
            "primSpecRefractionIndex",
            "primSpecExtinctionCoefficient",
            "primSpecRoughness",
            "normal",
            "bump",
            "displacementScalar",
            "displacementVector"]


        # define name of attribute to export material tag
        self.material_tag = 'materialTag'


        # create main layout
        self.mainLayout = QtWidgets.QHBoxLayout()


        # define colors for selection
        self.color_blue = '#0099ff'
        self.color_red = '#9e0428'



        # create tree widget to represent material library
        self.library_tree = QtWidgets.QTreeWidget()

        self.tree_style_blue = '''
            QAbstractItemView  { outline: none }
            QTreeWidget { border: none }
            QTreeWidget::branch:selected { background: %s }
            QTreeWidget::item:selected { background: %s }
            ''' % (self.color_blue, self.color_blue)

        self.tree_style_red = '''
            QAbstractItemView  { outline: none }
            QTreeWidget { border: none }
            QTreeWidget::branch:selected { background: %s }
            QTreeWidget::item:selected { background: %s }
            ''' % (self.color_red, self.color_red)

        self.library_tree.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.library_tree.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.library_tree.setObjectName('tree')
        self.library_tree.setMinimumSize(QtCore.QSize(150, 0))
        self.library_tree.setMaximumSize(QtCore.QSize(150, 1920))
        self.library_tree.header().setVisible(False)
        self.library_tree.itemClicked.connect(self.update_list)

        self.tree_root = self.library_tree.invisibleRootItem()

        self.build_tree_item('Empty', [], self.tree_root)

        self.RenderManAssetLibrary_path = os.path.join(
            os.environ.get('RMANTREE'),
            'lib', 'RenderManAssetLibrary', 'Materials')

        self.RenderManAssetLibrary = self.get_library(self.RenderManAssetLibrary_path)[0][1]
        self.build_tree(self.tree_root, self.RenderManAssetLibrary)

        self.build_tree_item('Textured', self.shader_parameters, self.tree_root)

        self.library_tree.setItemsExpandable(False)
        self.mainLayout.addWidget(self.library_tree)



        # create disabled list widget for default program state
        self.empty_state = QtWidgets.QListWidget()
        self.empty_state.setEnabled(False)

        self.empty_state.setStyleSheet('''
            QListWidget {
                border: none;
                background: #383838;
            } ''')

        self.mainLayout.addWidget(self.empty_state)



        # create list widget to represent material previews
        self.material_grid = QtWidgets.QListWidget()

        self.grid_style_blue = '''
            QAbstractItemView  { outline: none }
            QListWidget { border: none }
            QListWidget::item:selected { background: %s }
            QListWidget::item { background: #3c3f41 }
            ''' % self.color_blue

        self.grid_style_red = '''
            QAbstractItemView  { outline: none }
            QListWidget { border: none }
            QListWidget::item:selected { background: %s }
            QListWidget::item { background: #3c3f41 }
            ''' % self.color_red

        self.material_grid.itemClicked.connect(self.update_tags)

        self.material_grid.setViewMode(QtWidgets.QListView.IconMode)
        self.material_grid.setIconSize(QtCore.QSize(128, 128))
        self.material_grid.setMovement(QtWidgets.QListView.Static)
        self.material_grid.setGridSize(QtCore.QSize(150, 150))
        self.material_grid.setResizeMode(QtWidgets.QListView.Adjust)
        self.material_grid.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)

        # variable that store chosen material item
        self.selected_material_item = None

        self.mainLayout.addWidget(self.material_grid)



        # create list widget to represent choice of shader parameters
        self.texture_tags = QtWidgets.QListWidget()

        self.texture_tags.setStyleSheet('''
            QAbstractItemView  { outline: none }
            QListWidget::item:selected { background: %s }
            QListWidget { border: none; spacing: 10; }
            ''' % self.color_blue)

        self.texture_tags.itemClicked.connect(self.update_tags)

        # variable that store items for shader parameters choice
        self.shader_parameter_items = []
        for i in self.shader_parameters:
            item = QtWidgets.QListWidgetItem(i, self.texture_tags)
            item.setCheckState(QtCore.Qt.Unchecked)

            self.shader_parameter_items.append(item)

        self.mainLayout.addWidget(self.texture_tags)



        # adjust main window
        self.setWindowTitle('Shader Tags')
        self.mainLayout.setStretch(1, 0)
        self.mainLayout.setSpacing(5)
        self.setLayout(self.mainLayout)


        # build interface depending on selected objects
        self.update_interface()



    def get_library(self, tree_path):

        ''' Creates structure of material library as multidimensional list

        :param tree_path:   <type 'str'>    Directory to material library
        :return:            <type 'list'>   Structured material library to build interface '''


        # define structure base
        materials_tree = [[tree_path, [], []]]


        # for each item in current directory
        for item in os.listdir(materials_tree[0][0]):


            # if item is folder
            if os.path.splitext(item)[1] == '':
                subtree_path = os.path.join(materials_tree[0][0], item)

                # dive inside, get structure and append it to current one
                structure = self.get_library(subtree_path)
                materials_tree[0][1].append(structure[0])


            # if item is special tagged folder
            elif os.path.splitext(item)[1] == '.rma':
                json_path = os.path.join(materials_tree[0][0], item, 'asset.json')
                json_data = json_manager.read(json_path)

                # get label from 'json' file, create path to current item
                # and append those ones to current structure as single item
                user_data = [
                    json_data['RenderManAsset']['label'],
                    os.path.join(materials_tree[0][0], item)]
                materials_tree[0][2].append(user_data)


        # collect result and share link to the structure
        return materials_tree



    def print_library(self, tree, spacer=''):

        ''' Print structure of material library to console

        :param tree:    <type 'list'>   Structured material library as multidimensional list
        :param spacer:  <type 'str'>    Tab symbols that represent levels of structure '''


        for subtree in tree:
            print('{}{}'.format(spacer, os.path.basename(subtree[0])))

            for x in subtree[2]:
                print('{}* {}'.format(spacer, os.path.splitext(x[0])[0]))

            print('\n')

            spacer_level = '\t' + spacer
            self.print_library(subtree[1], spacer_level)



    def build_tree(self, root, library):

        ''' Fills tree widget to represent material library

        :param root:    <class '... .QTreeWidgetItem'>  Parent item to append new children
        :param library: <type 'list'>                   Structured material library '''


        # for each structure item (if there is any one)
        for structure in library:

            # create child item from current structure item
            self.build_tree(
                self.build_tree_item(                   # use created child as root
                    os.path.basename(structure[0]),     # get name from structure
                    structure[2],                       # get data to store
                    root),
                structure[1])                           # use stored structure for recursion



    def build_tree_item(self, name, data, root):

        ''' Creates named child item in tree widget with stored data

        :param name: <type 'str'>                   Name of new child item
        :param data: <type 'list'>                  Data That will be stored in created item
        :param root: <class '... .QTreeWidgetItem'> Parent item to create new child

        :return:     <class '... .QTreeWidgetItem'> New child item '''


        # create new tree item
        item = QtWidgets.QTreeWidgetItem()


        # adjust item name, properties and stored data
        item.setText(0, name)

        item.setFlags(
            QtCore.Qt.ItemIsEnabled |
            QtCore.Qt.ItemIsSelectable)

        item.setData(0, QtCore.Qt.UserRole, data)


        # append the child item to the parent item
        root.addChild(item)

        # set child expanded by default
        self.library_tree.expandItem(item)


        # share link to the new child item
        return item



    def find_tree_item(self, material_name):

        ''' Finds item of "library_tree" with requested name of material

        :param material_name:   <type 'str'>                    Name of item to search

        :return:                <class '... .QTreeWidgetItem'>  Found item of "library_tree"
        :return:                <type 'NoneType'>               If item wasn't found '''


        # for each item in tree
        for item in self.get_tree_items():

            # skip 'Empty' and 'Textured' tree items
            if item.text(0) not in ['Empty', 'Textured']:

                # in user data of current item
                for user_data in item.data(0, QtCore.Qt.UserRole):

                    # compare requested name stored names
                    if user_data[0] == material_name:

                        # share link to the found tree item
                        return item


        # if nothing found (materialTag with changed value)
        return None



    def get_tree_items(self, root=None, items=None):

        ''' Creates list of all tree widget items

        :param root:    <class '... .QTreeWidgetItem'>  Parent item to find its children
        :param items:   <type 'list'>                   List of children of chosen parent

        :return:        <type 'list'>                   List of all tree widget items '''


        # define root item and children container for the first recursion level
        if not root:
            root = self.library_tree.invisibleRootItem()

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

        ''' Creates structure that store information about Maya Outliner tab

        :return: <type 'dict'> Outliner state structure '''


        # create output structure
        state = dict(selection_type=None)


        # check if there is selected objects
        selected_objects = selected()
        if selected_objects:


            # if all selected objects are mesh objects
            # change value of the key 'type' in output structure
            if type_control.uniform_selection(selected_objects, 'mesh'):
                state['selection_type'] = 'mesh'


            # if all selected objects are transform objects
            # change value of the key 'type' in output structure
            if type_control.uniform_selection(selected_objects, 'transform'):
                state['selection_type'] = 'transform'


        # share link to the output structure
        return state



    def get_geometry_tags(self):

        ''' Creates structure that store selected geometry names
        and its previously set export tags,
        also structure have characteristic of itself

        :return: <type 'dict'> Structure of export tags '''


        # create output structure
        structure = dict(
            uniform_selection=True,
            has_parameter=False,
            has_material=False,
            has_empty=False,
            parameters_only=False,
            empties_only=False,
            selected=[])


        pair_buffer = None

        # search all possible tags in selected geometry objects
        for geometry in selected():

            # create structure to store name and tags
            # for each geometry item
            structure_item = dict(
                geometry=geometry.name(),
                tags=[])


            # if geometry has material tag
            # append attribute value to pair structure
            if hasAttr(geometry, self.material_tag, checkShape=False):
                value = getAttr('{}.{}'.format(geometry.name(), self.material_tag))
                structure['has_material'] = True
                structure_item['tags'].append(value)

            # if geometry hasn't material tag
            # find tags for shader parameters
            # and append found tags itself to pair structure
            else:
                for tag in self.shader_parameters:
                    if hasAttr(geometry, tag, checkShape=False):
                        structure['has_parameter'] = True
                        structure_item['tags'].append(tag)


            # check if there is at least one selected geometry with no tag
            # then switch structure flag for empty item
            if structure_item['tags'] == []:
                structure['has_empty'] = True


            # check if all selected geometry objects have the same tags
            # then switch structure flag for uniform selection
            if isinstance(pair_buffer, type(None)):
                pair_buffer = structure_item['tags']

            if pair_buffer != structure_item['tags']:
                structure['uniform_selection'] = False


            # append pair structure for geometry item to output structure
            structure['selected'].append(structure_item)


        # check if all selected geometry objects have no tag at all
        # then switch structure flag for empty items
        if pair_buffer == [] and structure['uniform_selection']:
            structure['empties_only'] = True


        # check if all selected geometry objects have shader parameter tags only
        # then switch structure flag for parameter items
        if structure['has_parameter']:
            if not structure['has_material']:
                if not structure['has_empty']:
                    structure['parameters_only'] = True


        # share link to the output structure
        return structure



    def update_interface(self):

        ''' Clears interface to default state when selection in Maya is changed '''


        # update variable that store selected geometry names and its tags
        self.geometry_tags = self.get_geometry_tags()

        # deselects all selected items and lost the focus
        self.library_tree.clearSelection()
        self.library_tree.clearFocus()

        # switch list widgets to disabled
        self.empty_state.show()
        self.material_grid.hide()
        self.texture_tags.hide()

        # clear variable for material choice
        self.selected_material_item = None

        # set unchecked all items for shader parameter choice
        for tag in self.shader_parameter_items:
            tag.setCheckState(QtCore.Qt.Unchecked)


        # get information of Outliner selection
        selection_state = self.outliner_state()

        # disable/enable interface depending on selection validity
        if not selection_state['selection_type']:
            self.library_tree.setEnabled(False)
        else:
            self.library_tree.setEnabled(True)


            # run interface in corresponding mode
            # depending on count of selected geometry objects
            if len(selected()) < 2:
                self.inform_mode()
            else:
                self.warning_mode()



    def inform_mode(self):

        ''' Select interface items depending on tag of selected geometry object '''


        # set interface to inform style mode
        self.library_tree.setStyleSheet(self.tree_style_blue)
        self.material_grid.setStyleSheet(self.grid_style_blue)


        # if selected geometry object has no tag at all
        # then select 'Empty' tree item
        if self.geometry_tags['has_empty']:

            empty_item = self.library_tree.findItems(
                'Empty',
                QtCore.Qt.MatchExactly)[0]
            empty_item.setSelected(True)


        # if selected geometry object has material tag
        # then select material preview with tag name
        elif not self.geometry_tags['has_parameter']:
            self.select_material_item(self.geometry_tags['selected'][0]['tags'][0])


        # if selected geometry object has shader parameter tag
        # then set shader parameter items with tag names to checked state
        else:
            self.select_tag_items(self.geometry_tags['selected'][0]['tags'])



    def warning_mode(self):

        ''' Select interface items depending on tags of selected geometry objects '''


        # set interface to warning style mode
        self.library_tree.setStyleSheet(self.tree_style_red)
        self.material_grid.setStyleSheet(self.grid_style_red)


        # if all selected geometry have the same tags
        # then update interface depending on common attribute
        # and set interface to regular style mode
        if self.geometry_tags['uniform_selection']:
            self.library_tree.setStyleSheet(self.tree_style_blue)
            self.material_grid.setStyleSheet(self.grid_style_blue)

            if self.geometry_tags['empties_only']:
                empty_item = self.library_tree.findItems(
                    'Empty',
                    QtCore.Qt.MatchExactly)[0]
                empty_item.setSelected(True)

            elif self.geometry_tags['has_material']:
                self.select_material_item(self.geometry_tags['selected'][0]['tags'][0])

            else:
                self.select_tag_items(self.geometry_tags['selected'][0]['tags'])


        # if all selected geometry have different shader parameter tags
        # then select 'Textured' tree item and set all shader parameter items to unchecked state
        elif self.geometry_tags['parameters_only']:
            self.select_tag_items([])


        # if all selected geometry have different tags
        # then select tree widget items
        # (select all items if materialTag was changed manually)
        else:

            if self.geometry_tags['has_parameter']:
                textured_item = self.library_tree.findItems(
                    'Textured',
                    QtCore.Qt.MatchExactly)[0]
                textured_item.setSelected(True)


            if self.geometry_tags['has_empty']:
                empty_item = self.library_tree.findItems(
                    'Empty',
                    QtCore.Qt.MatchExactly)[0]
                empty_item.setSelected(True)


            for structure_item in self.geometry_tags['selected']:
                for tag in structure_item['tags']:

                    if tag not in self.shader_parameters:

                        tree_item = self.find_tree_item(tag)
                        if tree_item:
                            tree_item.setSelected(True)

                        else:
                            for tree_item in self.get_tree_items():
                                tree_item.setSelected(True)


            # if selected only one library category
            # then build previews and select appropriate items
            if len(self.library_tree.selectedItems()) == 1:

                self.update_list(self.library_tree.selectedItems()[0])

                for structure_item in self.geometry_tags['selected']:
                    grid_item = self.material_grid.findItems(
                        structure_item['tags'][0],
                        QtCore.Qt.MatchExactly)[0]
                    grid_item.setSelected(True)



    def select_material_item(self, material_name):

        ''' Build previews of material group and select item with chosen material name

        :param material_name: <type 'str'> Material name on the basis of which will be build interface '''


        # find tree item that has input material name
        tree_item = self.find_tree_item(material_name)
        if tree_item:

            # set material selection variable
            # select tree item
            self.selected_material_item = material_name
            tree_item.setSelected(True)


            # switch list widget to appropriate one
            # build previews of material group with input material name
            # select material item with input material name
            self.update_list(tree_item)


        # select all items if materialTag was changed manually
        # set interface to warning style mode
        else:
            for tree_item in self.get_tree_items():
                tree_item.setSelected(True)

            self.library_tree.setStyleSheet(self.tree_style_red)
            self.material_grid.setStyleSheet(self.grid_style_red)



    def select_tag_items(self, tag_list):

        ''' Set check/uncheck state for shader parameter items depending on input list

        :param tag_list: <type 'list'> List of loaded from geometry tags'''


        # select 'Textured' tree item
        textured_item = self.library_tree.findItems(
            'Textured',
            QtCore.Qt.MatchExactly)[0]
        textured_item.setSelected(True)


        # set check state for shader parameter items
        for item in self.shader_parameter_items:
            item.setCheckState(QtCore.Qt.Unchecked)

            if item.text() in tag_list:
                item.setCheckState(QtCore.Qt.Checked)


        # switch list widget to appropriate one
        self.update_list(textured_item)



    def update_list(self, tree_item):

        ''' Switches list widgets to show appropriate information

        :param tree_item: <type '... .QTreeWidgetItem'> Selected tree item '''


        # if selected 'Empty' item then:
        # any way set interface to inform style mode
        # switch list widget to disabled one
        # deletes all existing tags in selected geometry objects
        if tree_item.text(0) == 'Empty':

            self.library_tree.setStyleSheet(self.tree_style_blue)
            self.material_grid.setStyleSheet(self.grid_style_blue)

            self.selected_material_item = None

            self.empty_state.show()
            self.material_grid.hide()
            self.texture_tags.hide()

            self.delete_tags()


        # if selected 'Textured' item then:
        # switch list widget to show shader parameter list
        elif tree_item.text(0) == 'Textured':
            self.empty_state.hide()
            self.material_grid.hide()
            self.texture_tags.show()


        # if selected material library items then:
        # switch list widget to show list of material library group
        else:
            self.empty_state.hide()
            self.material_grid.show()
            self.texture_tags.hide()

            self.build_material_previews(tree_item)



    def build_material_previews(self, tree_item):

        ''' Fills list widget with previews of selected material group

        :param tree_item: <type '... .QTreeWidgetItem'> Selected tree item '''


        # clear material library list widget
        self.material_grid.clear()


        # read user data from selected tree item
        # create material library item previews using user data
        for i in tree_item.data(0, QtCore.Qt.UserRole):
            item = QtWidgets.QListWidgetItem(self.material_grid)
            item.setText(i[0])
            icon_path = os.path.join(i[1], 'Luxo_jr_100.png')
            item.setIcon(QtGui.QIcon(icon_path))


            # show selection from previous choice
            if item.text() == self.selected_material_item:
                item.setSelected(True)



    def update_tags(self, list_item):

        ''' Update tags for each selected geometry object
        depending on chosen material library or shader parameter widget item

        :param list_item:  <type '... .QListWidgetItem'>  Chosen widget item '''


        # delete all existing tags
        # in selected geometry objects
        self.delete_tags()

        # set interface to inform style mode
        self.library_tree.setStyleSheet(self.tree_style_blue)
        self.material_grid.setStyleSheet(self.grid_style_blue)


        # if input item is from shader parameter list then:
        # clear material selection variable
        # check/uncheck widget item
        # add chosen shader parameter tags to selected objects
        if self.library_tree.selectedItems()[0].text(0) == 'Textured':

            self.selected_material_item = None

            if list_item.checkState() == QtCore.Qt.CheckState.Checked:
                list_item.setCheckState(QtCore.Qt.Unchecked)
            else:
                list_item.setCheckState(QtCore.Qt.Checked)

            for item in self.shader_parameter_items:
                if item.checkState() == QtCore.Qt.CheckState.Checked:
                    attribute_path_list = self.add_tag(item.text())
                    for attribute_path in attribute_path_list:
                        setAttr(attribute_path, '{}_MAPID_.tex'.format(item.text()))


        # if input item is from material library list then:
        # uncheck all shader parameter widget items
        # set material selection variable
        # add chosen material tag to selected objects
        else:
            self.selected_material_item = list_item.text()

            for item in self.shader_parameter_items:
                item.setCheckState(QtCore.Qt.Unchecked)

            attribute_path_list = self.add_tag(self.material_tag)
            for attribute_path in attribute_path_list:
                setAttr(attribute_path, list_item.text())


        # do not show selection after clicking
        self.texture_tags.clearSelection()
        self.texture_tags.clearFocus()



    def delete_tags(self):

        ''' Deletes all existing tags in selected geometry objects '''


        tag_list = self.shader_parameters[:]
        tag_list.append(self.material_tag)

        for geometry in selected():
            for tag in tag_list:

                if hasAttr(geometry, tag, checkShape=False):
                    deleteAttr('{}.{}'.format(geometry, tag))



    def add_tag(self, tag_name):

        ''' Add attribute for each selected geometry object

        :param tag_name: <type 'str'> Name for attribute that will be created '''


        # create container for attribute paths
        # collect names of selected geometry objects
        attribute_path_list = []
        selected_objects = [geometry.name() for geometry in selected()]


        # add attribute for each selected geometry object
        for geometry_name in selected_objects:
            select(geometry_name)

            addAttr(longName=tag_name, dataType='string')
            attribute_path_list.append('{}.{}'.format(geometry_name, tag_name))


        # select all collected previously geometry objects
        # share link to the list of attribute paths
        select(selected_objects)
        return attribute_path_list



    def dockCloseEventTriggered(self, *args, **kwargs):

        # detach method for updating interface from SelectionChanged event
        scriptJob(kill=self.selection_event)
        super(DockableWindow, self).dockCloseEventTriggered(*args, **kwargs)




def main():

    # run program only if Renderman is installed

    if os.environ.get('RMANTREE'):
        dockable_window = DockableWindow()
        dockable_window.show(dockable=True)

    else:
        inViewMessage(
            amg='Renderman is not installed',
            pos='botCenter',
            fade=True)


# these options are for _install_.py module

shelf_command = '''
from ms_shelf import export_tag
# reload(export_tag)
export_tag.main()
'''

install_options = dict(
    image1='export_tag.png',
    label='Shader Tag Manager',
    annotation='Run dockable Maya window for managing shader tags',
    imageOverlayLabel='',
    command=shelf_command,
    doubleClickCommand='')
