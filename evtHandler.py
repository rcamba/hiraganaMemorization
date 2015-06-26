import wx
from random import choice as randChoice

def searchBarHandler(self, evt):
	if evt.GetEventObject().GetValue() in self.dictList:
		self.searchBar.SetForegroundColour((0,0,0))#text color
		self.searchBar.SetBackgroundColour((0,255,0))

	else:
		self.searchBar.SetForegroundColour((255,255,255))#text color
		self.searchBar.SetBackgroundColour((255,0,0))


def resetToggleOpt(self, evt, resetTargs=["def","sylImg"]):

	if "def" in resetTargs:
		self.currWordLabel.Show()
		self.prevWordLabel.Show()
		self.Layout()

	if "sylImg" in resetTargs:
		[img.Show() for img in self.prevImgHolder+self.currImgHolder]
		self.Layout()
		self.hideSyllableImgFlag=False


def hideDefinitionHandler(self, evt):
	resetToggleOpt(self, evt, ["sylImg"])
	if evt.GetEventObject().GetValue():
		self.currWordLabel.Hide()
		self.prevWordLabel.Hide()
		self.Layout()


def hideSyllableImgHandler(self, evt):
	resetToggleOpt(self, evt, ["def"])
	if evt.GetEventObject().GetValue():
		[img.Hide() for img in self.prevImgHolder+self.currImgHolder]
		self.Layout()
		self.hideSyllableImgFlag=True



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



def nextCurrImgBox(self, evt):

	self.currWord=randChoice(self.wordDict.keys())
	self.definition=self.wordDict[self.currWord]
	self.wordDict.pop(self.currWord)

	self.currWordLabel.SetLabel(self.definition)

	fileList=self.fileListForWord(self.currWord)

	[img.Destroy() for img in self.currImgHolder]
	self.currImgHolder=[]

	self.drawWord(fileList, self.currImgSizer, self.currImgHolder, hidden=True)


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