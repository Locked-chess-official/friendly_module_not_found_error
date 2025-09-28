from .handle_path import scan_dir, find_in_path
import sys
import traceback
import importlib
import builtins
from .traceback_change import original_traceback_TracebackException_init
from .runpy_change import original_runpy_get_module_details
from .idlelib_all_change import original_idlelib_run_print_exception

major, minor = sys.version_info[:2]

original_import = builtins.__import__
_CHILD_ERR_MSG = 'module {!r} has no child module {!r}'
def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
    try:
        return original_import(name,
                               globals=globals,
                               locals=locals,
                               fromlist=fromlist,
                               level=level)
    except ModuleNotFoundError as e:
        if " halted; None in sys.modules" not in e.msg:
            parent, _, child = e.name.rpartition('.')            
            if parent:
                original_msg = e.msg
                e.msg = _CHILD_ERR_MSG.format(parent, child)
                if original_msg.endswith("is not a package"):
                    e.msg += f'; {parent!r} is not a package'
                e.args = (e.msg,)
        raise

builtins.__import__ = custom_import
importlib._bootstrap.BuiltinImporter.__find__ = staticmethod(lambda name=None: (sorted(sys.builtin_module_names) if not name else []))
original_sys_excepthook = sys.__excepthook__


def excepthook(exc_type, exc_value, exc_tb):
    tb_exception = traceback.TracebackException(
        exc_type, exc_value, exc_tb, capture_locals=False
    )

    frames = [frame for frame in tb_exception.stack
              if "friendly_module_not_found_error" not in frame.filename]
    
    tb_exception.stack = traceback.StackSummary.from_list(frames)

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

        frames = [frame for frame in tb_exception.stack
                  if "friendly_module_not_found_error" not in frame.filename]
        
        tb_exception.stack = traceback.StackSummary.from_list(frames)

        for line in tb_exception.format(colorize=self.can_colorize):
            self.write(line)
    InteractiveColoredConsole._excepthook = _excepthook

