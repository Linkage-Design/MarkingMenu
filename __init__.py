import bpy
import copy
from bpy.types import Menu, Operator, AddonPreferences
from bpy.props import StringProperty, EnumProperty

bl_info = {
    "name": "Linkage Marking Menu",
    "author": "Linkage Design",
    "version": (0, 5),
    "blender": (4, 2, 0),
    "description": "Customizable marking menu for Object and Edit modes",
    "category": "Interface",
}

COMMON_OBJECT_OPERATORS = COMMON_OBJECT2_OPERATORS = [
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

#COMMON_OBJECT2_OPERATORS = COMMON_OBJECT_OPERATORS.copy()

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

class PIE_MT_CustomizableSelectionsBase(Menu):
    #PIE_POSITIONS = [3, 5, 1, 7, 2, 6, 0, 4]
    PIE_POSITIONS = [6, 2, 4, 0, 7, 1, 5, 3]
    
    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        
        preferences = context.preferences.addons[__name__].preferences
        
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
        print("---------------")
        print(self.common_operators)
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
    bl_idname = "PIE_MT_customizable_selections_object"
    bl_label = "Linkage Marking Menu (Object Mode)"
    mode = "object"
    common_operators = COMMON_OBJECT_OPERATORS
    
class PIE_MT_CustomizableSelectionsObject2(PIE_MT_CustomizableSelectionsBase):
    bl_idname = "PIE_MT_customizable_selections_object_2"
    bl_label = "Linkage Marking Menu (Object Mode 2)"
    mode = "object2"
    common_operators = copy.deepcopy(COMMON_OBJECT_OPERATORS)

class PIE_MT_CustomizableSelectionsEdit(PIE_MT_CustomizableSelectionsBase):
    bl_idname = "PIE_MT_customizable_selections_edit"
    bl_label = "Linkage Marking Menu (Edit Mode)"
    mode = "edit"
    common_operators = COMMON_EDIT_OPERATORS

class PIE_OT_CallCustomizablePieMenu(Operator):
    bl_idname = "pie.call_customizable_pie_menu"
    bl_label = "Call Customizable Pie Menu"
    
    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.wm.call_menu_pie(name="PIE_MT_customizable_selections_object")
        elif context.mode == 'EDIT_MESH':
            bpy.ops.wm.call_menu_pie(name="PIE_MT_customizable_selections_edit")
        return {'FINISHED'}
    
class PIE_OT_CallCustomizablePieMenu2(Operator):
    bl_idname = "pie.call_customizable_pie_menu_2"
    bl_label = "Call Customizable Pie Menu 2"
    
    def execute(self, context):
        if context.mode == 'OBJECT':
            bpy.ops.wm.call_menu_pie(name="PIE_MT_customizable_selections_object_2")
        return {'FINISHED'}    

def get_all_operators(self, context):
    items = []
    for op_module_name in dir(bpy.ops):
        op_module = getattr(bpy.ops, op_module_name)
        for op_name in dir(op_module):
            if not op_name.startswith("__"):
                full_name = f"{op_module_name}.{op_name}"
                label = op_name.replace("_", " ").title()
                items.append((full_name, f"{label} ({op_module_name})", ""))
    return sorted(items, key=lambda x: x[1].lower())  # Sort by label, case-insensitive

class PIE_OT_SearchOperator(Operator):
    bl_idname = "pie.search_operator"
    bl_label = "Search Operator"
    bl_property = "operator"

    operator: EnumProperty(items=get_all_operators)
    target_property: StringProperty()

    def execute(self, context):
        preferences = context.preferences.addons[__name__].preferences
        setattr(preferences, self.target_property, self.operator)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {'RUNNING_MODAL'}

class PIE_AddonPreferences(AddonPreferences):
    bl_idname = __name__

    object_defaults = [
        "object.select_all(action='TOGGLE')",
        "object.delete",
        "object.duplicate_move",
        "object.shade_smooth",
        "object.join",
        "object.convert(target='MESH')",
        "object.origin_set(type='ORIGIN_GEOMETRY')",
        "wm.call_menu(name='VIEW3D_MT_object_apply')"
    ]

    edit_defaults = [
        "mesh.select_all(action='TOGGLE')",
        "mesh.delete",
        "mesh.duplicate_move",
        "mesh.extrude_region_move",
        "mesh.subdivide",
        "mesh.separate(type='SELECTED')",
        "mesh.faces_shade_smooth",
        "wm.call_menu(name='VIEW3D_MT_edit_mesh_faces')"
    ]

    for mode, defaults in [('object', object_defaults), ('object2', object_defaults), ('edit', edit_defaults)]:
        for i in range(8):
            exec(f"{mode}_pie_item_{i}: EnumProperty(name=f'{mode.capitalize()} Pie Item {i+1}', items=COMMON_{mode.upper()}_OPERATORS, default=defaults[i])")
            exec(f"{mode}_custom_op_{i}: StringProperty(name=f'{mode.capitalize()} Custom Operator {i+1}')")

    def draw(self, context):
        layout = self.layout
        
        for mode in ['object', 'object2', 'edit']:
            box = layout.box()
            box.label(text=f"{mode.capitalize()} Mode Pie Menu")
            for i in range(8):
                row = box.row()
                row.prop(self, f"{mode}_pie_item_{i}")
                if getattr(self, f"{mode}_pie_item_{i}") == "Custom":
                    sub_row = row.row(align=True)
                    sub_row.prop(self, f"{mode}_custom_op_{i}", text="")
                    op = sub_row.operator("pie.search_operator", text="", icon='VIEWZOOM')
                    op.target_property = f"{mode}_custom_op_{i}"

classes = (
    PIE_MT_CustomizableSelectionsObject,
    PIE_MT_CustomizableSelectionsObject2,    
    PIE_MT_CustomizableSelectionsEdit,
    PIE_OT_CallCustomizablePieMenu,
    PIE_OT_CallCustomizablePieMenu2,
    PIE_OT_SearchOperator,
    PIE_AddonPreferences,
)

addon_keymaps = []

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')
    kmi = km.keymap_items.new('pie.call_customizable_pie_menu', 'LEFTMOUSE', 'PRESS', shift=True, ctrl=True)
    kmi = km.keymap_items.new('pie.call_customizable_pie_menu_2', 'RIGHTMOUSE', 'PRESS', shift=True, ctrl=True)    
    addon_keymaps.append((km, kmi))
    
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh')
    kmi = km.keymap_items.new('pie.call_customizable_pie_menu', 'LEFTMOUSE', 'PRESS', shift=True, ctrl=True)
    addon_keymaps.append((km, kmi))

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()