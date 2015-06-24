import wx
from random import choice as randChoice

def hideDefinitionHandler(obj):
	print "hideDefinitionHandler"

def hideRomajiHandler(obj):
	print "hideRomajiHandler"

'''
def handleClickInputBox(evt):
	evt.GetEventObject().SetValue("")
	evt.GetEventObject().SetFocus()


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

def handleInput(self,evt):
	updatePrevImgBox(self, evt)
	checkForCorrectAns(self, evt)
	drawNextWord(self, evt)


def drawNextWord(self, evt):

		randWord=randChoice(self.wordDict.keys())
		self.prevWord=randWord
		self.definition=self.wordDict[randWord]
		self.randWordLabel.SetLabel(self.definition)
		self.wordDict.pop(randWord)
		fileList=fileListForWord(randWord)

		for i in self.imgHolder[:]:
			i.Destroy()
		self.imgHolder=[]

		#self.currImgSizer.Clear()

		#self.currImgNLabelSizer.Layout()
		#self.imgBoxSizer.Layout()


		for filename in fileList:
			self.drawImage(filename, self.currImgSizer)


		for i in self.imgHolder[:]:
			i.Show()

		#self.currImgNLabelSizer.Layout()
		#self.imgBoxSizer.Layout()
		self.Layout()

'''