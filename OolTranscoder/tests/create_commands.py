import cases.export_UNCOMPRESS_only as UNCOMPRESS_only
import cases.export_QT_only as QT_only
import cases.export_HD_only as HD_only

import cases.export_all_on as all
import controllers.export as exp
import sys
import os
import unittest
import json

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())


_logs_dir = os.path.join(os.getcwd(), "tests", "logs")
if not os.path.exists(_logs_dir):
    os.makedirs(_logs_dir)


class TestTranscodingCommands(unittest.TestCase):

    def test_command_01(self):
        print(".-> Export all videos with default folders")
        test = all.case
        self.maxDiff = None
        result = exp.with_source(test["config"])

        self.assertEqual(
            result["UNCOMPRESS"],
            test["UNCOMPRESS"]
        )

        self.assertEqual(
            result["H264"],
            test["H264"]
        )

        self.assertEqual(
            result["4444"],
            test["4444"]
        )

        self.assertEqual(
            result["QT"],
            test["QT"]
        )

        self.assertEqual(
            result["HD"],
            test["HD"]
        )

        with open(os.path.join(_logs_dir, "TestTranscodingCommands_01.json"), "w") as fp:
            json.dump(result, fp, indent=4, sort_keys=True)

    def test_command_02(self):
        print("-> Export UNCOMPRESS only")
        test = UNCOMPRESS_only.case
        self.maxDiff = None
        result = exp.with_source(test["config"])

        self.assertEqual(
            result["UNCOMPRESS"],
            test["UNCOMPRESS"]
        )

        self.assertEqual(
            result["H264"],
            test["H264"]
        )

        self.assertEqual(
            result["4444"],
            test["4444"]
        )

        self.assertEqual(
            result["QT"],
            test["QT"]
        )

        self.assertEqual(
            result["HD"],
            test["HD"]
        )

        with open(os.path.join(_logs_dir, "TestTranscodingCommands_02.json"), "w") as fp:
            json.dump(result, fp, indent=4, sort_keys=True)

    def test_command_03(self):
        print("-> Export QT only")
        test = QT_only.case
        self.maxDiff = None
        result = exp.with_source(test["config"])

        self.assertEqual(
            result["UNCOMPRESS"],
            test["UNCOMPRESS"]
        )

        self.assertEqual(
            result["H264"],
            test["H264"]
        )

        self.assertEqual(
            result["4444"],
            test["4444"]
        )

        self.assertEqual(
            result["QT"],
            test["QT"]
        )

        self.assertEqual(
            result["HD"],
            test["HD"]
        )

        with open(os.path.join(_logs_dir, "TestTranscodingCommands_03.json"), "w") as fp:
            json.dump(result, fp, indent=4, sort_keys=True)

    def test_command_04(self):
        print("-> Export HD only")
        test = HD_only.case
        self.maxDiff = None
        result = exp.with_source(test["config"])

        self.assertEqual(
            result["UNCOMPRESS"],
            test["UNCOMPRESS"]
        )

        self.assertEqual(
            result["H264"],
            test["H264"]
        )

        self.assertEqual(
            result["4444"],
            test["4444"]
        )

        self.assertEqual(
            result["QT"],
            test["QT"]
        )

        self.assertEqual(
            result["HD"],
            test["HD"]
        )

        with open(os.path.join(_logs_dir, "TestTranscodingCommands_04.json"), "w") as fp:
            json.dump(result, fp, indent=4, sort_keys=True)


if __name__ == "__main__":
    unittest.main()
