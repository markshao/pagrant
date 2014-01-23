__author__ = 'root'

from pkg_resources import load_entry_point

# the working set itself is the iter for the package list
# for entry in working_set:
#     print get_entry_map(entry)

print load_entry_point("lxc", "PAGRANT", "VMPROVIDER_INFO")()

