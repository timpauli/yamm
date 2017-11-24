from unittest import TestCase, main

from yamm import Chain


class ChainTest(TestCase):

    def test_equal(self):
        test = Chain({(1,): {1: 1, 2: 1},
                      (2,): {1: 1}})
        check = Chain({(2,): {1: 1},
                       (1,): {2: 1, 1: 1}})
        self.assertEqual(test, check)

    def test_from_data1(self):
        test = Chain.test_from_data([1, 2, 1, 1])
        check = Chain({(1,): {1: 1, 2: 1},
                       (2,): {1: 1}})
        self.assertEqual(test, check)

    def test_from_data2(self):
        test = Chain.test_from_data([1, 2, 1, 1], 2)
        check = Chain({(1, 2): {1: 1},
                       (2, 1): {1: 1}})
        self.assertEqual(test, check)

    def test_from_matrix(self):
        pass

    def test_step(self):
        chain = Chain({(1,): {1: 1, 2: 1},
                       (2,): {1: 1}})
        test = chain.step(2)
        check = 1
        self.assertEqual(test, check)

    def test_walk(self):
        chain = Chain({(1,): {2: 1},
                       (2,): {3: 1},
                       (3,): {1: 1}})
        test = chain.walk_until(1)
        check = (1, 2, 3)
        for t, c in zip(test, check):
            self.assertEqual(t, c)

    def test_walk_until(self):
        chain = Chain({(1,): {1: 1, 2: 1},
                       (2,): {1: 1}})
        test = len(chain.walk_until(1, 8))
        check = 8
        self.assertEqual(test, check)


if __name__ == '__main__':
    main()
