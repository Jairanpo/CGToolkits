import command_data as data
import controllers.encode as enc
import sys
import os
import unittest

if not os.getcwd() in sys.path:
    sys.path.append(os.getcwd())


class TestEncoding(unittest.TestCase):

    def test_command_01(self):
        print(".-> Best case scenario")
        test = data.test_01
        self.maxDiff = None
        self.assertTrue(enc.command(test["config"])["valid"])
        self.assertEqual(
            enc.command(test["config"])["command"],
            test["command"]
        )

    def test_command_02(self):
        print("-> Invalid source file")
        self.maxDiff = None
        result = enc.command(data.test_02["config"])

        self.assertFalse(result["valid"])
        self.assertEqual(result["message"], data.test_02["message"])
        self.assertEqual(result["command"], data.test_02["command"])

    def test_command_03(self):
        print("-> Invalid output file")
        self.maxDiff = None
        result = enc.command(data.test_03["config"])

        self.assertFalse(result["valid"])
        self.assertEqual(result["message"], data.test_03["message"])
        self.assertEqual(result["command"], data.test_03["command"])

    def test_command_04(self):
        print("-> To default framerate")
        test = data.test_04
        self.maxDiff = None
        self.assertTrue(enc.command(test["config"])["valid"])
        self.assertEqual(
            enc.command(test["config"])["command"],
            test["command"]
        )

    def test_command_05(self):
        print("-> Without force")
        test = data.test_05
        self.maxDiff = None
        self.assertTrue(enc.command(test["config"])["valid"])
        self.assertEqual(
            enc.command(test["config"])["command"],
            test["command"]
        )

    def test_command_06(self):
        print("-> Without crf")
        test = data.test_06
        self.maxDiff = None
        self.assertTrue(enc.command(test["config"])["valid"])
        self.assertEqual(
            enc.command(test["config"])["command"],
            test["command"]
        )

    def test_command_07(self):
        print("-> Without preset")
        test = data.test_07
        self.maxDiff = None
        self.assertTrue(enc.command(test["config"])["valid"])
        self.assertEqual(
            enc.command(test["config"])["command"],
            test["command"]
        )


if __name__ == "__main__":
    unittest.main()
