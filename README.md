# friendly_module_not_found_error

<img width="1481" height="760" alt="Windows PowerShell 2025_8_10 21_54_12" src="https://github.com/user-attachments/assets/29f81573-3784-4d44-b75f-4bd1c518727b" />

This is a Python package that provides a custom exception class for handling module not found errors in a friendly way.

## Installation

To install the package, run the following command:

```cmd/bash
pip install friendly_module_not_found_error
```

## Usage

Don't need to import the packages. The pth file is already in the site-packages folder.
Any using for the module in your programs are undocumental behavior(UB).

You can use the code to test the effects of the package:

```python
import ant
```

The message raised will change to : "No module named 'ant'. Did you mean 'ast'?"
The suggestion may be change according to the package you have installed.

```python
import multiprocessing.dumy
```

The message raised will change to : "module 'multiprocessing' has no child module 'dumy'. Did you mean 'dummy'?"

You can also run "testmodule" to test the effects of the python.

## Effect and explain

The example:

```python
import xxx.yyy.zzz
```

If "xxx" not exist, the message is:
"**No module named 'xxx'**"
If "xxx" exist but "yyy" not exist, the message is:
"**module 'xxx' has no child module 'yyy'**"
Then the message add like the text below:
The final name will be compared to all module at that path. If at the top, it first compared with stdlib and then compared with the path in `sys.path`. Or, if the module before is not a package and the now module not exist, the message will add "module '...' is not a package". For the non-package module, it won't support for this condition: module has a child module, and it has child module. For package, it will scan the attribute `__path__` to get all possible child module to compare.

The change can clearly show the specific error in import and give the near name suggestion. For example, the original is "No module named 'xxx.yyy.zzz'", we cannot get message that which step is wrong, now we can see which step is wrong:
"No module named 'xxx'" means the top, "module 'xxx' has no child module 'yyy'" means the second, and ''module 'xxx.yyy' has no child module 'zzz'" means the third, and so on. And like `NameError` and `AttributeError`, it will suggest the possible name.

## require

python3.7+

In friendly_module_not_found_error verison 0.4.2, it supports python3.7+.

## License

This package is licensed under the MIT License. See the LICENSE file for more information.

## issues

If you have any questions or suggestions, please open an [issue](https://github.com/Locked-chess-official/friendly_module_not_found_error/issues) on GitHub.

## Contributing

Contributions are welcome! Please submit a [pull request](https://github.com/Locked-chess-official/friendly_module_not_found_error/pulls) with your changes.

## data

The test for "\_\_main\_\_.py" here:

| No. | number of entries | used time(/s) | average time(/s) | result |
|-- | -- | -- | -- | -- |
| 1 | 5 | 0.064 | 0.013 | success |
| 2 | 5 | 0.072 | 0.014 | success |
| 3 | 5 | 0.052 | 0.010 | success |
| 4 | 5 | 0.056 | 0.011 | success |
| 5 | 5 | 0.057 | 0.011 | success |
| 6 | 6 | 0.081 | 0.014 | success |
| 7 | 6 | 0.062 | 0.010 | success |
| 8 | 6 | 0.091 | 0.015 | success |
| 9 | 6 | 0.064 | 0.011 | success |
| 10 | 6 | 0.064 | 0.011 | success |

The speed test here:

| tool | function | arg | number | average time(/ms) |
| -- | -- | -- | -- | -- |
| timeit | find_all_packages | (no args) | 1000 | 8.567 |
| timeit | scan_dir | path/to/site-packages | 1000 | 4.845 |

## Note

If a module that is not a package contains submodules, and those submodules also contain their own submodules, this nested module structure is not supported.
When this situation occurs, you should reorganize the code using proper package structure. This approach violates Python's packaging best practices and should be avoided.

To make your custom import hook be supported, you need to define a magic method `__find__` to return the list of all modules.
For example:

```python
class MyImportHook:
    def __find__(self, name: str=None) -> list[str]:
        """
        Return a list of all modules that are available to the import hook without import them.
        If the "name" is provided, the method should return a list of all submodules that under the module named "name".
        parameter name: The name of the module to find submodules for. If None, return all top modules.
        """
        return []
```

The `__find__` method should return a list of all modules that are available to the import hook without import them.
If the "name" is provided, the method should return a list of all submodules that under the module named "name". Or it needs to return all top modules if the "name" is None.

## Rejected suggestion

- Build a cache for site-packages when install: The code runs fast, so it can find all of the packages fast. Before that finding costs, the computer has been almost broken.
- Suggest for "pip install xxx": spell mistakes are often closely associated with homograph attacks. Suggesting for it will help it.

## Credits

This package was created by Locked-chess-official and is maintained by Locked-chess-official
