import traceback
a = ""
b = ""
try:
  import wrong_module
except:
  a = traceback.format_exc()

try:
  import wrong_child_name
except:
  b = traceback.format_exc()

print(a)
print(b)
