
import unittest
from relationize.relationize import * 
import os
import sys

import pandas as pd
from io import StringIO

# DESCRIPTION =======================================
"""
This module is focused on auditing tabular data where multiple units of
analysis are contained in the same table.

While this is generally a bad idea, it is convenient when many coders are
working together on a single data sheet, and so, it should be supported.
"""

# FIXTURES ==========================================
"""
This is an example of good data, that should return as (data,True).
- Each unit of analysis is denoted by an id column
- Each unique id corresponds to a unique set of values
  in the columns related to that id (uoa)
"""
goodData = StringIO("""
id1,v1a,v1b,id2,v2a,v2b
A  ,a  ,b  ,A  ,c  ,b
B  ,b  ,a  ,A  ,c  ,b
A  ,a  ,b  ,A  ,c  ,b
B  ,b  ,a  ,B  ,b  ,d
A  ,a  ,b  ,B  ,b  ,d
B  ,b  ,a  ,B  ,b  ,d
""")

"""
This is an example of bad data, that should return as (data,False).
- The id value A for id column id2 has more than one unique set of
  corresponding values.
"""
badData = StringIO("""
id1,v1a,v1b,id2,v2a,v2b
A  ,a  ,b  ,A  ,a  ,b
B  ,b  ,a  ,A  ,b  ,b
A  ,a  ,b  ,A  ,c  ,b
B  ,b  ,a  ,B  ,b  ,d
A  ,a  ,b  ,B  ,b  ,d
B  ,b  ,a  ,B  ,b  ,d
B  ,b  ,a  ,C  ,a  ,d
A  ,a  ,b  ,C  ,b  ,d
""")

# TESTS =============================================
class TestTest(unittest.TestCase):
    def setUp(self):
        self.goodData = pd.read_csv(goodData)
        self.badData = pd.read_csv(badData)

    def test_relationize(self):
        d = getRelations(self.goodData,{
            "id1":("v1a","v1b"),
            "id2":("v2a","v2b")})
        self.assertTrue(all([valid for data,valid in d]))

        d = getRelations(self.badData,{
            "id1":("v1a","v1b"),
            "id2":("v2a","v2b")})

        # One valid and one invalid relation 
        self.assertTrue(not all([valid for data,valid in d]))
        self.assertEqual(1,len([data for data,valid in d if not valid]))
        self.assertEqual(1,len([data for data,valid in d if valid]))

        invalid = [data for data,valid in d if not valid][0]
        # Returns five rows of duplicates
        self.assertEqual(5,invalid.shape[0])

if __name__ == "__main__":
    unittest.main()

