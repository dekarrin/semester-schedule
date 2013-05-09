# functions for graph structures

def create_dep_graph(source, dep_list_index):
    """Create a dependency graph from a homogenous dictionary of dictionaries.
    source -- the dictionary to create the graph from.
    dep_list_index -- the index of the sub-dicts that contains the list of
    dependencies for that item.
    Return the graph. The graph is a dict that contains the same keys as the
    source dictionary, but its values are nodes. Nodes are dicts that contain
    two keys: 'data', which is the original value of the key in the source, and
    'deps', which are lists of nodes that this particular node depends on. This
    may be an empty list if there are no dependencies. 'parents' is a list of
    all nodes that depend on that node.
    """
    nodes = dict()
    # add all nodes to the graph before adding any links
    for k in source:
        nodes[k] = {'data': source[k], 'deps': list(), 'parents': list()}
    # now go through and add all links
    for k in nodes:
        dep_ref_list = nodes[k]['data'][dep_list_index]
        if dep_ref_list:
            for d in dep_ref_list:
                nodes[d]['parents'].append(nodes[k])
                nodes[k]['deps'].append(nodes[d])
    return nodes
    
def analyze(graph):
    """Analyze a graph created with create_dep_graph.
    Return a dict with information about the graph, containing the following
    keys:
    'cycles' -- tells whether the graph contains cycles.
    'roots' -- contains a list of all nodes that do not have any dependencies.
    """
    info = {'roots': list()}
    info['acyclic'] = detect_cycles(graph)
    info['roots'] = detect_roots(graph)
    return info
    
def detect_roots(graph):
    """Return all nodes that are not descendents of other nodes."""
    roots = []
    for k, n in graph.items():
        if not n['parents']:
            roots.append(n)
    return roots
    
def detect_cycles(graph):
    """Detects cycles in a graph created with create_dep_graph.
    Return whether there is at least one cycle.
    """
    for k in graph:
        if detect_single_cycle(graph[k]):
            return True
            
def detect_single_cycle(node, traversed = None):
    """Detects cycles using DFS starting from the given node index.
    Return whether there is at least one cycle.
    """
    if traversed is None:
        traversed = []
    if node in traversed:
        return True
    if node['deps']:
        traversed.append(node)
        for d in node['deps']:
            if detect_single_cycle(d, traversed):
                return True
        traversed.remove(node)
        return False
    else:
        return False
