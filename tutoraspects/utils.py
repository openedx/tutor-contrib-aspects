from ruamel.yaml import YAML

yaml = YAML()

def recursive_sort_mappings(s):
    if isinstance(s, list):
        for elem in s:
            recursive_sort_mappings(elem)
        return
    if not isinstance(s, dict):
        return
    for key in sorted(s, reverse=True):
        value = s.pop(key)
        recursive_sort_mappings(value)
        s.insert(0, key, value)
