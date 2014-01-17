__author__ = 'root'

from pkg_resources import working_set, get_entry_map

# the working set itself is the iter for the package list
for entry in working_set:
    print get_entry_map(entry)