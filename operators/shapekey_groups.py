import bpy


GROUP_PREFIX = "==="

# Group names to exclude (case-insensitive, without ===)
EXCLUDED_GROUPS = {
    "vrc",   # excludes === VRC ===
}


def get_shape_key_headers(obj):
    keys = obj.data.shape_keys
    if not keys:
        return []

    return [
        kb for kb in keys.key_blocks
        if kb.name.startswith(GROUP_PREFIX)
    ]


class OBJECT_OT_move_shape_key_to_group(bpy.types.Operator):
    bl_idname = "object.move_shape_key_to_group"
    bl_label = "Move Shape Key To Group"
    bl_options = {'UNDO'}

    target_group: bpy.props.StringProperty()

    def execute(self, context):
        obj = context.object
        keys = obj.data.shape_keys

        if not obj or not keys:
            return {'CANCELLED'}

        key_blocks = keys.key_blocks
        active_index = obj.active_shape_key_index
        active_key = key_blocks[active_index]

        # Prevent moving headers
        if active_key.name.startswith(GROUP_PREFIX):
            self.report({'WARNING'}, "Cannot move a group header")
            return {'CANCELLED'}

        # Find target index
        target_index = None
        for i, kb in enumerate(key_blocks):
            if kb.name == self.target_group:
                target_index = i
                break

        if target_index is None:
            return {'CANCELLED'}

        # We want it BELOW the header
        insert_index = target_index + 1

        # Adjust if moving downward
        if active_index < insert_index:
            insert_index -= 1

        # Move shape key using ops
        obj.active_shape_key_index = active_index

        while obj.active_shape_key_index > insert_index:
            bpy.ops.object.shape_key_move(type='UP')

        while obj.active_shape_key_index < insert_index:
            bpy.ops.object.shape_key_move(type='DOWN')

        return {'FINISHED'}


class OBJECT_MT_shape_key_move_group_menu(bpy.types.Menu):
    bl_label = "Move To Shape Group"
    bl_idname = "OBJECT_MT_shape_key_move_group_menu"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        headers = get_shape_key_headers(obj)

        if not headers:
            layout.label(text="No === groups found")
            return

        for header in headers:
            op = layout.operator(
                OBJECT_OT_move_shape_key_to_group.bl_idname,
                text=header.name.replace("===", "").strip()
            )
            op.target_group = header.name


def shape_key_context_menu(self, context):
    layout = self.layout
    obj = context.object

    if not obj or not obj.data.shape_keys:
        return

    active = obj.active_shape_key
    if not active:
        return

    layout.separator()
    layout.menu(OBJECT_MT_shape_key_move_group_menu.bl_idname)

    layout.separator()
    layout.operator(
        OBJECT_OT_sort_shape_key_groups.bl_idname,
        icon='SORTALPHA'
    )

def normalize_group_name(name):
    return name.strip("= ").lower()


def sort_shape_keys_by_groups(obj):
    if not obj or obj.type != 'MESH':
        return False, "Active object is not a mesh"

    shape_keys = obj.data.shape_keys
    if not shape_keys:
        return False, "Object has no shape keys"

    key_blocks = shape_keys.key_blocks

    # Basis always stays first
    keys = list(key_blocks)[1:]

    result = []
    current_group = []
    current_group_name = None
    sort_current_group = False

    def flush_group():
        nonlocal current_group
        if not current_group:
            return

        if sort_current_group:
            current_group.sort(key=lambda k: k.name.lower())

        result.extend(current_group)
        current_group.clear()

    for key in keys:
        if key.name.startswith(GROUP_PREFIX):
            flush_group()

            current_group_name = normalize_group_name(key.name)
            sort_current_group = current_group_name not in EXCLUDED_GROUPS

            result.append(key)
        else:
            if current_group_name is not None:
                current_group.append(key)
            else:
                result.append(key)

    flush_group()

    # Apply new order in Blender
    for target_index, key in enumerate(result, start=1):
        current_index = key_blocks.find(key.name)
        if current_index != target_index:
            obj.active_shape_key_index = current_index
            bpy.ops.object.shape_key_move(type='TOP')
            for _ in range(target_index - 1):
                bpy.ops.object.shape_key_move(type='DOWN')

    return True, "Shape keys sorted"


class OBJECT_OT_sort_shape_key_groups(bpy.types.Operator):
    bl_idname = "object.sort_shape_key_groups"
    bl_label = "Sort Shape Key Groups"
    bl_description = "Sort shape keys inside === groups (with exclusions)"
    bl_options = {'UNDO'}

    def execute(self, context):
        obj = context.object
        ok, msg = sort_shape_keys_by_groups(obj)

        if ok:
            self.report({'INFO'}, msg)
            return {'FINISHED'}
        else:
            self.report({'WARNING'}, msg)
            return {'CANCELLED'}

classes = (
    OBJECT_OT_move_shape_key_to_group,
    OBJECT_MT_shape_key_move_group_menu,
    OBJECT_OT_sort_shape_key_groups,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.MESH_MT_shape_key_context_menu.append(shape_key_context_menu)


def unregister():
    bpy.types.MESH_MT_shape_key_context_menu.remove(shape_key_context_menu)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
