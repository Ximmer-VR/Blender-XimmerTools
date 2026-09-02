bl_info = {
    "name": "Add Shape Set",
    "author": "Ximmer",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "Object > Add Shape Set",
    "description": "Add predefined blendshape sets to the selected object",
    "category": "Object",
}

import bpy

SHAPES_VRC_VISEMES = [
    "=== VRC Visemes ===",
    "vrc/sil",
    "vrc/PP",
    "vrc/FF",
    "vrc/TH",
    "vrc/DD",
    "vrc/kk",
    "vrc/CH",
    "vrc/SS",
    "vrc/nn",
    "vrc/RR",
    "vrc/aa",
    "vrc/E",
    "vrc/ih",
    "vrc/oh",
    "vrc/ou",
]

SHAPES_UNIFIED_EXPRESSIONS = [

    "=== Unified Expressions L/R Bases Remove ===",

    "BrowDown",         # L/R
    "BrowInnerUp",      # L/R
    "BrowOuterUp",      # L/R
    "CheekPuff",        # L/R
    "CheekSquint",      # L/R
    "CheekSuck",        # L/R
    "EyeClosed",        # L/R
    "EyeLookDown",      # L/R
    "EyeLookIn",        # L/R
    "EyeLookOut",       # L/R
    "EyeLookUp",        # L/R
    "EyeSquint",        # L/R
    "EyeWide",          # L/R
    "MouthDimple",      # L/R
    "MouthDimple",      # L/R
    "MouthFrown",       # L/R
    "MouthPress",       # L/R
    "MouthSmile",       # L/R
    "MouthStretch",     # L/R
    "MouthTightener",   # L/R
    "MouthUpperUp",     # L/R

    "=== Unified Expressions L/R Mirror ===",

    "Jaw",              # L/R Mirror
    "Mouth",            # L/R Mirror

    "=== Unified Expressions L/R Bases Keep ===",

    "MouthPress",       # L/R
    "MouthLowerDown",   # L/R
    "NoseSneer",        # L/R

    "=== Unified Expressions ===",

    "EyeConstrict",
    "EyeDilation",
    "JawForward",
    "JawOpen",
    "LipFunnel",
    "LipPucker",
    "LipSuckLower",
    "LipSuckUpper",
    "MouthClosed",
    "MouthRaiserLower",
    "MouthRaiserUpper",
    "TongueDown",
    "TongueDownLeftMorph",
    "TongueDownRightMorph",
    "TongueLeft",
    "TongueOut",
    "TongueRight",
    "TongueUp",
    "TongueUpLeftMorph",
    "TongueUpRightMorph",

]

SHAPES_ARKIT = [
    "browDown",
    "browInnerUp",
    "browOuterUp",
    "eyeBlink",
    "eyeLookDown",
    "eyeLookIn",
    "eyeLookOut",
    "eyeLookUp",
    "eyeSquint",
    "eyeWide",
    "jawForward",
    "jaw",
    "jawOpen",
    "mouthClose",
    "mouthFunnel",
    "mouthPucker",
    "mouth",
    "mouthSmile",
    "mouthFrown",
    "mouthDimple",
    "mouthStretch",
    "mouthRollLower",
    "mouthRollUpper",
    "mouthShrugLower",
    "mouthShrugUpper",
    "mouthPress",
    "mouthLowerDown",
    "mouthUpperUp",
    "cheekPuff",
    "cheekSquint",
    "noseSneer",
]

SHAPES_SRANIPAL = [
    "Eye_Right_Look_Up",
    "Eye_Right_Look_Down",
    "Eye_Right_Left",
    "Eye_Right_Right",
    "Eye_Left_Look_Up",
    "Eye_Left_Look_Down",
    "Eye_Left_Right",
    "Eye_Left_Left",
    "Eye_Right_Blink",
    "Eye_Left_Blink",
    "Eye_Right_squeeze",
    "Eye_Left_squeeze",
    "Eye_Right_Wide",
    "Eye_Left_Wide",
    "Eye_Right_Dilation",
    "Eye_Left_Dilation",
    "Eye_Right_Constrict",
    "Eye_Left_Constrict",
    "Cheek_Puff_Right",
    "Cheek_Puff_Left",
    "Cheek_Suck",
    "Jaw_Open",
    "Mouth_Ape_Shape",
    "Jaw_Right",
    "Jaw_Left",
    "Jaw_Forward",
    "Mouth_Upper_Inside",
    "Mouth_Lower_Inside",
    "Mouth_Upper_Overturn",
    "Mouth_Lower_Overturn",
    "Mouth_Pout",
    "Mouth_Upper_Up_Right",
    "Mouth_Upper_Up_Left",
    "Mouth_Lower_Down_Right",
    "Mouth_Lower_Down_Left",
    "Mouth_Smile_Right",
    "Mouth_Smile_Left",
    "Mouth_Sad_Right",
    "Mouth_Sad_Left",
    "Mouth_Lower_Overlay",
    "Tongue_LongStep1 Tongue_LongStep2",
    "Tongue_Up",
    "Tongue_Down",
    "Tongue_Right",
    "Tongue_Left",
    "Tongue_Roll",
]

