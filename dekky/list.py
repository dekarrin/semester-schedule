# functions for working with lists

def index_dict_list(dict_list, index):
    """Reorganize a list of dicts into a dict of dicts.
    dict_list -- The original list of dictionaries.
    index -- The key in the dicts to index each dictionary by.
    Return the indexed dictionary.
    """
    dict_dict = dict()
    for d in dict_list:
        dict_dict[d[index]] = d
    return dict_dict