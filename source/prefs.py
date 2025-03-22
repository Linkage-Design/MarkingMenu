################################################################################
#
#   prefs.py
#
################################################################################
#
#   DESCRIPTION
#       This file contains class and function definistions to support the
#       preferences for the Marking Menus Blender Add-on package
#
#   AUTHOR
#       Jayme Wilkinson
#
#   CREATED
#       Mar 20, 2025
#
################################################################################
#
#   Copyright (C) 2025 Jayme Wilkinson
#
#   The software and information contained herein are proprietary to, and
#   comprise valuable trade secrets of Jayme Wilkinson, whom intends
#   to preserve as trade secrets such software and information. This software
#   and information or any other copies thereof may not be provided or
#   otherwise made available to any other person or organization.
#
###############################################################################
import bpy

from   . import utils

###############################################################################
#
#   Define Default values for this class here
#
###############################################################################

#  Define the URL Locations
URL_LIST = [
    ("Linkage Design", "linkage-d.com/tools-training"),
    ("Report Issues", "github.com/Linkage-Design/MarkingMenus/issues"),
    ("Blender Marketplace", "blendermarket.com/products/customizable-marking-menus"),
    ("Gumroad", "linkagedesign.gumroad.com/l/markingmenus"),
    ("Instagram", "instagram.com/LinkageDesign"),
    ("YouTube", "youtube.com/c/LinkageDesign")
]


###############################################################################
#
#   Define Default Values for this Add-on
#
###############################################################################

#   Default object mode operators
OBJECT_OPERATORS = [
    ("object.select_all(action='TOGGLE')", "Select All (Toggle)", "Toggle selection of all objects"),
    ("object.select_all(action='DESELECT')", "Deselect All", "Deselect all objects"),
    ("object.select_random", "Select Random", "Randomly select objects"),
    ("object.select_all(action='INVERT')", "Inverse Selection", "Invert the current selection"),
    ("object.duplicate_move", "Duplicate", "Duplicate selected objects"),
    ("object.delete", "Delete", "Delete selected objects"),
    ("object.join", "Join", "Join selected objects"),
    ("object.subdivision_set(level=1)", "Set Subdivision Level 1", "Set subdivision level to 1"),
    ("object.shade_smooth", "Shade Smooth", "Set shading to smooth"),
    ("object.shade_flat", "Shade Flat", "Set shading to flat"),
    ("object.origin_set(type='ORIGIN_GEOMETRY')", "Set Origin to Geometry", "Set origin to center of geometry"),
    ("object.convert(target='MESH')", "Convert to Mesh", "Convert selected objects to mesh"),
    ("object.modifier_add(type='SUBSURF')", "Add Subdivision Surface", "Add subdivision surface modifier"),
    ("object.modifier_add", "Add Modifier Menu", "Open the Add Modifier menu"),
    ("wm.call_menu(name='VIEW3D_MT_object_apply')", "Apply Menu", "Open the Apply menu"),
    ("wm.call_menu_pie(name='VIEW3D_MT_pivot_pie')", "Origin Pie Menu", "Open the origin/pivot pie menu"),
    ("Custom", "Custom Operator", "Use a custom operator")
]