SHAPES = {
    "ARKit": SHAPES_ARKIT,
    "SRanipal": SHAPES_SRANIPAL,
    "Unified Expressions": SHAPES_UNIFIED_EXPRESSIONS,
    "VRC Visemes": SHAPES_VRC_VISEMES,
}


UE_TO_ARKIT = {
    "SetName": "ARKit",
    "browDownLeft":         {"BrowDownLeft": 1.0},
    "browDownRight":        {"BrowDownRight": 1.0},
    "browInnerUp":          {"BrowInnerUp": 1.0},
    "browOuterUpLeft":      {"BrowOuterUpLeft": 1.0},
    "browOuterUpRight":     {"BrowOuterUpRight": 1.0},
    "eyeBlinkLeft":         {"EyeClosedLeft": 1.0},
    "eyeBlinkRight":        {"EyeClosedRight": 1.0},
    "eyeLookDownLeft":      {"EyeLookDownLeft": 1.0},
    "eyeLookDownRight":     {"EyeLookDownRight": 1.0},
    "eyeLookInLeft":        {"EyeLookInLeft": 1.0},
    "eyeLookInRight":       {"EyeLookInRight": 1.0},
    "eyeLookOutLeft":       {"EyeLookOutLeft": 1.0},
    "eyeLookOutRight":      {"EyeLookOutRight": 1.0},
    "eyeLookUpLeft":        {"EyeLookUpLeft": 1.0},
    "eyeLookUpRight":       {"EyeLookUpRight": 1.0},
    "eyeSquintLeft":        {"EyeSquintLeft": 1.0},
    "eyeSquintRight":       {"EyeSquintRight": 1.0},
    "eyeWideLeft":          {"EyeWideLeft": 1.0},
    "eyeWideRight":         {"EyeWideRight": 1.0},
    "jawForward":           {"JawForward": 1.0},
    "jawLeft":              {"JawLeft": 1.0},
    "jawRight":             {"JawRight": 1.0},
    "jawOpen":              {"JawOpen": 1.0},
    "mouthClose":           {"MouthClosed": 1.0},
    "mouthFunnel":          {"LipFunnel": 1.0},
    "mouthPucker":          {"LipPucker": 1.0},
    "mouthLeft":            {"MouthLeft": 1.0},
    "mouthRight":           {"MouthRight": 1.0},
    "mouthSmileLeft":       {"MouthSmileLeft": 1.0},
    "mouthSmileRight":      {"MouthSmileRight": 1.0},
    "mouthFrownLeft":       {"MouthFrownLeft": 1.0},
    "mouthFrownRight":      {"MouthFrownRight": 1.0},
    "mouthDimpleLeft":      {"MouthDimpleLeft": 1.0},
    "mouthDimpleRight":     {"MouthDimpleRight": 1.0},
    "mouthStretchLeft":     {"MouthStretchLeft": 1.0},
    "mouthStretchRight":    {"MouthStretchRight": 1.0},
    "mouthRollLower":       {"LipSuckLower": 1.0},
    "mouthRollUpper":       {"LipSuckUpper": 1.0},
    "mouthShrugLower":      {"MouthRaiserLower": 1.0},
    "mouthShrugUpper":      {"MouthRaiserUpper": 1.0},
    "mouthPressLeft":       {"MouthPressLeft": 1.0},
    "mouthPressRight":      {"MouthPressRight": 1.0},
    "mouthLowerDownLeft":   {"MouthLowerDownLeft": 1.0},
    "mouthLowerDownRight":  {"MouthLowerDownRight": 1.0},
    "mouthUpperUpLeft":     {"MouthUpperUpLeft": 1.0},
    "mouthUpperUpRight":    {"MouthUpperUpRight": 1.0},
    "cheekPuff":            {"CheekPuff": 1.0},
    "cheekSquintLeft":      {"CheekSquintLeft": 1.0},
    "cheekSquintRight":     {"CheekSquintRight": 1.0},
    "noseSneerLeft":        {"NoseSneerLeft": 1.0},
    "noseSneerRight":       {"NoseSneerRight": 1.0},

}

