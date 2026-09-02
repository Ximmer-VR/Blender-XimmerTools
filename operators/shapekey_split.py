import bpy


def split_shape_key(obj, key_name, blend_zone):

    print(blend_zone)

    """Split the selected shape key into Left and Right versions."""
    if obj.type != 'MESH' or not obj.data.shape_keys:
        return False, "Object is not a mesh or has no shape keys."

    shape_keys = obj.data.shape_keys
    key_block = shape_keys.key_blocks.get(key_name)

    if not key_block:
        return False, f"Shape key '{key_name}' not found."

    # Deselect all objects to avoid conflicts
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Add Left shape key
    bpy.ops.object.shape_key_add(from_mix=False)
    right_key = obj.active_shape_key
    right_key.name = f"{key_name}Right"

    # Add Right shape key
    bpy.ops.object.shape_key_add(from_mix=False)
    left_key = obj.active_shape_key
    left_key.name = f"{key_name}Left"

    # Restore original active shape key
    obj.active_shape_key_index = shape_keys.key_blocks.keys().index(key_name)

    for idx, vertex in enumerate(obj.data.vertices):
        original_co = key_block.data[idx].co
        current_co = vertex.co

        # Calculate blend factor (-1 to 1 range, crossing the center)
        blend_factor = current_co.x / blend_zone
        blend_factor = max(-1.0, min(1.0, blend_factor))  # Clamp to valid range

        print(f'x: {current_co.x}, blend_factor: {blend_factor}')

        if blend_factor == 0:
            left_weight = 0.5
            right_weight = 0.5
        elif blend_factor < 0:
            # More contribution to the left shape
            left_weight = -blend_factor  # Positive weight for left
            right_weight = 1 + blend_factor  # Reduced weight for right
        else:
            # More contribution to the right shape
            left_weight = 1 - blend_factor  # Reduced weight for left
            right_weight = blend_factor  # Positive weight for right

        # Interpolate positions based on weights
        left_key.data[idx].co = original_co.lerp(current_co, left_weight)
        right_key.data[idx].co = original_co.lerp(current_co, right_weight)

    return True, f"Shape key successfully split. {blend_zone}"


class OBJECT_OT_SplitShapeKey(bpy.types.Operator):
    """Split the selected shape key into Left and Right"""
    bl_idname = "object.split_shape_key"
    bl_label = "Split Shape Key Left/Right"
    bl_options = {'REGISTER', 'UNDO'}

    # Add a modifiable property for the blend zone
    blend_zone: bpy.props.FloatProperty(
        name="Blend Zone",
        description="Width of the zone near the center where vertices are blended",
        default=0.01,
        min=0.0,
        soft_max=0.1,
        step=0.001,
        precision=4
    )

    def execute(self, context):
        obj = context.object
        shape_key_name = obj.active_shape_key.name if obj.active_shape_key else None

        if not shape_key_name:
            self.report({'ERROR'}, "No active shape key selected.")
            return {'CANCELLED'}

        success, message = split_shape_key(obj, shape_key_name, self.blend_zone)
        if not success:
            self.report({'ERROR'}, message)
            return {'CANCELLED'}

        self.report({'INFO'}, message)
        return {'FINISHED'}

    def invoke(self, context, event):
        """Invoke method to initialize properties when the operator is called."""
        return context.window_manager.invoke_props_dialog(self)


def menu_func(self, context):
    self.layout.separator()
    self.layout.operator(OBJECT_OT_SplitShapeKey.bl_idname, icon='MODIFIER')


def register():
    bpy.utils.register_class(OBJECT_OT_SplitShapeKey)
    bpy.types.MESH_MT_shape_key_context_menu.append(menu_func)


def unregister():
    bpy.types.MESH_MT_shape_key_context_menu.remove(menu_func)
    bpy.utils.unregister_class(OBJECT_OT_SplitShapeKey)
