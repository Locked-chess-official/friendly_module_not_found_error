import traceback
import unittest

class ExceptionTest(unittest.TestCase):
    def test_exception(self):
        import_error_tuple = (
            ("import ant", ModuleNotFoundError, "No module named 'ant'. Did you mean: 'ast'?"),
            ("import multiprocessing.dumy", ModuleNotFoundError, "module 'multiprocessing' has no child module 'dumy'. Did you mean: 'dummy'?"),
            ("import wrong_module", ModuleNotFoundError, "module 'wrong_module' has no child module 'wrong_module'"),
            ("import wrong_child_module", ModuleNotFoundError, "module 'wrong_child_module.wrong_child_module' has no child module 'wrong_child_module'. Did you mean: 'wrong_child_modules'?")
        )
        for i in import_error_tuple:
            if i:
                self.check_message(i[0], i[1], i[2])

    def check_message(self, code, exc_type, exc_msg):
        try:
            exec(code)
        except exc_type:
            self.assertIn(exc_msg, traceback.format_exc())

if __name__ == '__main__':
    unittest.main()
