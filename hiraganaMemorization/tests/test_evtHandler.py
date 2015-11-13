import unittest
from os import pardir
from sys import path

path.append(pardir)
from hirMem.evtHandler import generateCorrectAns


class TestEvts(unittest.TestCase):

	def setUp(self):
		print "\nStarting ", self._testMethodName

	def test_generateCorrectAns_valid(self):
		word = "sa-sokuon-ki"

		correctAns = generateCorrectAns(word)
		self.assertEqual(correctAns, "sakki")

	def test_generateCorrectAns_invalid_sokuon(self):
		word = "sokuon-sokuon"
		expectedMsg = "Last syllable can't be a sokuon"

		with self.assertRaises(ValueError) as context:
			generateCorrectAns(word)

		self.assertIn(expectedMsg, str(context.exception))

	def test_generateCorrectAns_invalid_lastWordSokuon(self):
		word = "ka-ki-sokuon"
		expectedMsg = "Last syllable can't be a sokuon"

		with self.assertRaises(ValueError) as context:
			generateCorrectAns(word)

		self.assertIn(expectedMsg, str(context.exception))

	def test_generateCorrectAns_invalid_lastWordVowel(self):
		word = "sokuon-o"
		expectedMsg = "must not be a vowel"

		with self.assertRaises(ValueError) as context:
			generateCorrectAns(word)

		self.assertIn(expectedMsg, str(context.exception))


def getEvts_TS():
	ts = unittest.TestSuite()

	ts.addTest(TestEvts("test_generateCorrectAns_valid"))
	ts.addTest(TestEvts("test_generateCorrectAns_invalid_sokuon"))
	ts.addTest(TestEvts("test_generateCorrectAns_invalid_lastWordSokuon"))
	ts.addTest(TestEvts("test_generateCorrectAns_invalid_lastWordVowel"))

	return ts


if __name__ == "__main__":

	suiteList = []

	evts_TS = getEvts_TS()

	suiteList.append(evts_TS)
	fullSuite = unittest.TestSuite(suiteList)

	runner = unittest.TextTestRunner()
	runner.run(fullSuite)
