from .handle_path import scan_dir, find_in_path
import sys
import traceback
import importlib
from .traceback_change import original_traceback_TracebackException_init, remove_stack
from .runpy_change import original_runpy_get_module_details
from .idlelib_all_change import original_idlelib_run_print_exception
from .importlib_change import original_find_and_load_unlocked

major, minor = sys.version_info[:2]
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

