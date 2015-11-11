import wx
import re
from random import choice as randChoice


def insertDictHandler(cdp, evt):
	"""
	used in ChangeDictFrame

	places the user's selected dictionary/ies in to the current dictionary box

	argument:
		cdp -- reference to ChangeDictPanel
		evt -- event generated by event handler (EVT_LISTBOX_DCLICK or EVT_BUTTON)
	"""

	selection = list(cdp.unused_dict_box.GetSelections())
	selection.reverse()

	for s in selection:
		item = cdp.unusedDicts.pop(s)
		cdp.currDicts.append(item)

	cdp.unused_dict_box.Set(cdp.unusedDicts)
	cdp.curr_dict_box.Set(cdp.currDicts)

	cdp.parent.LAST = False


def removeDictHandler(cdp, evt):
	"""
	used in ChangeDictFrame

	places the user's selected dictionary/ies in to the unused dictionary box

	argument:
		cdp -- reference to ChangeDictPanel
		evt -- event generated by event handler (EVT_LISTBOX_DCLICK or EVT_BUTTON)
	"""

	selection = list(cdp.curr_dict_box.GetSelections())
	selection.reverse()

	for s in selection:
		item = cdp.currDicts.pop(s)
		cdp.unusedDicts.append(item)

	cdp.unused_dict_box.Set(cdp.unusedDicts)
	cdp.curr_dict_box.Set(cdp.currDicts)

	cdp.parent.LAST=False


def curr_sb_handler(cdp, evt):
	pass


def curr_dlb_handler(cdp, evt):
	pass


def unused_dlb_handler(cdp, evt):
	"""
	used in ChangeDictFrame

	method bound to when an item in the unused list box is clicked

	argument:
		cdp -- reference to ChangeDictPanel
		evt -- event generated by event handler (EVT_LISTBOX)
	"""

	print evt.GetEventObject().GetSelections()


def unused_sb_handler(cdp, evt):
	"""
	used in ChangeDictFrame

	method bound to when the user types in the searh bar for the unused dictionaries
	hides items that doesn't match the user's search query

	argument:
		cdp -- reference to ChangeDictPanel
		evt -- event generated by event handler (EVT_TEXT)
	"""

	if evt.GetEventObject().GetValue() in cdp.unusedDicts:
		#pass
		cdp.unused_dict_search_bar.SetBackgroundColour((0,255,0))
		cdp.unused_dict_search_bar.SetForegroundColour((0,0,0))#text color

	else:
		#pass
		cdp.unused_dict_search_bar.SetBackgroundColour((255,0,0))
		cdp.unused_dict_search_bar.SetForegroundColour((255,255,255))#text color

	item_list = cdp.unusedDicts

	pattern = re.compile(evt.GetEventObject().GetValue())
	cdp.unused_dict_box.Set([item  for item in item_list if re.search(pattern, item) is not None])

	cdp.Refresh()


def changeDictHandler(panel):
	"""
	used in wxHiraganaMemorization/MainFrame

	launches ChangeDictFrame for the user to change which dictionaries they want to use

	argument:
		panel -- MainPanel
	"""

	panel.cdf.unused_dict_search_bar.SetValue("")
	panel.cdf.Center()
	panel.cdf.Show()


def hideDefinitionHandler(frame, panel):
	"""
	used in wxHiraganaMemorization/MainFrame

	un/hides the english definition for the word

	argument:
		frame -- MainFrame
		panel -- MainPanel
	"""

	if frame.hideDefinitionMenuItem.IsChecked():
		frame.hideDefinitionMenuItem.Check()
		panel.currWordLabel.Hide()
		panel.prevWordLabel.Hide()

	else:
		frame.hideDefinitionMenuItem.Check(False)
		panel.currWordLabel.Show()
		panel.prevWordLabel.Show()

	panel.Layout()


