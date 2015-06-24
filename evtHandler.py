import wx
from random import choice as randChoice

def hideDefinitionHandler(evt):
	print "hideDefinitionHandler"

def hideRomajiHandler(evt):
	print "hideRomajiHandler"

def statsBtnHandler(evt):
	print "Stats button"

def changesDictBtnHandler(evt):
	print "Change dict"

def handleClickInputBox(evt):
	evt.GetEventObject().SetValue("")
	evt.GetEventObject().SetFocus()

def handleInput(self, evt):
	userAns=evt.GetEventObject().GetValue()
	evt.GetEventObject().SetValue("")
	evt.GetEventObject().SetFocus()

	if userAns=="quit" or userAns=="exit":
		self.closeHandler()
	else:
		checkAns(self, userAns)
		nextPrevImgBox(self, evt)
		nextCurrImgBox(self, evt)

def checkAns(self, userAns):
	correctAns=self.currWord.replace("-","")
	if userAns==correctAns:
		print "Correct"
	else:
		print "{userAns} is wrong. Correct answer is {correctAns}".format(userAns=userAns, correctAns=correctAns)


def nextPrevImgBox(self, evt):
	prevWord=self.currWord
	prevDef=self.definition

	self.prevWordLabel.SetLabel(prevDef)

	fileList=self.fileListForWord(prevWord)

	[img.Destroy() for img in self.prevImgHolder]
	self.prevImgHolder=[]

	self.drawWord(fileList, self.prevImgSizer, self.prevImgHolder, hidden=True)

	[img.Show() for img in self.prevImgHolder]

	self.Layout()

def nextCurrImgBox(self, evt):

	self.currWord=randChoice(self.wordDict.keys())
	self.definition=self.wordDict[self.currWord]
	self.wordDict.pop(self.currWord)

	self.currWordLabel.SetLabel(self.definition)

	fileList=self.fileListForWord(self.currWord)

	[img.Destroy() for img in self.currImgHolder]
	self.currImgHolder=[]

	self.drawWord(fileList, self.currImgSizer, self.currImgHolder, hidden=True)

	[img.Show() for img in self.currImgHolder]

	self.Layout()
'''

def correctAnsForFileList(fileList):

	word=""
	vowels=['a','e','o','i','u']

	for i in range (0,len(fileList)) :
		fileList[i]=fileList[i].replace(".png","")

		if fileList[i]=="minitsu":
			if i<len(fileList)-1:
				if fileList[i+1][0] not in vowels:
					word=word+(fileList[i+1][0])
				else:
					raise ValueError("Last syllable must not be a vowel")
			else:
				raise ValueError("Last syllable can't be a Sokuon(little tsu)")

		else:
			word=word+(fileList[i])

	return word

def updatePrevImgBox(self, evt):
	#self.prevImgSizer.Clear()
	#self.prevImgNLabelSizer.Layout()
	#self.imgBoxSizer.Layout()

	fileList=fileListForWord(self.prevWord)
	for filename in fileList:
			self.drawImage(filename, self.prevImgSizer)
	for i in self.prevImgHolder[:]:
		i.Show()
	self.prevImgSizer.Layout()
	self.prevImgNLabelSizer.Layout()
	self.imgBoxSizer.Layout()
	self.Layout()


def checkForCorrectAns(self, evt):
	print evt.GetEventObject().GetValue()
	from string import replace
	eList=map(lambda x: x.replace(".png",""),fileListForWord(self.prevWord))
	rStr="".join(eList)
	print rStr
	evt.GetEventObject().SetValue("")





'''