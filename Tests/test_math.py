import unittest
from Other.Maths.Permutations import generate_permutation


class TestPermutaionGenerator(unittest.TestCase):

    def test_min_length(self):
        test_data = [1, 2, 3, 4, 5]
        expected_result = [[1], [2], [3], [4], [5]]

        result = generate_permutation(test_data, 1)

        self.assertEquals(len(result), len(expected_result))
        self.assertListEqual(result, expected_result)

    def test_small(self):
        test_data = [1, 2, 3, 4]
        expected_result = [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

        result = generate_permutation(test_data, 2)

        self.assertEquals(len(result), len(expected_result))
        self.assertListEqual(result, expected_result)

    def test_big(self):
        test_data = [1, 2, 3, 4, 5, 6]
        expected_result = [[1, 2, 3, 4, 5], [1, 2, 3, 4, 6],
                           [1, 2, 3, 5, 6], [1, 2, 4, 5, 6], [1, 3, 4, 5, 6], [2, 3, 4, 5, 6]]

        result = generate_permutation(test_data, 5)

        self.assertEquals(len(result), len(expected_result))
        self.assertListEqual(result, expected_result)

    def test_max_length(self):
        test_data = [1, 2, 3, 4, 5]
        expected_result = [[1, 2, 3, 4, 5]]

        result = generate_permutation(test_data, 5)

        self.assertEquals(len(result), len(expected_result))
        self.assertListEqual(result, expected_result)
