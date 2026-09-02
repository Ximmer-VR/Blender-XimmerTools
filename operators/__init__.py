from . import shapekey_groups
from . import shapekey_sets
from . import shapekey_remove_unused
from . import shapekey_split


modules = [
    shapekey_groups,
    shapekey_sets,
    shapekey_remove_unused,
    shapekey_split,
]


def register():
    for m in modules:
        m.register()


def unregister():
    for m in reversed(modules):
        m.unregister()
