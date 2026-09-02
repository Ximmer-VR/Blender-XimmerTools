bl_info = {
    "name": "Ximmer's Blender Tools",
    "author": "Ximmer",
    "version": (1, 0, 0),
    "blender": (5, 0, 0),
    "location": "View3D > Sidebar",
    "description": "Collection of modeling and workflow tools",
    "category": "3D View",
}

from . import operators


def register():
    operators.register()


def unregister():
    operators.unregister()


if __name__ == "__main__":
    register()
