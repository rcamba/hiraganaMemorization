import unittest
from sys import path
path.append("../")
from hm_eventHandlers import fileListForWord, correctAnsForFileList

class TestHMEvts(unittest.TestCase):
	def setUp(self):
		print "\nStarting ", self._testMethodName

	def test_wordForFileList_valid(self):
		word="sa-minitsu-ki"
		fileList=fileListForWord(word)

		correctAns=correctAnsForFileList(fileList)
		self.assertEqual(correctAns, "sakki")


	def test_wordForFileList_invalid_minitsu(self):
		word="minitsu-minitsu"
		fileList=fileListForWord(word)
		expectedMsg="Last syllable can't be a Sokuon"

		with self.assertRaises(ValueError) as context:
			correctAnsForFileList(fileList)

		self.assertTrue( expectedMsg in str(context.exception) )

	def test_wordForFileList_invalid_lastWordMinitsu(self):
		word="ka-ki-minitsu"
		fileList=fileListForWord(word)
		expectedMsg="Last syllable can't be a Sokuon"

		with self.assertRaises(ValueError) as context:
			correctAnsForFileList(fileList)

		self.assertTrue( expectedMsg in str(context.exception) )

	def test_wordForFileList_invalid_lastWordVowel(self):
		word="minitsu-o"
		fileList=fileListForWord(word)
		expectedMsg="Last syllable must not be a vowel"

		with self.assertRaises(ValueError) as context:
			correctAnsForFileList(fileList)

		self.assertTrue( expectedMsg in str(context.exception) )


def getHMEvts_TS():
	ts= unittest.TestSuite()

	ts.addTest( TestHMEvts( "test_wordForFileList_valid"))
	ts.addTest( TestHMEvts( "test_wordForFileList_invalid_minitsu"))
	ts.addTest( TestHMEvts( "test_wordForFileList_invalid_lastWordMinitsu"))
	ts.addTest( TestHMEvts( "test_wordForFileList_invalid_lastWordVowel"))


	return ts

if __name__=="__main__":


	suiteList=[]

	hmEvts_TS=getHMEvts_TS()

	suiteList.append(hmEvts_TS)
	fullSuite = unittest.TestSuite(suiteList)

	runner = unittest.TextTestRunner()
	runner.run(fullSuite)
