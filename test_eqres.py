import unittest

import eqres

res = {'r1': 100, 'r2': 40.5, 'r3': 1500, 'r4': 0, 'r5': 18}
three_res = {'ra': 100, 'rb': 40.5, 'rc': 1500}
two_res = {'r1': 100, 'r2': 40.5}

class TestEqres(unittest.TestCase):


    def test_parallel(self):
        result = eqres.parallel(two_res, res)
        self.assertEqual(result, 'r12 = 28.83')

    def test_consistent(self):
        result = eqres.consistent(two_res, res)
        self.assertEqual(result, 'r12 = 140.5')

    def test_to_triangle(self):
        result = eqres.to_triangle(three_res, res)
        self.assertEqual(result, 'rd = 143.2, re = 2148.0, rf = 5303.70')

    def test_to_star(self):
        result = eqres.to_star(three_res, res)
        self.assertEqual(result, 'ra = 91.44, rb = 2.47, rc = 37.03')


if __name__ == '__main__':
    unittest.main()
