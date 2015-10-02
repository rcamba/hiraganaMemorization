import wx
import re
from random import choice as randChoice

def insertDictHandler(self, evt):
	selection = list(self.unused_dict_box.GetSelections())
	selection.reverse()

	for s in selection:
		item = self.unusedDicts.pop(s)
		self.currDicts.append(item)

	self.unused_dict_box.Set(self.unusedDicts)
	self.curr_dict_box.Set(self.currDicts)

	self.parent.LAST=False


def removeDictHandler(self, evt):
	selection = list(self.curr_dict_box.GetSelections())
	selection.reverse()

	for s in selection:
		item = self.currDicts.pop(s)
		self.unusedDicts.append(item)

	self.unused_dict_box.Set(self.unusedDicts)
	self.curr_dict_box.Set(self.currDicts)

	self.parent.LAST=False


def curr_sb_handler(self, evt):
	pass

def curr_dlb_handler(self, evt):
	pass

def unused_dlb_handler(self, evt):
	print evt.GetEventObject().GetSelections()

def unused_sb_handler(self, evt):

	if evt.GetEventObject().GetValue() in self.unusedDicts:
		#pass


		self.unused_dict_search_bar.SetBackgroundColour((0,255,0))
		self.unused_dict_search_bar.SetForegroundColour((0,0,0))#text color

	else:
		#pass
		self.unused_dict_search_bar.SetBackgroundColour((255,0,0))
		self.unused_dict_search_bar.SetForegroundColour((255,255,255))#text color

	item_list = self.unusedDicts

	pattern = re.compile(evt.GetEventObject().GetValue())
	self.unused_dict_box.Set([item  for item in item_list if re.search(pattern, item) is not None])

	self.Refresh()


def statsBtnHandler(evt):
	print "Stats button"

def changesDictBtnHandler(self, evt):
	print "Change dict!"
	self.cdp.unused_dict_search_bar.SetValue("")
	self.cdp.Center()
	self.cdp.Show()


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

def handleClickInputBox(evt):
	evt.GetEventObject().SetValue("")
	evt.GetEventObject().SetFocus()

def handleInput(self, evt):
	userAns=evt.GetEventObject().GetValue()
	evt.GetEventObject().SetValue("")
	evt.GetEventObject().SetFocus()

	if userAns=="quit" or userAns=="exit":
		self.closeHandler()

	elif self.LAST is False:
		checkAns(self, userAns)
		nextPrevImgBox(self, evt)
		nextCurrImgBox(self, evt)

	else:
		print "No words remaining"


def generateCorrectAns(currWord):
	correctAns=""
	vowels=['a','e','o','i','u']
	tokens=currWord.split('-')
	for i in range(0,len(tokens)):

		if tokens[i]=="minitsu":
			if i<len(tokens)-1 and tokens[i+1][0] not in vowels:
				correctAns=correctAns+tokens[i+1][0]
			else:
				raise ValueError("Last syllable can't be a Sokuon(little tsu) and must not be a vowel" + ". Tokens="+ str(tokens))
		else:
			correctAns=correctAns+tokens[i]

	return correctAns


def checkAns(self, userAns):
	correctAns=generateCorrectAns(self.currWord)
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

	if len(self.wordDict)>0:
		self.currWord=randChoice(self.wordDict.keys())
		self.definition=self.wordDict[self.currWord]
		self.wordDict.pop(self.currWord)

		self.currWordLabel.SetLabel(self.definition)

		fileList=self.fileListForWord(self.currWord)

		[img.Destroy() for img in self.currImgHolder]
		self.currImgHolder=[]

		self.drawWord(fileList, self.currImgSizer, self.currImgHolder, hidden=True)

	else:
		[img.Hide() for img in self.prevImgHolder]
		[img.Hide() for img in self.currImgHolder]

		self.currWordLabel.SetLabel("")
		self.prevWordLabel.SetLabel("No words remaining")
		self.LAST=True
		self.Layout()