################################################################################
#
#   utils.py
#
################################################################################
#
#   DESCRIPTION
#       This file contains utility functions used in this Blender Add-on
#
#   AUTHOR
#       Jayme Wilkinsoin
#
#   CREATED
#       Mar 20, 2025
#
################################################################################
#
#   Copyright (C) 2025 Jayme Wilkinsoin
#
#   The software and information contained herein are proprietary to, and
#   comprise valuable trade secrets of Jayme Wilkinsoin, whom intends
#   to preserve as trade secrets such software and information. This software
#   and information or any other copies thereof may not be provided or
#   otherwise made available to any other person or organization.
#
################################################################################
import bpy

###############################################################################
#
#   Utility functions for the Add-On
#
###############################################################################
def get_all_operators(self, context):
    '''
    DESCRIPTION
        This method is used to get all operators for the search popup

    ARGUMENTS
        context     (in)    The current context for Blender

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

     # Sort by label, case-insensitive
    return sorted(items, key=lambda x: x[1].lower())
