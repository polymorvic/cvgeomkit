_DEBUG_MODE = False


def set_debug_mode(mode: bool) -> None:
    """Enable or disable debug mode."""
    global _DEBUG_MODE
    _DEBUG_MODE = mode


def get_debug_mode() -> bool:
    """Check if debug mode is enabled."""
    global _DEBUG_MODE
    return _DEBUG_MODE
