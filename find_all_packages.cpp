#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include "find_all_packages.h"

namespace nb = nanobind;

NB_MODULE(find_all_packages, m) {
    m.def("find_all_packages", [](){
        ModuleList* list = find_all_packages();
        std::vector<std::string> packages;
        for (int i=0;i < list->count;i++) {
            packages.push_back(list->names[i]);
        }
        return packages;
    });
    m.def("scan_dir", [](std::string& path){
        ModuleList* list = create_module_list();
        scan_dir(path.c_str(), list);
        std::vector<std::string> packages;
        for (int i=0;i < list->count;i++) {
            packages.push_back(list->names[i]);
        }
        return packages;
    });
};