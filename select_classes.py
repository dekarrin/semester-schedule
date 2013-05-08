#!/usr/bin/env python

################################################################################
# select_classes.py                                                            #
# -----------------                                                            #
# Selects classes that should be taken this semester. Classes are selected     #
# based on which classes have already been taken, which classes are availible, #
# and which classes provide the most benefit.                                  #
#                                                                              #
# Prerequisite and Corequisite requirements are taken into account. A class    #
# will not be selected for the semester if the prerequisite requirements are   #
# not fulfilled. In addition, classes that are prerequisites for many other    #
# required classes will be selected before classes are prerequisites for fewer #
# classes.                                                                     #
################################################################################

def main():
    class_data = read_class_data()
    pass

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        pass #simply exit; do not barf all over the console