UE_TO_SRANIPAL = {
    "SetName": "SRanipal",
    "Eye_Right_Look_Up":        {"EyeLookUpRight": 1.0},
    "Eye_Right_Look_Down":      {"EyeLookDownRight": 1.0},
    "Eye_Right_Left":           {"EyeLookInRight": 1.0},
    "Eye_Right_Right":          {"EyeLookOutRight": 1.0},
    "Eye_Left_Look_Up":         {"EyeLookUpLeft": 1.0},
    "Eye_Left_Look_Down":       {"EyeLookDownLeft": 1.0},
    "Eye_Left_Right":           {"EyeLookInLeft": 1.0},
    "Eye_Left_Left":            {"EyeLookOutLeft": 1.0},
    "Eye_Right_Blink":          {"EyeClosedRight": 1.0},
    "Eye_Left_Blink":           {"EyeClosedLeft": 1.0},
    "Eye_Right_squeeze":        {"BrowDownRight": 1.0, "CheekSquintRight": 1.0, "EyeSquintRight": 1.0},
    "Eye_Left_squeeze":         {"BrowDownLeft": 1.0, "CheekSquintLeft": 1.0, "EyeSquintLeft": 1.0},
    "Eye_Right_Wide":           {"EyeWideRight": 1.0},
    "Eye_Left_Wide":            {"EyeWideLeft": 1.0},
    "Eye_Right_Dilation":       {"EyeDilationRight": 1.0},
    "Eye_Left_Dilation":        {"EyeDilationLeft": 1.0},
    "Eye_Right_Constrict":      {"EyeConstrictRight": 1.0},
    "Eye_Left_Constrict":       {"EyeConstrictLeft": 1.0},
    "Cheek_Puff_Right":         {"CheekPuffRight": 1.0},
    "Cheek_Puff_Left":          {"CheekPuffLeft": 1.0},
    "Cheek_Suck":               {"CheekSuck": 1.0},
    "Jaw_Open":                 {"JawOpen": 1.0},
    "Mouth_Ape_Shape":          {"MouthClosed": 1.0},
    "Jaw_Right":                {"JawRight": 1.0},
    "Jaw_Left":                 {"JawLeft": 1.0},
    "Jaw_Forward":              {"JawForward": 1.0},
    "Mouth_Upper_Inside":       {"LipSuckUpper": 1.0},
    "Mouth_Lower_Inside":       {"LipSuckLower": 1.0},
    "Mouth_Upper_Overturn":     {"LipFunnelUpper": 1.0},
    "Mouth_Lower_Overturn":     {"LipFunnelLower": 1.0},
    "Mouth_Pout":               {"LipPucker": 1.0},
    "Mouth_Upper_Up_Right":     {"MouthUpperUpRight": 1.0},
    "Mouth_Upper_Up_Left":      {"MouthUpperUpLeft": 1.0},
    "Mouth_Lower_Down_Right":   {"MouthLowerDownRight": 1.0},
    "Mouth_Lower_Down_Left":    {"MouthLowerDownLeft": 1.0},
    "Mouth_Smile_Right":        {"MouthSmileRight": 1.0},
    "Mouth_Smile_Left":         {"MouthSmileLeft": 1.0},
    "Mouth_Sad_Right":          {"MouthSadRight": 1.0},
    "Mouth_Sad_Left":           {"MouthSadLeft": 1.0},
    "Mouth_Lower_Overlay":      {"MouthRaiserLower": 1.0},
    "Tongue_LongStep1":         {"TongueOut": 1.0},
    "Tongue_LongStep2":         {"TongueOut": 1.0},
    "Tongue_Up":                {"TongueUp": 1.0},
    "Tongue_Down":              {"TongueDown": 1.0},
    "Tongue_Right":             {"TongueRight": 1.0},
    "Tongue_Left":              {"TongueLeft": 1.0},
    "Tongue_Roll":              {"TongueRoll": 1.0},
}

UE_TO_MMD = {
    "SetName": "MMD",

    "あ": {"JawOpen": 1.0},
}

SHAPE_CONVERSIONS = {
    "Unified Expressions → ARKit": UE_TO_ARKIT,
    "Unified Expressions → SRanipal": UE_TO_SRANIPAL,
    "Unified Expressions → MMD": UE_TO_MMD,
}

# ------------------------------------------------------------
#   Operators
# ------------------------------------------------------------

