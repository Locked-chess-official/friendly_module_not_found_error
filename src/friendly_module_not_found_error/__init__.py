from .handle_path import scan_dir, find_in_path
import sys
import traceback
import importlib
from .traceback_change import original_traceback_TracebackException_init, remove_stack
from .runpy_change import original_runpy_get_module_details
from .idlelib_all_change import original_idlelib_run_print_exception

major, minor = sys.version_info[:2]
_ERR_MSG_PREFIX = 'No module named '
_CHILD_ERR_MSG = 'module {!r} has no child module {!r}'

def _find_and_load_unlocked(name, import_):
    path = None
    parent, _, child = name.rpartition('.')
    parent_spec = None
    if parent:
        if parent not in sys.modules:
            importlib._bootstrap._call_with_frames_removed(import_, parent)
        # Crazy side-effects!
        module = sys.modules.get(name)
        if module is not None:
            return module
        parent_module = sys.modules[parent]
        try:
            path = parent_module.__path__
        except AttributeError:
            msg = _CHILD_ERR_MSG.format(parent, child) + f'; {parent!r} is not a package'
            raise ModuleNotFoundError(msg, name=name) from None
        parent_spec = parent_module.__spec__
        if getattr(parent_spec, '_initializing', False):
            importlib._bootstrap._call_with_frames_removed(import_, parent)
        # Crazy side-effects (again)!
        module = sys.modules.get(name)
        if module is not None:
            return module
    spec = importlib._bootstrap._find_spec(name, path)
    if spec is None:
        if not parent:
            msg = f'{_ERR_MSG_PREFIX}{name!r}'
        else:
            msg = _CHILD_ERR_MSG.format(parent, child)
        raise ModuleNotFoundError(msg, name=name)
    else:
        if parent_spec:
            # Temporarily add child we are currently importing to parent's
            # _uninitialized_submodules for circular import tracking.
            parent_spec._uninitialized_submodules.append(child)
        try:
            module = importlib._bootstrap._load_unlocked(spec)
        finally:
            if parent_spec:
                parent_spec._uninitialized_submodules.pop()
    if parent:
        # Set the module as an attribute on its parent.
        parent_module = sys.modules[parent]
        try:
            setattr(parent_module, child, module)
        except AttributeError:
            msg = f"Cannot set an attribute on {parent!r} for child module {child!r}"
            _warnings.warn(msg, ImportWarning)
    return module

importlib._bootstrap._find_and_load_unlocked = _find_and_load_unlocked
importlib._bootstrap.BuiltinImporter.__find__ = staticmethod(lambda name=None: (sorted(sys.builtin_module_names) if not name else []))
original_sys_excepthook = sys.__excepthook__

def excepthook(exc_type, exc_value, exc_tb):
    tb_exception = traceback.TracebackException(
        exc_type, exc_value, exc_tb, capture_locals=False
    )

    for line in tb_exception.format():
        sys.stderr.write(line)
sys.excepthook = sys.__excepthook__ = excepthook
if minor >= 13:
    from _pyrepl.console import InteractiveColoredConsole
    def _excepthook(self, exc_type, exc_value, exc_tb):
        tb_exception = traceback.TracebackException(
            exc_type, exc_value, exc_tb, capture_locals=False,
            limit=traceback.BUILTIN_EXCEPTION_LIMIT
        )

        for line in tb_exception.format(colorize=self.can_colorize):
            self.write(line)
    InteractiveColoredConsole._excepthook = _excepthook

