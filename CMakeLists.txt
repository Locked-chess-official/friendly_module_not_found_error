cmake_minimum_required(VERSION 3.15...3.27)
project(find_all_packages)

if (CMAKE_VERSION VERSION_LESS 3.18)
  set(DEV_MODULE Development)
else()
  set(DEV_MODULE Development.Module)
endif()

find_package(Python 3.8 COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# 这里建议放早一点，防止被覆盖
set(CMAKE_BUILD_TYPE Debug)

execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)

find_package(nanobind CONFIG REQUIRED)

set(SOURCE 
    find_all_packages.cpp
    find_all_packages.c
    )

add_definitions(-DNB_ENABLE_DOCSTRINGS=1)



nanobind_add_module(find_all_packages NOMINSIZE ${SOURCE})
target_compile_definitions(find_all_packages PRIVATE
    PYTHON_STD_PATH="\\\"C:/Users/hh180/AppData/Local/Programs/Python/Python313/Lib\\\""
    PYTHON_SITE_PATH="\\\"C:/Users/hh180/AppData/Local/Programs/Python/Python313/Lib/site-packages\\\""
    PY_EXT_PREFIX="\\\".cp313-win_amd64\\\""
)