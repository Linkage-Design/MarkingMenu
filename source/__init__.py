################################################################################
#
#   __init__.py
#
################################################################################
#
#   DESCRIPTION
#       This is the entry point for the Linkeage Design Marking Menus Blender
#       Add-on.
#
#   AUTHOR
#       Josh Kirkpatrick
#       Jayme Wilkinson
#
#   HISTORY
#       Oct 2025 Initial Version
#
################################################################################
#
#   Copyright (C) 2024 Linkage Design
#
#   The software and information contained herein are proprietary to, and
#   comprise valuable trade secrets of Linkage Design, which intends to
#   preserve as trade secrets such software and information. This software
#   and information or any other copies thereof may not be provided or
#   otherwise made available to any other person or organization.
#
################################################################################
import  bpy
import  copy


###############################################################################
#
#   Define Default Marking Menu Values
#
###############################################################################
#   Default object mode operators
COMMON_OBJECT_OPERATORS = [
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
    ("Custom", "Custom Operator", "Use a custom operator"),
]

#   Default Object2 marking Menu Operators (Initially the same as OBJECT Operators)
COMMON_OBJECT2_OPERATORS = COMMON_OBJECT_OPERATORS

#    Default edit mode operators
COMMON_EDIT_OPERATORS = [
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
    ("Custom", "Custom Operator", "Use a custom operator"),
]

#   Define a variable to store and process this addon's keymaps.
addon_keymaps = []

