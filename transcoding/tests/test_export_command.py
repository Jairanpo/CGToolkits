import sys
import os
import unittest

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())

import controllers.export as exp
import export_data as data

class TestTranscodingCommands(unittest.TestCase):

    def test_command_01(self):
        print(".-> Export all videos with default folders")
        test = data.ts01
        self.maxDiff = None
        result = exp.with_sources([test["config"]])
        self.assertEqual(
            result["UNCOMPRESS"],
            data.ts01["commands"]["UNCOMPRESS"]
        )