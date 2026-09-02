import bpy
from bpy.types import Operator


EPSILON = 1e-6


def shape_key_affects_mesh(shape_key, basis_key):
    for v_sk, v_basis in zip(shape_key.data, basis_key.data):
        if (v_sk.co - v_basis.co).length > EPSILON:
            return True
    return False


class OBJECT_OT_remove_unused_shape_keys(Operator):
    bl_idname = "object.remove_unused_shape_keys"
    bl_label = "Remove Unused Shape Keys"
    bl_description = "Delete shape keys that don't move any vertices"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object

        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object")
            return {'CANCELLED'}

        if not obj.data.shape_keys or not obj.data.shape_keys.key_blocks:
            self.report({'ERROR'}, "No shape keys found")
            return {'CANCELLED'}

        key_blocks = obj.data.shape_keys.key_blocks
        basis = key_blocks[0]

        keys_to_remove = []

        for sk in key_blocks[1:]:  # Skip Basis
            if sk.name.startswith("==="):
                continue

            if not shape_key_affects_mesh(sk, basis):
                keys_to_remove.append(sk)

        for sk in reversed(keys_to_remove):
            self.report({'INFO'}, f"Removing shape key: {sk.name}")
            obj.shape_key_remove(sk)

        self.report({'INFO'}, f"Removed {len(keys_to_remove)} unused shape keys")
        return {'FINISHED'}


def draw_shape_key_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(
        OBJECT_OT_remove_unused_shape_keys.bl_idname,
        icon='SHAPEKEY_DATA'
    )


classes = (
    OBJECT_OT_remove_unused_shape_keys,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.MESH_MT_shape_key_context_menu.append(draw_shape_key_menu)


def unregister():
    bpy.types.MESH_MT_shape_key_context_menu.remove(draw_shape_key_menu)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
