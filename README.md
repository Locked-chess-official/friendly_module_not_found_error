# Friendly_ModuleNotFoundError


<img width="1481" height="760" alt="Windows PowerShell 2025_8_10 21_54_12" src="https://github.com/user-attachments/assets/29f81573-3784-4d44-b75f-4bd1c518727b" />

## What it is doing?

It is to grade the message of the `ModuleNotFoundError`. 

## Compare
The original message is : "No module named 'xxx.yyy.zzz'".
After its effect: 
- If module "xxx" is not exist, it changes to "No module named 'xxx'" and give the nearly name if it exist.
- If module "xxx" is exist but "yyy" not, it changes to "module 'xxx' has no child module 'yyy'" and give the nearly name if it exist.
- The next is same as above.
- If one module existed in the name is not a package, it will add the information in the message.

## Usage

<del>To compile the project, it is better to define the marco below:</del>

- <del>PYTHON_STD_PATH: The path of the python standard librarys.</del>
- <del>PYTHON_SITE_PATH: The path of the python site-packages.</del>
- <del>PY_EXT_PREFIX: The name that `.pyd` or `.so` need.</del>

<del>The project now build on [nanobind](https://nanobind.readthedocs.io/en/latest/). See how to build it.</del>

Now use the python script. The "traceback-3.x-final.py" is the final result now.

⚠️Warning: If you want to change the traceback.py in your python environment, please save the file. If the file went wrong, you can recovery and open an issue here.

## data

The test for "test.py" here:

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

## Effect and explain

The example:
```
import xxx.yyy.zzz
```
If "xxx" not exist, the message is:
"No module named 'xxx'"
If "xxx" exist but "yyy" not exist, the message is:
"module 'xxx' has no child module 'yyy'"
Then the message add like the text below:
The final name will be compared to all module at that path. If at the top, it first compared with stdlib and then compared with the path in `sys.path`. Or, if the module before is not a package and the now module not exist, the message will add "module '...' is not a package". For the non-package module, it won't support for this condition: module has a child module, and it has child module. For package, it will scan the attribute `__path__` to get all possible child module to compare.

The change can clearly show the specific error in import and give the near name suggestion. For example, the original is "No module named 'xxx.yyy.zzz'", we cannot get message that which step is wrong, now we can see which step is wrong:
"No module named 'xxx'" means the top, "module 'xxx' has no child module 'yyy'" means the second, and ''module 'xxx.yyy' has no child module 'zzz'" means the third, and so on. And like `NameError` and `AttributeError`, it will suggest the possible name.

## Now problem

- <del>Whether it can build on any systems</del>
- <del>How to build it in cpython and how to initlizate the builtins-modules.</del>
- <del>How to make it give exactly idea.</del>

## Rejected suggestion

- Build a cache for site-packages when install: The code runs fast, so it can find all of the packages fast. Before that finding costs, the computer has been almost broken.
- Suggest for "pip install xxx": spell mistakes are often closely associated with homograph attacks. Suggesting for it will help it.