#   Default Preference Propertiess
defaults = {
    "object": [
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
    "edit": [
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


###############################################################################
#
#   Utility functions for the Add-On
#
###############################################################################
def get_all_operators(self, context):
    '''
    DESCRIPTION
        Get all operators for the search popup

    ARGUMENTS
        context

    RETURN
        A sortedlist of available operators
    '''
    items = []
    for op_module_name in dir(bpy.ops):
        op_module = getattr(bpy.ops, op_module_name)
        for op_name in dir(op_module):
            if not op_name.startswith("__"):
                full_name = f"{op_module_name}.{op_name}"
                label = op_name.replace("_", " ").title()
                items.append((full_name, f"{label} ({op_module_name})", ""))

    return sorted(items, key=lambda x: x[1].lower())  # Sort by label, case-insensitive


###############################################################################
#
#   Classes for PIE menus and operators
#
###############################################################################
class PIE_MT_CustomizableSelectionsBase(bpy.types.Menu):
    '''
    DESCRIPTION
        Define the base class for the pie menu

    '''
    PIE_POSITIONS = [6, 2, 4, 0, 7, 1, 5, 3]

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        preferences = context.preferences.addons[__package__].preferences

        for i in self.PIE_POSITIONS:
            op_name = getattr(preferences, f"{self.mode}_pie_item_{i}")
            custom_op = getattr(preferences, f"{self.mode}_custom_op_{i}")

            if op_name == "Custom":
                if custom_op:
                    self.draw_custom_operator(pie, custom_op, i)
                else:
                    pie.separator()
            elif op_name:
                self.draw_operator(pie, op_name, i)
            else:
                pie.separator()

    def draw_operator(self, pie, op_string, index):
        op_name, op_args = self.parse_operator_string(op_string)
        text = next((item[1] for item in self.common_operators if item[0] == op_string), op_string)

        if hasattr(bpy.ops, op_name.split('.')[0]):
            op = pie.operator(op_name, text=text)
            for key, value in op_args.items():
                try:
                    setattr(op, key, eval(value))
                except:
                    self.report({'WARNING'}, f"Could not set property {key} for operator {op_name}")
        else:
            pie.separator()
            self.report({'WARNING'}, f"Operator {op_name} not found")

    def draw_custom_operator(self, pie, op_string, index):
        op_name, op_args = self.parse_operator_string(op_string)
        text = op_name.split(".")[-1].replace("_", " ").title()

        if hasattr(bpy.ops, op_name.split('.')[0]):
            op = pie.operator(op_name, text=text)
            for key, value in op_args.items():
                try:
                    setattr(op, key, eval(value))
                except:
                    self.report({'WARNING'}, f"Could not set property {key} for operator {op_name}")
        else:
            pie.separator()
            self.report({'WARNING'}, f"Custom operator {op_name} not found")

    def parse_operator_string(self, op_string):
        op_parts = op_string.split("(", 1)
        op_name = op_parts[0]
        op_args = {}
        if len(op_parts) > 1:
            args_string = op_parts[1].rstrip(")")
            if args_string:
                for arg in args_string.split(","):
                    key, value = arg.split("=")
                    op_args[key.strip()] = value.strip()
        return op_name, op_args

class PIE_MT_CustomizableSelectionsObject(PIE_MT_CustomizableSelectionsBase):
    '''
    DESCRIPTION
        Define the pie menu for Object Mode (left click)
    '''
    bl_label  = "Linkage Marking Menu (Object Mode)"
    bl_idname = "PIE_MT_customizable_selections_object"
    mode = "object"
    common_operators = COMMON_OBJECT_OPERATORS

class PIE_MT_CustomizableSelectionsObject2(PIE_MT_CustomizableSelectionsBase):
    '''
    DESCRIPTION
        Define the pie menu for Object Mode 2 (right click)
    '''
    bl_idname = "PIE_MT_customizable_selections_object_2"
    bl_label = "Linkage Marking Menu (Object Mode 2)"
    mode = "object2"
    common_operators = copy.deepcopy(COMMON_OBJECT_OPERATORS)

class PIE_MT_CustomizableSelectionsEdit(PIE_MT_CustomizableSelectionsBase):
    '''
    DESCRIPTION
        Define the pie menu for Edit Mode
    '''
    bl_idname = "PIE_MT_customizable_selections_edit"
    bl_label = "Linkage Marking Menu (Edit Mode)"
    mode = "edit"
    common_operators = COMMON_EDIT_OPERATORS

class PIE_OT_CallCustomizablePieMenu(bpy.types.Operator):
    '''
    DESCRIPTION
        Define the operator to call the object1 pie menu or edit pie menu, depending on context
    '''
    bl_idname = "pie.call_customizable_pie_menu"
    bl_label = "Call Customizable Pie Menu"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.wm.call_menu_pie(name="PIE_MT_customizable_selections_object")
        elif context.mode == 'EDIT_MESH':
            bpy.ops.wm.call_menu_pie(name="PIE_MT_customizable_selections_edit")
        return {'FINISHED'}

class PIE_OT_CallCustomizablePieMenu2(bpy.types.Operator):
    '''
    DESCRIPTION
        Define the operator to call the object1 pie menu
    '''
    bl_idname = "pie.call_customizable_pie_menu_2"
    bl_label = "Call Customizable Pie Menu 2"

    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.wm.call_menu_pie(name="PIE_MT_customizable_selections_object_2")
        return {'FINISHED'}

class PIE_OT_SearchOperator(bpy.types.Operator):
    '''
    DESCRIPTION
        Define the operator for the search popup in the preferences menu
    '''
    bl_idname   = "pie.search_operator"
    bl_label    = "Search Operator"
    bl_property = "operator"

    operator: bpy.props.EnumProperty(items = get_all_operators) # type: ignore
    target_property: bpy.props.StringProperty() # type: ignore

    def execute(self, context):
        preferences = context.preferences.addons[__package__].preferences
        setattr(preferences, self.target_property, self.operator)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'RUNNING_MODAL'}


###############################################################################
#
#   Pie Menu Addon Preferences Classes
#
###############################################################################
class PIE_AddonPreferences(bpy.types.AddonPreferences):
    '''
    DESCRIPTION
        Define the preferences for the addon
    '''
    bl_idname = __package__

    # Define the properties for the pie menu items
    object_pie_item_0: bpy.props.EnumProperty(name="Object Pie Item 1", items=COMMON_OBJECT_OPERATORS, default=defaults["object"][0]) # type: ignore
    object_pie_item_1: bpy.props.EnumProperty(name="Object Pie Item 2", items=COMMON_OBJECT_OPERATORS, default=defaults["object"][1]) # type: ignore
    object_pie_item_2: bpy.props.EnumProperty(name="Object Pie Item 3", items=COMMON_OBJECT_OPERATORS, default=defaults["object"][2]) # type: ignore
    object_pie_item_3: bpy.props.EnumProperty(name="Object Pie Item 4", items=COMMON_OBJECT_OPERATORS, default=defaults["object"][3]) # type: ignore
    object_pie_item_4: bpy.props.EnumProperty(name="Object Pie Item 5", items=COMMON_OBJECT_OPERATORS, default=defaults["object"][4]) # type: ignore
    object_pie_item_5: bpy.props.EnumProperty(name="Object Pie Item 6", items=COMMON_OBJECT_OPERATORS, default=defaults["object"][5]) # type: ignore
    object_pie_item_6: bpy.props.EnumProperty(name="Object Pie Item 7", items=COMMON_OBJECT_OPERATORS, default=defaults["object"][6]) # type: ignore
    object_pie_item_7: bpy.props.EnumProperty(name="Object Pie Item 8", items=COMMON_OBJECT_OPERATORS, default=defaults["object"][7]) # type: ignore

    object2_pie_item_0: bpy.props.EnumProperty(name="Object2 Pie Item 1", items=COMMON_OBJECT2_OPERATORS, default=defaults["object2"][0]) # type: ignore
    object2_pie_item_1: bpy.props.EnumProperty(name="Object2 Pie Item 2", items=COMMON_OBJECT2_OPERATORS, default=defaults["object2"][1]) # type: ignore
    object2_pie_item_2: bpy.props.EnumProperty(name="Object2 Pie Item 3", items=COMMON_OBJECT2_OPERATORS, default=defaults["object2"][2]) # type: ignore
    object2_pie_item_3: bpy.props.EnumProperty(name="Object2 Pie Item 4", items=COMMON_OBJECT2_OPERATORS, default=defaults["object2"][3]) # type: ignore
    object2_pie_item_4: bpy.props.EnumProperty(name="Object2 Pie Item 5", items=COMMON_OBJECT2_OPERATORS, default=defaults["object2"][4]) # type: ignore
    object2_pie_item_5: bpy.props.EnumProperty(name="Object2 Pie Item 6", items=COMMON_OBJECT2_OPERATORS, default=defaults["object2"][5]) # type: ignore
    object2_pie_item_6: bpy.props.EnumProperty(name="Object2 Pie Item 7", items=COMMON_OBJECT2_OPERATORS, default=defaults["object2"][6]) # type: ignore
    object2_pie_item_7: bpy.props.EnumProperty(name="Object2 Pie Item 8", items=COMMON_OBJECT2_OPERATORS, default=defaults["object2"][7]) # type: ignore

    edit_pie_item_0: bpy.props.EnumProperty(name="Edit Pie Item 1", items=COMMON_EDIT_OPERATORS, default=defaults["edit"][0]) # type: ignore
    edit_pie_item_1: bpy.props.EnumProperty(name="Edit Pie Item 2", items=COMMON_EDIT_OPERATORS, default=defaults["edit"][1]) # type: ignore
    edit_pie_item_2: bpy.props.EnumProperty(name="Edit Pie Item 3", items=COMMON_EDIT_OPERATORS, default=defaults["edit"][2]) # type: ignore
    edit_pie_item_3: bpy.props.EnumProperty(name="Edit Pie Item 4", items=COMMON_EDIT_OPERATORS, default=defaults["edit"][3]) # type: ignore
    edit_pie_item_4: bpy.props.EnumProperty(name="Edit Pie Item 5", items=COMMON_EDIT_OPERATORS, default=defaults["edit"][4]) # type: ignore
    edit_pie_item_5: bpy.props.EnumProperty(name="Edit Pie Item 6", items=COMMON_EDIT_OPERATORS, default=defaults["edit"][5]) # type: ignore
    edit_pie_item_6: bpy.props.EnumProperty(name="Edit Pie Item 7", items=COMMON_EDIT_OPERATORS, default=defaults["edit"][6]) # type: ignore
    edit_pie_item_7: bpy.props.EnumProperty(name="Edit Pie Item 8", items=COMMON_EDIT_OPERATORS, default=defaults["edit"][7]) # type: ignore

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
        layout = self.layout

        for mode in defaults:
            box = layout.box()
            box.label(text=f"{mode.capitalize()} Mode Pie Menu")

            for i in range(8):
                row = box.row()
                prop_name = f"{mode}_pie_item_{i}"
                custom_name = f"{mode}_custom_op_{i}"
                row.prop(self, prop_name)

                if getattr(self, prop_name) == "Custom":
                    sub_row = row.row(align=True)
                    sub_row.prop(self, custom_name, text="")
                    op = sub_row.operator("pie.search_operator", text="", icon='VIEWZOOM')
                    op.target_property = custom_name


###############################################################################
#
#   Define a list of classes to register with Blender Add-On system
#
###############################################################################
classes = (
    PIE_MT_CustomizableSelectionsObject,
    PIE_MT_CustomizableSelectionsObject2,
    PIE_MT_CustomizableSelectionsEdit,
    PIE_OT_CallCustomizablePieMenu,
    PIE_OT_CallCustomizablePieMenu2,
    PIE_OT_SearchOperator,
    PIE_AddonPreferences
)

###############################################################################
#
#   Registartion / Unregistartion functions.
#
###############################################################################
def register():
    #   Register modules
    for cls in classes:
        bpy.utils.register_class(cls)

    #   Register shortcuts for object mode pie menus
    wm  = bpy.context.window_manager
    km  = wm.keyconfigs.addon.keymaps.new(name = 'Object Mode')
    kmi = km.keymap_items.new('pie.call_customizable_pie_menu', 'LEFTMOUSE', 'PRESS', shift=True, ctrl=True)
    kmi = km.keymap_items.new('pie.call_customizable_pie_menu_2', 'RIGHTMOUSE', 'PRESS', shift=True, ctrl=True)
    addon_keymaps.append((km, kmi))

    #   Register keyboard shortcuts for edit mode pie menus
    km  = wm.keyconfigs.addon.keymaps.new(name='Mesh')
    kmi = km.keymap_items.new('pie.call_customizable_pie_menu', 'LEFTMOUSE', 'PRESS', shift=True, ctrl=True)
    addon_keymaps.append((km, kmi))

def unregister():
    #   Unregister modules in reverse order to avoid dependency issues
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    #   Remove keyboard shortcuts
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()
