from rope import (Rope, prepend, append, delete_range, insert,
                  create_rope_from_map, rotate_left, rotate_right, rebalance)
import unittest


def make_deep_rope() -> Rope:
    deep_rope = Rope('345')
    prepend(deep_rope, '012')
    deep_rope.right = Rope('7')
    prepend(deep_rope.right, '6')
    append(deep_rope.right, '8')
    append(deep_rope.right, '9')
    return deep_rope


# These tests are here as a starting point, they are not comprehensive
class Testing(unittest.TestCase):
    def test_rope_basics(self) -> None:
        self.assertEqual(Rope('test').to_string(), 'test')
        self.assertEqual(prepend(Rope('test'), 'abc').to_string(), 'abctest')
        self.assertEqual(append(Rope('test'), 'abc').to_string(), 'testabc')
        self.assertEqual(append(Rope('test'), 'abc').total_size(), 7)

    def test_deletion(self) -> None:
        self.assertEqual(delete_range(Rope('test'), 1, 2).to_string(), 'tst')
        self.assertEqual(delete_range(Rope('test'), 2, 4).to_string(), 'te')
        self.assertEqual(delete_range(Rope('test'), 0, 2).to_string(), 'st')

    def test_deletion_deeper(self) -> None:
        # TODO: use parametrized here.
        rope = make_deep_rope()
        self.assertEqual(delete_range(rope, 0, 2).to_string(), '23456789')
        rope = make_deep_rope()
        self.assertEqual(delete_range(rope, 0, 4).to_string(), '456789')
        rope = make_deep_rope()
        self.assertEqual(delete_range(rope, 0, 9).to_string(), '9')
        rope = make_deep_rope()
        self.assertEqual(delete_range(rope, 0, 100).to_string(), '')
        rope = make_deep_rope()
        self.assertEqual(delete_range(rope, 4, 7).to_string(), '0123789')
        rope = make_deep_rope()
        self.assertEqual(delete_range(rope, 2, 8).to_string(), '0189')

    def test_insertion(self) -> None:
        self.assertEqual(insert(Rope('test'), '123', 2).to_string(), 'te123st')
        self.assertEqual(insert(Rope('test'), '123', 4).to_string(), 'test123')
        self.assertEqual(insert(Rope('test'), '123', 0).to_string(), '123test')

    def test_insertion_deeper(self) -> None:
        self.assertEqual(insert(make_deep_rope(), 'XYZ', 0).to_string(), 'XYZ0123456789')
        self.assertEqual(insert(make_deep_rope(), 'XYZ', 2).to_string(), '01XYZ23456789')
        self.assertEqual(insert(make_deep_rope(), 'XYZ', 4).to_string(), '0123XYZ456789')
        self.assertEqual(insert(make_deep_rope(), 'XYZ', 7).to_string(), '0123456XYZ789')
        self.assertEqual(insert(make_deep_rope(), 'XYZ', 9).to_string(), '012345678XYZ9')
        self.assertEqual(insert(make_deep_rope(), 'XYZ', 10).to_string(), '0123456789XYZ')
        self.assertEqual(insert(make_deep_rope(), 'XYZ', 100).to_string(), '0123456789XYZ')

    # def test_extra_credit_rebalancing(self):
    #   self.assertEqual(rotate_left(create_rope_from_map({
    #     'text': '3',
    #     'left': { 'text': 'a' },
    #     'right': { 'text': '5', 'left': { 'text': 'b' }, 'right': { 'text': '7', 'left': { 'text': 'c' }, 'right': { 'text': 'd' } } },
    #   })).to_dictionary(), {
    #     'text': '5',
    #     'left': {
    #       'text': '3',
    #       'left': { 'text': 'a' },
    #       'right': { 'text': 'b' }
    #     },
    #     'right': {
    #       'text': '7',
    #       'left': { 'text': 'c' },
    #       'right': { 'text': 'd' }
    #     },
    #   })
    #   self.assertEqual(rotate_right(create_rope_from_map({
    #     'text': '5',
    #     'left': { 'text': '3', 'right': { 'text': 'b' }, 'left': { 'text': '2', 'left': { 'text': 'd' }, 'right': { 'text': 'c' } } },
    #     'right': { 'text': 'a' },
    #   })).to_dictionary(), {
    #     'text': '3',
    #     'left': {
    #       'text': '2',
    #       'left': { 'text': 'd' },
    #       'right': { 'text': 'c' }
    #     },
    #     'right': {
    #       'text': '5',
    #       'left': { 'text': 'b' },
    #       'right': { 'text': 'a' }
    #     },
    #   })

    #   balancedTree = {
    #     'text': 'b',
    #     'left': { 'text': 'a' },
    #     'right': { 'text': 'c' }
    #   }

    #   self.assertEqual(rebalance(create_rope_from_map({
    #     'text': 'c',
    #     'left': { 'text': 'a', 'right': { 'text': 'b' } },
    #   })).to_dictionary(), balancedTree)
    #   self.assertEqual(rebalance(create_rope_from_map({
    #     'text': 'c',
    #     'left': { 'text': 'b', 'left': { 'text': 'a' } },
    #   })).to_dictionary(), balancedTree)
    #   self.assertEqual(rebalance(create_rope_from_map({
    #     'text': 'a',
    #     'right': { 'text': 'b', 'right': { 'text': 'c' } },
    #   })).to_dictionary(), balancedTree)
    #   self.assertEqual(rebalance(create_rope_from_map({
    #     'text': 'a',
    #     'right': { 'text': 'c', 'left': { 'text': 'b' } },
    #   })).to_dictionary(), balancedTree)

if __name__ == '__main__':
    unittest.main()
