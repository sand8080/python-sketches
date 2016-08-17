# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy


def extract_key_paths(base_path, collection):
    """Extracts key paths for collection and joins with base_path.

    If collection is list or tuple indexes will be added to base_path.
    If collection is dict keys will be added to base_path.

    :param base_path: list of indexes
    :param collection: collection
    :return: base_path extended by collection indexes
    """

    if isinstance(collection, dict):
        return [base_path + [k] for k in collection.keys()]
    elif isinstance(collection, (list, tuple)):
        return [base_path + [idx] for idx in range(len(collection))]
    else:
        return None


def extract_all_paths(collection):
    """Extracts all paths to leaf elements of collection.

    In case of {'a': {'b': 1}} result will be [['a', 'b']]
    In case of ['a', {'b': 1}}] result will be [[0], [1, 'b']]
    Empty collection considered as leaf element and in this case
    for {'a': []} result will be [['a']]

    :param collection: collection
    :return: list of paths to leaf elements
    """

    paths = extract_key_paths([], collection)
    for path in paths:
        point = collection
        for k in path:
            point = point[k]
        new_paths = extract_key_paths(path, point)
        if new_paths:
            paths.extend(new_paths)
        else:
            yield path


def remove_from_collection(collection, remove_keys=(),
                           modify_collection=False):
    """Removes from collection keys listed in filter_keys

    :param collection: collection to be cleaned
    :param remove_keys: list of keys to be removed
    :param modify_collection: modify original collection or not
    :return: filtered collection
    """

    result = collection if modify_collection else copy.deepcopy(collection)
    paths = extract_key_paths([], result)
    for path in paths:
        point = result
        deleted = False
        for k in path:
            if isinstance(point, dict) and k in remove_keys:
                del point[k]
                deleted = True
                break
            point = point[k]
        if deleted:
            continue
        new_paths = extract_key_paths(path, point)
        if new_paths:
            paths.extend(new_paths)

    return result
