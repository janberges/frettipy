#!/usr/bin/env python3

import frettipy
import unittest

class Test(unittest.TestCase):
    def test(self):
        with open('before.py') as before, open('after.py') as after:
            self.assertEqual(frettipy.prettify(before.read()), after.read())

if __name__ == '__main__':
    unittest.main()