class OBJECT_OT_add_shape_set(bpy.types.Operator):
    """Add a set of shape keys to the active object"""
    bl_idname = "object.add_shape_set"
    bl_label = "Add Shape Set"
    bl_options = {'REGISTER', 'UNDO'}

    set_name: bpy.props.StringProperty()

    def execute(self, context):
        obj = context.object

        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Must have a mesh object selected")
            return {'CANCELLED'}

        # ensure shape keys exist
        if obj.data.shape_keys is None:
            obj.shape_key_add(name="Basis")

        for shape in SHAPES.get(self.set_name, []):
            # avoid dupes
            names = [k.name for k in obj.data.shape_keys.key_blocks]
            if shape not in names:
                obj.shape_key_add(name=shape)

        self.report({'INFO'}, f"Added {self.set_name} shapes")
        return {'FINISHED'}

class OBJECT_OT_convert_shape_set(bpy.types.Operator):
    """Convert shape keys from one set to another"""
    bl_idname = "object.convert_shape_set"
    bl_label = "Convert Shape Set"
    bl_options = {'REGISTER', 'UNDO'}

    conversion_name: bpy.props.StringProperty()

    def execute(self, context):
        obj = context.object

        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "Must have a mesh object selected")
            return {'CANCELLED'}

        if obj.data.shape_keys is None:
            self.report({'ERROR'}, "Object has no shape keys")
            return {'CANCELLED'}

        key_blocks = obj.data.shape_keys.key_blocks
        basis = key_blocks.get("Basis")

        conversion = SHAPE_CONVERSIONS.get(self.conversion_name)
        if not conversion:
            self.report({'ERROR'}, "Unknown conversion")
            return {'CANCELLED'}

        conversion_name = conversion['SetName']

        obj.shape_key_add(name=f'=== {conversion_name} ===', from_mix=False)

        for target_name, sources in conversion.items():

            if target_name == "SetName":
                continue

            # Create target shape if missing
            if target_name not in key_blocks:
                target = obj.shape_key_add(name=target_name, from_mix=False)
            else:
                target = key_blocks[target_name]

            # Reset target to basis
            for i, v in enumerate(target.data):
                v.co = basis.data[i].co.copy()

            # Accumulate weighted deltas
            for source_name, weight in sources.items():
                source = key_blocks.get(source_name)
                if not source:
                    self.report({'WARNING'}, f"Missing source shape: {source_name}")
                    continue

                for i, v in enumerate(target.data):
                    delta = source.data[i].co - basis.data[i].co
                    v.co += delta * weight

        self.report({'INFO'}, f"Converted using {self.conversion_name}")
        return {'FINISHED'}


# ------------------------------------------------------------
#   Menu
# ------------------------------------------------------------

class OBJECT_MT_shape_sets_menu(bpy.types.Menu):
    bl_label = "Add Shape Set"
    bl_idname = "OBJECT_MT_shape_sets_menu"

    def draw(self, context):
        layout = self.layout
        for key in SHAPES.keys():
            op = layout.operator(
                OBJECT_OT_add_shape_set.bl_idname,
                text=key
            )
            op.set_name = key

class OBJECT_MT_shape_conversion_menu(bpy.types.Menu):
    bl_label = "Convert Shape Set"
    bl_idname = "OBJECT_MT_shape_conversion_menu"

    def draw(self, context):
        layout = self.layout
        for key in SHAPE_CONVERSIONS.keys():
            op = layout.operator(
                OBJECT_OT_convert_shape_set.bl_idname,
                text=key
            )
            op.conversion_name = key

def draw_shape_sets_menu(self, context):
    self.layout.separator()
    self.layout.menu(OBJECT_MT_shape_sets_menu.bl_idname)

def draw_shape_conversion_menu(self, context):
    self.layout.menu(OBJECT_MT_shape_conversion_menu.bl_idname)

# ------------------------------------------------------------
#   Registration
# ------------------------------------------------------------

classes = [
    OBJECT_OT_add_shape_set,
    OBJECT_MT_shape_sets_menu,
    OBJECT_OT_convert_shape_set,
    OBJECT_MT_shape_conversion_menu,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.MESH_MT_shape_key_context_menu.append(draw_shape_sets_menu)
    bpy.types.MESH_MT_shape_key_context_menu.append(draw_shape_conversion_menu)
    #bpy.types.VIEW3D_MT_object.append(draw_shape_sets_menu)
    #bpy.types.VIEW3D_MT_object.append(draw_shape_conversion_menu)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    bpy.types.MESH_MT_shape_key_context_menu.remove(draw_shape_sets_menu)
    bpy.types.MESH_MT_shape_key_context_menu.remove(draw_shape_conversion_menu)
    #bpy.types.VIEW3D_MT_object.remove(draw_shape_sets_menu)
    #bpy.types.VIEW3D_MT_object.remove(draw_shape_conversion_menu)
