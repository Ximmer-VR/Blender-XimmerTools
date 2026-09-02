from . import shapekey_groups
from . import shapekey_sets


modules = [
    shapekey_groups,
    shapekey_sets,
]


def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()
