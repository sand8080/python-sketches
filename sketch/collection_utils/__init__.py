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


def collect_all_paths(collection):
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


def filter_collection(collection, filter_keys=(), filter_indexes=()):
    result = type(collection)()
    for path in collect_all_paths(collection):
        point_src = collection
        point_dst = result
        add_to_dst = True

        for k in path:
            point_src = point_src[k]
            if isinstance(point_src, dict) and k in filter_keys:
                add_to_dst = False
            elif isinstance(point_src, (list, tuple)) and k in filter_indexes:
                add_to_dst = False

            if not add_to_dst:
                break

        # # Adding to the result
        # if not add_to_dst:
        #     continue
        #
        # point_dst = result
        # point_src = collection
        # for k in path:
        #     # point_dst = point_dst[k]
        #     point_src = point_src[k]