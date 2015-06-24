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
	print evt.GetEventObject().GetValue()
	evt.GetEventObject().SetValue("")
	evt.GetEventObject().SetFocus()

	nextCurrImgBox(self, evt);

def nextCurrImgBox(self, evt):

	word=randChoice(self.wordDict.keys())
	self.definition=self.wordDict[word]
	self.wordDict.pop(word)

	self.wordLabel.SetLabel(self.definition)

	fileList=self.fileListForWord(word)

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