#    Default edit mode operators
EDIT_OPERATORS = [
    ("mesh.select_all(action='TOGGLE')", "Select All (Toggle)", "Toggle selection of all elements"),
    ("mesh.select_all(action='DESELECT')", "Deselect All", "Deselect all elements"),
    ("mesh.select_random", "Select Random", "Randomly select elements"),
    ("mesh.select_all(action='INVERT')", "Inverse Selection", "Invert the current selection"),
    ("mesh.duplicate_move", "Duplicate", "Duplicate selected elements"),
    ("mesh.delete", "Delete", "Delete selected elements"),
    ("mesh.separate(type='SELECTED')", "Separate Selected", "Separate selected elements"),
    ("mesh.subdivide", "Subdivide", "Subdivide selected edges"),
    ("mesh.faces_shade_smooth", "Shade Smooth", "Set shading to smooth"),
    ("mesh.faces_shade_flat", "Shade Flat", "Set shading to flat"),
    ("mesh.quads_convert_to_tris", "Triangulate Faces", "Convert quads to triangles"),
    ("mesh.tris_convert_to_quads", "Quadrangulate Faces", "Convert triangles to quads"),
    ("mesh.extrude_region_move", "Extrude Region", "Extrude selected region"),
    ("wm.call_menu(name='VIEW3D_MT_edit_mesh_faces')", "Faces Menu", "Open the Faces menu"),
    ("wm.call_menu_pie(name='VIEW3D_MT_pivot_pie')", "Origin Pie Menu", "Open the origin/pivot pie menu"),
    ("Custom", "Custom Operator", "Use a custom operator")
]

#   Default Object2 marking Menu Operators (Initially the same as OBJECT Operators)
OBJECT2_OPERATORS = OBJECT_OPERATORS

#   Define the default preference properties for this add-on
defaults = {
    "object":  [
                "object.select_all(action='TOGGLE')",
                "object.delete",
                "object.duplicate_move",
                "object.shade_smooth",
                "object.join",
                "object.convert(target='MESH')",
                "object.origin_set(type='ORIGIN_GEOMETRY')",
                "wm.call_menu(name='VIEW3D_MT_object_apply')"
            ],
    "object2": [
                "object.select_all(action='TOGGLE')",
                "object.delete",
                "object.duplicate_move",
                "object.shade_smooth",
                "object.join",
                "object.convert(target='MESH')",
                "object.origin_set(type='ORIGIN_GEOMETRY')",
                "wm.call_menu(name='VIEW3D_MT_object_apply')"
            ],
    "edit":    [
                "mesh.select_all(action='TOGGLE')",
                "mesh.delete",
                "mesh.duplicate_move",
                "mesh.extrude_region_move",
                "mesh.subdivide",
                "mesh.separate(type='SELECTED')",
                "mesh.faces_shade_smooth",
                "wm.call_menu(name='VIEW3D_MT_edit_mesh_faces')"
            ]
}

#   Define a place to store and process this add-on's keymaps.
addon_keymaps = []

#   Define a variable to store icon collections for this add-on
icon_collections = utils.loadIcons()