def handleClickInputBox(evt):
	"""
	used in wxHiraganaMemorization/MainFrame

	method bound to when the input box gains focus either by user clicking it or tabbing in to it
	remove current contents of the input box on re-focus
	when not in focus the input box contains the instruction "Enter Syllables"

	argument:
		evt -- event generated by event handler (EVT_LEFT_DOWN or EVT_SET_FOCUS)

	"""

	evt.GetEventObject().SetValue("")
	evt.GetEventObject().SetFocus()


def handleInput(panel, evt):
	"""
	used in wxHiraganaMemorization/MainPanel

	method bound to when the user enters an answer in the input box

	if input is "quit" or "exit" terminate the program
	otherwise
		check if their answer is correct
		update the previous image container
		move on to the next word

	argument:
		panel -- reference to MainPanel
		evt -- event generated by event handler (EVT_TEXT_ENTER)
	"""

	userAns = evt.GetEventObject().GetValue().lower()
	evt.GetEventObject().SetValue("")
	evt.GetEventObject().SetFocus()

	if userAns == "quit" or userAns == "exit":
		panel.closeHandler()

	elif panel.LAST is False:
		checkAns(panel, userAns)
		nextPrevImgBox(panel)
		nextCurrImgBox(panel)

	else:
		print "No words remaining"


def generateCorrectAns(currWord):
	"""
	creates correct answer for the current word
	currWord is formatted so that it can be used to create the syllables
	e.g:
		"ta-be-ma-su"
		answer: "tabemasu"

	the special case that this method handles is the sokuon for repeating consonants
	e.g:
		ke-sokuon-ko-n
		answer: "kekkon"

	argument:
		currWord -- the word to generate a correct answer for

	returns the correct answer for the given currWord
	"""

	correctAns = ""
	vowels = ['a','e','o','i','u']
	tokens = currWord.split('-')
	for i in range(0,len(tokens)):

		if tokens[i] == "sokuon":
			if i<len(tokens)-1 and tokens[i+1][0] not in vowels:
				correctAns = correctAns+tokens[i+1][0]
			else:
				raise ValueError("Last syllable can't be a sokuon(little tsu) and must not be a vowel" + ". Tokens="+ str(tokens))
		else:
			correctAns = correctAns+tokens[i]

	return correctAns


def checkAns(panel, userAns):
	"""
	Checks if the users answer is correct
	Currently just prints feedback to command line

	argument:
		panel -- reference to MainPanel
		userAns -- user input
	"""

	correctAns=generateCorrectAns(panel.currWord)
	if userAns == correctAns:
		print "{userAns} is correct.".format(userAns=userAns)
	else:
		print "{userAns} is wrong. Correct answer is {correctAns}.".format(userAns=userAns, correctAns=correctAns)


def nextPrevImgBox(panel):
	"""
	updates the previous image container with the last word and images that were just used in the current image container

	argument:
		panel -- reference to MainPanel
	"""

	prevWord = panel.currWord
	prevDef = panel.definition

	panel.prevWordLabel.SetLabel(prevDef)

	fileList = panel.fileListForWord(prevWord)

	[img.Destroy() for img in panel.prevImgHolder]
	panel.prevImgHolder = []

	panel.drawWord(fileList, panel.prevImgSizer, panel.prevImgHolder)


def nextCurrImgBox(panel):
	"""
	updates the current image container with the next word taken from the dictionary

	argument:
		panel -- reference to MainPanel
	"""

	if len(panel.wordDict) > 0:
		panel.currWord = randChoice(panel.wordDict.keys())
		panel.definition = panel.wordDict[panel.currWord]
		panel.wordDict.pop(panel.currWord)

		panel.currWordLabel.SetLabel(panel.definition)

		fileList = panel.fileListForWord(panel.currWord)

		[img.Destroy() for img in panel.currImgHolder]
		panel.currImgHolder = []

		panel.drawWord(fileList, panel.currImgSizer, panel.currImgHolder)

	else:
		[img.Hide() for img in panel.prevImgHolder]
		[img.Hide() for img in panel.currImgHolder]

		panel.currWordLabel.SetLabel("")
		panel.prevWordLabel.SetLabel("No words remaining")
		panel.LAST = True
		panel.Layout()