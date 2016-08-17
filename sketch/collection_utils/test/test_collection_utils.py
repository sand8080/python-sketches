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

import unittest2

from sketch import collection_utils as cu


class TestKeysPathsFinding(unittest2.TestCase):

    def test_extract_key_paths(self):
        self.assertEqual([], cu.extract_key_paths([], {}))
        self.assertEqual([], cu.extract_key_paths([], []))
        self.assertEqual([], cu.extract_key_paths([], ()))
        self.assertItemsEqual(
            [['a'], ['b'], [1]],
            cu.extract_key_paths([], {'a': 1, 'b': {'bb': 10}, 1: 2})
        )
        self.assertItemsEqual(
            [[0], [1], [2]],
            cu.extract_key_paths([], ['a', {}, 3])
        )
        self.assertItemsEqual(
            [['x', 'y', 'a'], ['x', 'y', 'b']],
            cu.extract_key_paths(['x', 'y'], {'a': 1, 'b': []})
        )
        self.assertItemsEqual(
            [['x', 'y', 'a'], ['x', 'y', 'b']],
            cu.extract_key_paths(['x', 'y'], {'a': 1, 'b': []})
        )
        self.assertIsNone(cu.extract_key_paths([], set([1, 2])))
        self.assertIsNone(cu.extract_key_paths([], frozenset([1, 2])))
        self.assertItemsEqual(
            [[0], [1]],
            cu.extract_key_paths([], (1, 2))
        )
        self.assertItemsEqual(
            [[0], [1]],
            cu.extract_key_paths([], (1, {'a': 'a_val'}))
        )

    def test_collect_all_paths(self):
        self.assertItemsEqual([], cu.extract_all_paths([]))
        self.assertItemsEqual([
            [0], [1], [2], [3, 0]],
            cu.extract_all_paths([1, [], {}, [1]])
        )
        self.assertItemsEqual([], cu.extract_all_paths([]))
        self.assertItemsEqual(
            [['a'], ['b'], ['c', 'd']],
            cu.extract_all_paths({'a': {}, 'b': [], 'c': {'d': 1}})
        )
        self.assertItemsEqual(
            [['a'], ['b'], ['c', 'd']],
            cu.extract_all_paths({'a': 1, 'b': 2, 'c': {'d': 3}})
        )
        self.assertItemsEqual([[0]], cu.extract_all_paths({0: None}))
        self.assertItemsEqual([[0], [1]], cu.extract_all_paths((1, 2)))
        self.assertItemsEqual(
            [[0], [1, 'a'], [1, 'b', 0]],
            cu.extract_all_paths((1, {'a': 1, 'b': [2]}))
        )
        self.assertItemsEqual(
            [['a'], ['b', 0]],
            cu.extract_all_paths({'a': 1, 'b': (2,)})
        )

    def test_filter_collection(self):
        self.assertEqual([], cu.remove_from_collection([]))
        self.assertEqual((), cu.remove_from_collection(()))
        self.assertEqual({}, cu.remove_from_collection({}))
        self.assertItemsEqual([1, 2, 3], cu.remove_from_collection([1, 2, 3]))
        self.assertItemsEqual((1, 2, 3), cu.remove_from_collection((1, 2, 3)))
        self.assertEqual(
            {'a': 1, 'b': 2},
            cu.remove_from_collection({'a': 1, 'b': 2})
        )

        self.assertEqual(
            {'a': {}},
            cu.remove_from_collection({'a': {'b': 1}}, remove_keys=('b',))
        )
        self.assertEqual(
            {},
            cu.remove_from_collection({'a': {'b': 1}}, remove_keys=('a',))
        )
        self.assertEqual(
            [{}],
            cu.remove_from_collection([{'a': {'b': 1}}], remove_keys=('a',))
        )
        self.assertEqual(
            ({},),
            cu.remove_from_collection(({'a': {'b': 1}},), remove_keys=('a',))
        )

        self.assertEqual(
            {'a': {'c': {'e': 3}}},
            cu.remove_from_collection(
                {'a': {'b': {'f': 5}, 'c': {'d': 2, 'e': 3, 'b': 4}}},
                remove_keys=('d', 'b')
            )
        )
        self.assertEqual(
            [{'a': {}}, {}, {'a': {'d': 3}}],
            cu.remove_from_collection(
                [{'a': {'b': 1}}, {'b': {'c': 2}}, {'a': {'d': 3, 'b': 4}}],
                remove_keys=('b',)
            )
        )

    def test_filter_collection_modify(self):
        origin = {'a': {'b': 1, 'c': 2}}
        expected_not_modified = copy.deepcopy(origin)
        expected_modified = {'a': {'c': 2}}

        self.assertEqual(
            expected_modified,
            cu.remove_from_collection(
                origin,
                remove_keys=('b',),
                modify_collection=False
            )
        )
        self.assertEqual(expected_not_modified, origin)

        self.assertEqual(
            expected_modified,
            cu.remove_from_collection(
                origin,
                remove_keys=('b',),
                modify_collection=True
            )
        )
        self.assertEqual(expected_modified, origin)
