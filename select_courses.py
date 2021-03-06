#!/usr/bin/env python

################################################################################
# select_courses.py                                                            #
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
# INPUT                                                                        #
# -----                                                                        #
# The academic career is given via stdin and consists of one course per line   #
# with each field of the course separated by a pipe character. The fields are  #
# as follows:                                                                  #
#                                                                              #
# name|code|taken|prereqs|coreqs|offerpattern|offered|credits|perm|priority    #
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
# 'credits' -- the number of credits that this course is worth.                #
# 'perm' -- used for indicating that the student recieved special              #
# permission to take this course. If set to "yes", eligibility determination   #
# will be bypassed and the course will be unconditionally eligible. If set to  #
# "no", normal rules of eligibility apply. Must be either "yes" or "no"        #
# 'priority' -- this value is added to the impact score during calculation. If #
# all priority calculation is to be automatic, this must be 0. Otherwise, it   #
# will complement the calculated value. This will not make an otherwise        #
# untakable course takable; that is done with the 'perm' field.                #
#                                                                              #
# OUTPUT                                                                       #
# ------                                                                       #
# The output of the program is a list of course codes that represent the       #
# selected courses. There is one course code per line. Every line, including   #
# the last one, contains on EOL character.                                     #
################################################################################

import sys
import argparse

import dekky.list
import dekky.schedule
import dekky.parse

COURSE_RECORD_COUNT = 10

MIN_CREDS = 12 # TODO: Make this a program parameter
MAX_CREDS = 18 # TODO: Make this a program parameter

def main():
    """Execute the program. Call only if this module is being run from the
    interpreter.
    """
    min_creds, max_creds = read_arguments()
    career = read_academic_career()
    candidates = build_candidate_list(career)
    semester = select_courses(candidates, MIN_CREDS, MAX_CREDS)
    write_semester_courses(semester)

def positive_int(string);
    value = int(string)
    if value < 0:
        
    
def read_arguments():
    """Parse arguments and options."""
    parser = argparse.ArgumentParser(description='Select semester courses.')
    parser.add_argument('-m', '--mincreds', default=MIN_CREDS_DEFAULT,
                        type=int,
                        help='The minimum number of credits in a semester')
    parser.add_argument('-x', '--maxcreds', default=MAX_CRED_DEFAULT,
                        type=int,
                        help='The maximum number of credits in a semester')
    args = parser.parse_args()
    
def read_academic_career():
    """Read the academic career from stdin. Return the academic career as a list
    of course dicts.
    """
    courses = list()
    for line in sys.stdin:
        if line[0] != '#':
            c = parse_course(line.rstrip('\r\n'))
            courses.append(c)
    return courses

def select_courses(candidates, min_credits, max_credits):
    """Choose courses based on how critical they are to the academic career.
    candidates -- the courses that may be selected from.
    min_credits -- the minimum number of credits in a semester.
    max_credits -- the maximum number of credits in a semester.
    Return a list of course codes that represent the selected courses.
    """
    sorted_candidates = sorted(candidates, key=lambda c: c['impact'])
    sorted_candidates.reverse()
    selected = []
    credits = 0
    for c in sorted_candidates:
        if credits + c['credits'] < max_credits:
            selected.append(c)
            credits += c['credits']
    if credits < min_credits:
        raise IndexError("Cannot select courses within the given bounds")
    return selected
    
def build_candidate_list(courses):
    """Build list of courses that may be taken this semester.
    Return a list of the candidate courses, with their 'impact' key set.
    """
    sorted_courses = dekky.list.index_dict_list(courses, 'code')
    # impact scores determine whether to take class.
    # at end of analysis, highest scoring courses are selected.
    try:
        prereq_scores = dekky.schedule.analyze_prereqs(sorted_courses)
    except IndexError:
        print "Warning: Prerequisite cycle detected"
    eligibility_scores = dekky.schedule.analyze_eligibility(sorted_courses)
    schedule_scores = dekky.schedule.analyze_offer_schedules(sorted_courses)
    scores = (prereq_scores, schedule_scores)
    eligibilities = (eligibility_scores,)
    combined = dekky.schedule.combine_impact_scores(scores, eligibilities)
    candidate_scores = dekky.schedule.drop_ineligible_scores(combined)
    candidates = dekky.schedule.filter_courses(courses, candidate_scores)
    return candidates

def write_semester_courses(semester):
    """Write the given courses to stdout.
    semester -- a list of course dicts that give info on the courses to be taken
    this semester.
    """
    for s in semester:
        sys.stdout.write(s['code'] + "|" + s['name'])
        sys.stdout.write('\n')

def parse_course(course_line):
    """Parse a line of course information into a map containing the data.
    course_line -- the course information to be parsed. Must not contain newline
    character.
    Return the dict with course data, or None if it is not valid.
    """
    parts = course_line.split('|')
    if len(parts) != COURSE_RECORD_COUNT:
        raise IndexError("'" + course_line + "' has an invalid field count")
    name = dekky.parse.string_val(parts[0])
    abbr = dekky.parse.string_val(parts[1])
    taken = dekky.parse.yes_no(parts[2])
    prereqs = dekky.parse.delimited_list(parts[3], ',')
    coreqs = dekky.parse.delimited_list(parts[4], ',')
    pattern = dekky.parse.int_val(parts[5])
    offered = dekky.parse.yes_no(parts[6])
    credits = dekky.parse.int_val(parts[7])
    perm = dekky.parse.yes_no(parts[8])
    prior = dekky.parse.int_val(parts[9])
    return {'name': name, 'code': abbr, 'taken': taken, 'prereqs': prereqs,
                    'coreqs': coreqs, 'pattern': pattern, 'offered': offered,
                    'credits': credits, 'permission': perm, 'impact': prior}
    

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        pass #simply exit; do not barf all over the console
