# python-sketches

## sketch.collection_utils

**Iterative implementation of extracting key paths from collection**

Extracts all key paths for leaf elements. For instase key paths for:

`{'a': 1, 'b': ()}, 'd': (8, 9, 'c': {'e': 2})} => [['a'], ['b'], ['d', 0], ['d', 1], ['d', 2, 'c', 'e']]`

**Iterative implementation of collection filtering**

Filters specified keys from collection:

`[{'a': {'b': 1}}, {'b': 2}, {'c': {'b': 3, 'd': 4}}] => filter keys: ('b',) => [{'a': {}}, {}, {'c': {'d': 4}}]`
