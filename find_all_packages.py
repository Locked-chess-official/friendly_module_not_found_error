import os
import sys
from importlib import machinery

def scan_dir(path):
    """
    Return all of the packages in the path without import
    contains：
      - .py file
      - directory with "__init__.py"
      - the .pyd/so file that has right ABI
    """
    if not os.path.isdir(path):
        return []

    suffixes = machinery.EXTENSION_SUFFIXES
    result = []

    for name in os.listdir(path):
        full_path = os.path.join(path, name)

        # .py file
        if name.endswith(".py") and os.path.isfile(full_path):
            modname = name[:-3]
            if modname.isidentifier():
                result.append(modname)

        # directory with "__init__.py"
        elif os.path.isdir(full_path):
            init_file = os.path.join(full_path, "__init__.py")
            if os.path.isfile(init_file) and name.isidentifier():
                result.append(name)

        # the .pyd/so file that has right ABI
        elif os.path.isfile(full_path):
            for suf in suffixes:
                if name.endswith(suf):
                    modname = name[:-len(suf)]
                    if modname.isidentifier():
                        result.append(modname)
                    break

    return sorted(result)

def find_all_packages():
    return sorted(sum([scan_dir(i) if i and
                isinstance(i, str) and not
                i.endswith("idlelib") else []
                for i in sys.path ], []) + 
                list(sys.builtin_module_names))

# example
if __name__ == "__main__":
    import timeit
    print(timeit.timeit("find_all_packages()", globals=globals(), number=1000))
