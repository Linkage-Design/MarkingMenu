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
#       Oct 2024 Initial Version
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

from    . import prefs
from    . import utils


###############################################################################
#
#   Classes for MarkingMenu Extension
#
###############################################################################
class PIE_MT_CustomizableSelectionsBase(bpy.types.Menu):
    '''
    DESCRIPTION
        Blender Pie menus are populated in the following order.

            Compass         Numpad
            Position        Hotkey
            ---------       ------
              West            4
              East            6
              South           2
              North           8
            NorthWest         7
            NorthEast         9
            SouthWest         1
            SouthEast         3

    '''
    PIE_POSITIONS = [6, 2, 4, 0, 7, 1, 5, 3]

    def draw(self, context):
        '''
        DESCRIPTION
            This method is called by Blender when it needs to draw our
            Pie Menu Items

        ARGUMENTS
            context     (in)   A context object we can use to get info

        RETURN
            None
        '''

        #   Get the preference data for this package
        preferences = context.preferences.addons[__package__].preferences

        #   Define a UI layout for the PieMenu
        pie_layt = self.layout.menu_pie()

        for i in self.PIE_POSITIONS:
            op_name   = getattr(preferences, f"{self.mode}_pie_item_{i}")
            custom_op = getattr(preferences, f"{self.mode}_custom_op_{i}")

            if op_name == "Custom":
                if custom_op:
                    self.draw_custom_operator(pie_layt, custom_op)
                else:
                    pie_layt.separator()

            elif op_name:
                self.draw_operator(pie_layt, op_name)

            else:
                pie_layt.separator()

    def draw_operator(self, pie, op_string):
        '''
        DESCRIPTION
            This method is called by the draw method to set attribute values
            for the standard operators

        ARGUMENTS
            pie         (in)    A Pie Menu Object to populate
            op_string   (in)    The operator string to add to the pie menu

        RETURN
            None
        '''

        #   Seperate the operator name from its arguments in op_string
        op_name, op_args = self.parse_operator_string(op_string)

        #   Detirmine the text label of the operator from its function
        op_text = next((item[1] for item in self.common_operators if item[0] == op_string), op_string)

        #   Check to see if the operator name exists in the python library
        if hasattr(bpy.ops, op_name):
            #   Add the op_name and op_text to the pie menu
            pie_menu_item = pie.operator(op_name, text = op_text)

            #   Add the op_args to the pie_menu_item
            for arg, value in op_args.items():
                try:
                    setattr(pie_menu_item, arg, value)
                except:
                    self.report({'WARNING'}, f"Could not set property {arg} for operator {op_name}")
        else:
            pie.separator()
            self.report({'WARNING'}, f"Operator {op_name} not found")

    def draw_custom_operator(self, pie, op_string):
        '''
        DESCRIPTION
            This method is called by the draw method to set attribute values
            for the custom operators

        ARGUMENTS
            pie         (in)    A Pie Menu Object to populate
            op_string   (in)    The operator string to add to the pie menu

        RETURN
            None
        '''

        #   Seperate the operator name from its arguments in op_string
        op_name, op_args = self.parse_operator_string(op_string)

        #   Detirmine the text label of the operator from its function
        op_text = op_name.split(".")[-1].replace("_", " ").title()

        if hasattr(bpy.ops, op_name.split('.')[0]):
            #   Add the op_name and op_text to the pie menu
            pie_menu_item = pie.operator(op_name, text = op_text)

            #   Add the op_args to the pie_menu_item
            for arg, value in op_args.items():
                try:
                    setattr(pie_menu_item, arg, value)
                except:
                    self.report({'WARNING'}, f"Could not set property {arg} for operator {op_name}")
        else:
            pie.separator()
            self.report({'WARNING'}, f"Custom operator {op_name} not found")

    def parse_operator_string(self, op_string):
        '''
        DESCRIPTION
            This method is used by the draw and draw_custom methods to parse
            the op_string data into its parts (op_name, and op_args)

        ARGUMENTS
            op_string   (in)    The variable to parse

        RETURN
            op_name (str)       The name of the operatot
            op_args (dict)      A dictionary containing all the args and
                                their values
        '''

        op_parts = op_string.split("(", 1)
        op_name = op_parts[0]
        op_args = {}

        if len(op_parts) > 1:
            args_string = op_parts[1].rstrip(")")
            if args_string:
                for arg in args_string.split(","):
                    key, value = arg.split("=")
                    op_args[key.strip()] = value.strip("'")

        return op_name, op_args


