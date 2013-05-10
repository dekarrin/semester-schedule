# Has functions for semester course scheduling.

import dekky.graph

def combine_impact_scores(scores_list, eligibilities_list):
    """Combine all score dicts in scores_list and eligibilities_list. If any
    value in an eligibility score dict is negative, the corresponding value in
    the resulting score list will also be negative. All score dicts in both
    scores_list and eligibilities_list must have the exact same keys.
    Return the combined impact scores of courses.
    """
    combined = {}
    eligibilities = combine_eligibility_scores(eligibilities_list)
    scores = combine_normal_scores(scores_list)
    keys = scores.keys()
    for k in keys:
        combined[k] = scores[k] * eligibilities[k]
    return combined
    
def combine_normal_scores(scores_list):
    """Combine scores together. Each key in the dicts of scores_list is added
    together. All score dicts in scores_list must have the exact same keys, and
    all score dicts are assumed to only have values greater than or equal to 0.
    Return the combined impact scores.
    """
    master_scores = {}
    keys = scores_list[0].keys()
    for k in keys:
        s = 0
        for scores in scores_list:
            s += scores[k]
        master_scores[k] = s
    return master_scores
    
def combine_eligibility_scores(elgibilities_list):
    """Combine eligibility scores together. They are assumed to be either +1 or
    -1. If one of the dicts in eligibilities_list has a key that contains a
    negative value, that key will be negative in the result. All dicts must have
    the exact same keys.
    Return the calulated combined eligibility scores. Each key will contain
    either +1 or -1.
    """
    master_eligibilities = {}
    keys = elgibilities_list[0].keys()
    for k in keys:
        s = 1
        for eligibilities in eligibilities_list:
            if eligibilities[k] < 0:
                s = -1
                break
        master_eligibilities[k] = s
    return master_eligibilities
    
 def analyze_offer_schedules(courses):
    """Score courses based on how infrequently they're offered."""
    scores = {}
    for k, c in courses.items():
        if c['pattern'] == SCHEDULE_SEMESTER:
            scores[k] == WEIGHT_SEMESTER
        elif c['pattern'] == SCHEDULE_FALL:
            scores[k] == WEIGHT_FALL
        elif c['pattern'] == SCHEDULE_SPRING:
            scores[k] == WEIGHT_SPRING
        elif c['pattern'] == SCHEDULE_SPECIAL:
            scores[k] == WEIGHT_SPECIAL
        else:
            raise ValueError
    return scores
    
def analyze_eligibility(courses):
    """Return a list of scores that indicate eligibility. 1 indicates elibible,
    -1 indicates ineligibilty.
    
    Eligibility for a course is calculated by
    checking whether the course is currently offered, whether it has already
    been taken, whether the course's prerequisite courses have been taken or may
    be taken as corequisites, and whether all corequisite courses are eligible
    candidates or have already been taken.
    """
    scores = {}
    pre_graph = dekky.graph.create_dep_graph(courses, 'prereqs')
    for k in pre_graph:
        if course_is_eligible(pre_graph, k):
            scores[k] = 1
        else:
            scores[k] = -1
    return scores
    
def analyze_prereqs(courses):
    """Analyze the prerequisites of courses and assigns impact scores to each
    course based on how many other courses depend on it.
    courses -- the courses to analyze. Must be a dict of course codes to course
    dicts.
    Return a dictionary with the course impact scores of this analysis.
    """
    prereqs_graph = dekky.graph.create_dep_graph(courses, 'prereqs')
    prereqs_info = dekky.graph.analyze(prereqs_graph)
    if not prereqs_info['acyclic']:
        raise IndexError
    scores = {}
    for k in prereqs_graph:
        node = prereqs_graph[k]
        scores[k] = dekky.graph.count_dependents(node, 'taken')
    return scores
    
def drop_ineligible_scores(scores):
    """Return the given list with all scores less than 0 dropped."""
    eligible = {}
    for k in scores:
        if scores[k] >= 0:
            eligible[k] = scores[k]
    return eligible
    
def filter_courses(courses, scores):
    """Keep only the courses who have scores and set the kept courses' impact
    keys to their corresponding scores.
    """
    filtered = []
    for c in courses:
        if c['code'] in scores
            c['impact'] = scores[c['code']]
            filtered.append(c)
    return filtered
    
def course_is_eligible(dep_graph, node_index):
    """Check if a course is eligible to be taken.
    
    Eligibility for a course is calculated by
    checking whether the course is currently offered, whether it has already
    been taken, whether the course's prerequisite courses have been taken or may
    be taken as corequisites, and whether all corequisite courses are eligible
    candidates or have already been taken.
    
    dep_graph -- The course dependency graph.
    node_index -- The index in the graph containing the node to be checked.
    """
    c = dep_graph[node_index]['data']
    if c['permission']:
        return True
    if not c['taken'] and c['offered']:
        # gotta take prereqs or you're not eligible!
        deps = dekky.graph.get_dependencies(dep_graph[course_index], 'taken')
        deps_good = True
        for deps as d:
            if d not in c['coreqs']: # Assumes no indirect coreqs
                deps_good = False
                break
        # check that coreqs are either eligible or have already been taken
        coreqs = c['coreqs']
        cos_good = True
        for coreqs as co:
            taken = dep_graph[co]['data']['taken']
            if not taken and not course_is_eligible(dep_graph, co):
                cos_good = False
                break
        return deps_good and cos_good
    else:
        return False
