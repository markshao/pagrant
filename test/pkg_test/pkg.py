__author__ = 'root'

from pkg_resources import working_set

# the working set itself is the iter for the package list
for entry in working_set:
    print entry