"""Interactive console utilities."""
import code


def interact():
    """Start an interactive Python console."""
    code.InteractiveConsole(locals=globals()).interact()
