#ifndef Find_All_Packages_H
#define Find_All_Packages_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    char **names;
    size_t count;
    size_t capacity;
} ModuleList;

ModuleList* create_module_list(void);
void free_module_list(ModuleList *list);
int add_module_to_list(ModuleList *list, const char *name);
void scan_dir(const char* path, ModuleList *list);
ModuleList* find_all_packages();

#ifdef __cplusplus
}
#endif

#endif // Find_All_Packages_H