###############################################################################
#
#   Pie Menu Addon Preferences Classes
#
###############################################################################
class Preferences(bpy.types.AddonPreferences):
    '''
    DESCRIPTION
        This class defines the preferences for this add-on
    '''

    bl_idname = __package__

    #   Define the properties for the pie menu items
    object_pie_item_0: bpy.props.EnumProperty(name="Object Pie Item 1", items=OBJECT_OPERATORS, default=defaults["object"][0]) # type: ignore
    object_pie_item_1: bpy.props.EnumProperty(name="Object Pie Item 2", items=OBJECT_OPERATORS, default=defaults["object"][1]) # type: ignore
    object_pie_item_2: bpy.props.EnumProperty(name="Object Pie Item 3", items=OBJECT_OPERATORS, default=defaults["object"][2]) # type: ignore
    object_pie_item_3: bpy.props.EnumProperty(name="Object Pie Item 4", items=OBJECT_OPERATORS, default=defaults["object"][3]) # type: ignore
    object_pie_item_4: bpy.props.EnumProperty(name="Object Pie Item 5", items=OBJECT_OPERATORS, default=defaults["object"][4]) # type: ignore
    object_pie_item_5: bpy.props.EnumProperty(name="Object Pie Item 6", items=OBJECT_OPERATORS, default=defaults["object"][5]) # type: ignore
    object_pie_item_6: bpy.props.EnumProperty(name="Object Pie Item 7", items=OBJECT_OPERATORS, default=defaults["object"][6]) # type: ignore
    object_pie_item_7: bpy.props.EnumProperty(name="Object Pie Item 8", items=OBJECT_OPERATORS, default=defaults["object"][7]) # type: ignore

    object2_pie_item_0: bpy.props.EnumProperty(name="Object2 Pie Item 1", items=OBJECT2_OPERATORS, default=defaults["object2"][0]) # type: ignore
    object2_pie_item_1: bpy.props.EnumProperty(name="Object2 Pie Item 2", items=OBJECT2_OPERATORS, default=defaults["object2"][1]) # type: ignore
    object2_pie_item_2: bpy.props.EnumProperty(name="Object2 Pie Item 3", items=OBJECT2_OPERATORS, default=defaults["object2"][2]) # type: ignore
    object2_pie_item_3: bpy.props.EnumProperty(name="Object2 Pie Item 4", items=OBJECT2_OPERATORS, default=defaults["object2"][3]) # type: ignore
    object2_pie_item_4: bpy.props.EnumProperty(name="Object2 Pie Item 5", items=OBJECT2_OPERATORS, default=defaults["object2"][4]) # type: ignore
    object2_pie_item_5: bpy.props.EnumProperty(name="Object2 Pie Item 6", items=OBJECT2_OPERATORS, default=defaults["object2"][5]) # type: ignore
    object2_pie_item_6: bpy.props.EnumProperty(name="Object2 Pie Item 7", items=OBJECT2_OPERATORS, default=defaults["object2"][6]) # type: ignore
    object2_pie_item_7: bpy.props.EnumProperty(name="Object2 Pie Item 8", items=OBJECT2_OPERATORS, default=defaults["object2"][7]) # type: ignore

    edit_pie_item_0: bpy.props.EnumProperty(name="Edit Pie Item 1", items=EDIT_OPERATORS, default=defaults["edit"][0]) # type: ignore
    edit_pie_item_1: bpy.props.EnumProperty(name="Edit Pie Item 2", items=EDIT_OPERATORS, default=defaults["edit"][1]) # type: ignore
    edit_pie_item_2: bpy.props.EnumProperty(name="Edit Pie Item 3", items=EDIT_OPERATORS, default=defaults["edit"][2]) # type: ignore
    edit_pie_item_3: bpy.props.EnumProperty(name="Edit Pie Item 4", items=EDIT_OPERATORS, default=defaults["edit"][3]) # type: ignore
    edit_pie_item_4: bpy.props.EnumProperty(name="Edit Pie Item 5", items=EDIT_OPERATORS, default=defaults["edit"][4]) # type: ignore
    edit_pie_item_5: bpy.props.EnumProperty(name="Edit Pie Item 6", items=EDIT_OPERATORS, default=defaults["edit"][5]) # type: ignore
    edit_pie_item_6: bpy.props.EnumProperty(name="Edit Pie Item 7", items=EDIT_OPERATORS, default=defaults["edit"][6]) # type: ignore
    edit_pie_item_7: bpy.props.EnumProperty(name="Edit Pie Item 8", items=EDIT_OPERATORS, default=defaults["edit"][7]) # type: ignore

    object_custom_op_0: bpy.props.StringProperty(name="Object Custom Operator 1") # type: ignore
    object_custom_op_1: bpy.props.StringProperty(name="Object Custom Operator 2") # type: ignore
    object_custom_op_2: bpy.props.StringProperty(name="Object Custom Operator 3") # type: ignore
    object_custom_op_3: bpy.props.StringProperty(name="Object Custom Operator 4") # type: ignore
    object_custom_op_4: bpy.props.StringProperty(name="Object Custom Operator 5") # type: ignore
    object_custom_op_5: bpy.props.StringProperty(name="Object Custom Operator 6") # type: ignore
    object_custom_op_6: bpy.props.StringProperty(name="Object Custom Operator 7") # type: ignore
    object_custom_op_7: bpy.props.StringProperty(name="Object Custom Operator 8") # type: ignore

    object2_custom_op_0: bpy.props.StringProperty(name="Object2 Custom Operator 1") # type: ignore
    object2_custom_op_1: bpy.props.StringProperty(name="Object2 Custom Operator 2") # type: ignore
    object2_custom_op_2: bpy.props.StringProperty(name="Object2 Custom Operator 3") # type: ignore
    object2_custom_op_3: bpy.props.StringProperty(name="Object2 Custom Operator 4") # type: ignore
    object2_custom_op_4: bpy.props.StringProperty(name="Object2 Custom Operator 5") # type: ignore
    object2_custom_op_5: bpy.props.StringProperty(name="Object2 Custom Operator 6") # type: ignore
    object2_custom_op_6: bpy.props.StringProperty(name="Object2 Custom Operator 7") # type: ignore
    object2_custom_op_7: bpy.props.StringProperty(name="Object2 Custom Operator 8") # type: ignore

    edit_custom_op_0: bpy.props.StringProperty(name="Edit Custom Operator 1") # type: ignore
    edit_custom_op_1: bpy.props.StringProperty(name="Edit Custom Operator 2") # type: ignore
    edit_custom_op_2: bpy.props.StringProperty(name="Edit Custom Operator 3") # type: ignore
    edit_custom_op_3: bpy.props.StringProperty(name="Edit Custom Operator 4") # type: ignore
    edit_custom_op_4: bpy.props.StringProperty(name="Edit Custom Operator 5") # type: ignore
    edit_custom_op_5: bpy.props.StringProperty(name="Edit Custom Operator 6") # type: ignore
    edit_custom_op_6: bpy.props.StringProperty(name="Edit Custom Operator 7") # type: ignore
    edit_custom_op_7: bpy.props.StringProperty(name="Edit Custom Operator 8") # type: ignore

    def draw(self, context):
        '''
        DESCRIPTION
            This method draws the user interface for this add-on preferenses. This
            ui lives in the add-ons section of the user's preference window

        ARGUMENTS
            context     (in)    A Blender context to get some info from.

        RETURN
            None
        '''

        #   Create a parent layout for our preference panels
        parentLayt = self.layout

        #   Create a new label for the Mariking Menu Settings
        parentLayt.label(text = "Marking Menu Settings")

        #   Populate the parentLayout with the Marking Menu ui elements
        for mode in defaults:
            #   Create a panel in our layout for each mode
            header, panel = parentLayt.panel(f"linkage_{mode}_marking_menus", default_closed = True)
            header.label(text=f"{mode.capitalize()} Marking Menus")

            if panel:
                #   Create a row for each mode and populate it with its pie menu options
                for i in range(8):
                    row = panel.row()
                    prop_name = f"{mode}_pie_item_{i}"
                    custom_name = f"{mode}_custom_op_{i}"
                    row.prop(self, prop_name)

                    if getattr(self, prop_name) == "Custom":
                        sub_row = row.row(align=True)
                        sub_row.prop(self, custom_name, text="")
                        op = sub_row.operator("pie.search_operator", text="", icon='VIEWZOOM')
                        op.target_property = custom_name

        #   Create a new label for the website buttons
        parentLayt.label(text = "Links to Websites")

        #   Create buttons for each url in the URL_LIST
        for i in range(0, len(URL_LIST), 2):
            rowLayt = parentLayt.row()
            for col in (0, 1):
                try:
                    #   Get the site and url values from URL_LIST
                    name, url = URL_LIST[i + col]
                    iconId = name.replace(' ', '')

                    #   Create the button
                    op = rowLayt.operator("wm.url_open", text = name,
                                icon_value = icon_collections[iconId].icon_id)
                    op.url = f"https://{url}"

                except IndexError as e:
                    break


###############################################################################
#
#   Registartion / Unregistartion functions.
#
###############################################################################
def register():
    #   Register module
    bpy.utils.register_module(__name__)

def unregister():
    #   Unregister module
    bpy.utils.unregister_class(__name__)
