# Friendly_ModuleNotFoundError


<img width="1481" height="760" alt="Windows PowerShell 2025_8_10 21_54_12" src="https://github.com/user-attachments/assets/29f81573-3784-4d44-b75f-4bd1c518727b" />

## What it is doing?

It is to grade the message of the `ModuleNotFoundError`. 

## Usage

<del>To compile the project, it is better to define the marco below:</del>

- <del>PYTHON_STD_PATH: The path of the python standard librarys.</del>
- <del>PYTHON_SITE_PATH: The path of the python site-packages.</del>
- <del>PY_EXT_PREFIX: The name that `.pyd` or `.so` need.</del>

<del>The project now build on [nanobind](https://nanobind.readthedocs.io/en/latest/). See how to build it.</del>

Now use the python script.

## Now problem

- <del>Whether it can build on any systems</del>
- <del>How to build it in cpython and how to initlizate the builtins-modules.</del>
- <del>How to make it give exactly idea.</del>

## Rejected suggestion

- Build a cache for site-packages when install: The code runs fast, so it can find all of the packages fast. Before that finding costs, the computer has been almost broken.
- Suggest for "pip install xxx": spell mistakes are often closely associated with homograph attacks. Suggesting for it will help it.