class PIE_MT_CustomizableSelectionsObject(PIE_MT_CustomizableSelectionsBase):
    '''
    DESCRIPTION
        Define the pie menu for Object Mode (left click)
    '''
    bl_idname = "PIE_MT_customizable_selections_object"
    bl_label  = "Linkage Marking Menu (Object Mode)"

    mode = "object"
    common_operators = prefs.OBJECT_OPERATORS


class PIE_MT_CustomizableSelectionsObject2(PIE_MT_CustomizableSelectionsBase):
    '''
    DESCRIPTION
        Define the pie menu for Object Mode 2 (right click)
    '''
    bl_idname = "PIE_MT_customizable_selections_object_2"
    bl_label  = "Linkage Marking Menu (Object Mode 2)"

    mode = "object2"
    common_operators = copy.deepcopy(prefs.OBJECT_OPERATORS)


class PIE_MT_CustomizableSelectionsEdit(PIE_MT_CustomizableSelectionsBase):
    '''
    DESCRIPTION
        Define the pie menu for Edit Mode
    '''
    bl_idname = "PIE_MT_customizable_selections_edit"
    bl_label  = "Linkage Marking Menu (Edit Mode)"

    mode = "edit"
    common_operators = prefs.EDIT_OPERATORS


class PIE_OT_CallCustomizablePieMenu(bpy.types.Operator):
    '''
    DESCRIPTION
        Define the operator to call the object1 pie menu or edit pie menu, depending on context
    '''
    bl_idname = "pie.call_customizable_pie_menu"
    bl_label  = "Call Customizable Pie Menu"

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
    bl_label  = "Call Customizable Pie Menu 2"

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

    operator: bpy.props.EnumProperty(items = utils.get_all_operators) # type: ignore
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
#   Define a list of classes to register with Blender Add-On system
#
###############################################################################
addon_keymaps = []
classes = ( PIE_MT_CustomizableSelectionsObject,
            PIE_MT_CustomizableSelectionsObject2,
            PIE_MT_CustomizableSelectionsEdit,
            PIE_OT_CallCustomizablePieMenu,
            PIE_OT_CallCustomizablePieMenu2,
            PIE_OT_SearchOperator,
            prefs.MarkingMenu )


###############################################################################
#
#   Registartion / Unregistartion functions.
#
###############################################################################
def register():
    '''
    DESCRIPTION
        This method is used by Blender to register the components of this
        Add-On.

    ARGUMENTS
        None

    RETURN
        None
    '''
    #   Register modules
    for cls in classes:
        bpy.utils.register_class(cls)

    #   Register shortcuts for object mode pie menus
    wm  = bpy.context.window_manager
    kc  = wm.keyconfigs.addon
    if kc:
        #   Register keymap shortcuts for object mode pie menus
        km  = wm.keyconfigs.addon.keymaps.new(name = 'Object Mode')
        kmi = km.keymap_items.new('pie.call_customizable_pie_menu', 'LEFTMOUSE', 'PRESS', shift=True, ctrl=True)
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new('pie.call_customizable_pie_menu_2', 'RIGHTMOUSE', 'PRESS', shift=True, ctrl=True)
        addon_keymaps.append((km, kmi))

        #   Register keyboard shortcuts for edit mode pie menus
        km  = wm.keyconfigs.addon.keymaps.new(name='Mesh')
        kmi = km.keymap_items.new('pie.call_customizable_pie_menu', 'LEFTMOUSE', 'PRESS', shift=True, ctrl=True)
        addon_keymaps.append((km, kmi))

def unregister():
    '''
    DESCRIPTION
        This method is used by Blender to unregister the classes we
        registered in this Extension's register method.

    ARGUMENTS
        None

    RETURN
        None
    '''
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

###############################################################################
#
#   This is the main registration entrypoint for this Add-On
#
###############################################################################
if __name__ == "__main__":
    register()
