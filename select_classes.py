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
#                                                                              #
# The academic career is given via stdin and consists of one course per line   #
# with each field of the course separated by a pipe character. The fields are  #
# as follows:                                                                  #
#                                                                              #
# name|code|taken|prereqs|coreqs|offerpattern|offered                          #
# No field may contain a pipe character as part of its value.                  #
#                                                                              #
# 'name' -- the name of this course. It is used for display purposes only.     #
# 'code' -- a string that uniquely identifies this course. It must not contain #
# commas.                                                                      #
# 'taken' -- indicates whether this course has already been taken. It must be  #
# either "yes" or "no".                                                        #
# 'prereqs' -- a comma-separated list of codes that are courses that must be   #
# taken before this course. Every value must be a code of some course in the   #
# given list.                                                                  #
# 'coreqs' -- identical to 'prereqs' in format. It refers to courses that must #
# be taken at the same time as this course. A course code may appear in both   #
# the 'coreqs' and 'prereqs' sections to indicate that it may be taken either  #
# before or during this course.                                                #
# 'offerpattern' -- a code that identifies how often this course is given.     #
#   1 - every semester                                                         #
#   2 - every fall semester                                                    #
#   3 - every spring semester                                                  #
#   4 - special                                                                #
# The 'special' code indicates unknown or sporadic offering. If the 'special'  #
# code is used and the course is elibale to be taken (prereqs met, and is      #
# offered), the course is given extremely high precedence.                     #
# 'offered' -- indicates whether the course is currently being offered. It     #
# must be either "yes" or "no".                                                #
################################################################################

import sys

COURSE_RECORD_COUNT = 7

def main():
    """Execute the program. Call only if this module is being run from the
    interpreter.
    """
    career = read_acedemic_career()
    semester = select_courses(classes)
    write_semester_courses(semester)

def read_academic_career():
    """Read the academic career from stdin. Return the academic career as a list
    of dekky.schedule.Course instances.
    """
    courses = list()
    input = open(sys.stdin, 'r')
    for line in input:
        c = parse_course(line.rstrip('\r\n')
        if c is not None:
            courses.append(c)
    return courses
    
def parse_course(course_line):
    """Parse a line of course information into a dekky.schedule.Course instance.
    course_line -- the course information to be parsed. Must not contain newline
    character.
    Return the course as an instance of dekky.schedule.Course if it is valid, or
    None if it is not valid.
    """
    parts = course_line.split('|')
    if len(parts) != COURSE_RECORD_COUNT:
        return None
    name = parts[0]
    abbr = parts[1]
    if parts[2] == 'yes':
        taken = True
    elif parts[2] == 'no':
        taken = False
    else:
        return None
    prereqs = parts[3].split(',')
    coreqs = parts[4].split(',')
    pattern = int(parts[5])
    if parts[6] == 'yes':
        offered = True
    elif parts[6] == 'no':
        offered = False
    else:
        return None
    
    

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        pass #simply exit; do not barf all over the console