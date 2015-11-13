from ConfigParser import RawConfigParser
from os import path, listdir
from string import strip

import wx
from wx.lib.agw.genericmessagedialog import GenericMessageDialog as GMD
from evtHandler import changeDictHandler, hideDefinitionHandler, handleClickInputBox, handleInput

from ChangeDictFrame import ChangeDictFrame
from random import choice as randChoice


pathToModule = path.dirname(__file__)
if len(pathToModule) == 0:
	pathToModule = '.'


class MainPanel(wx.Panel):

	def __init__(self, parent):
		self.parent = parent
		self.WindowSize = self.parent.WindowSize
		wx.Panel.__init__(self, parent)

		self.symDictPath = path.join(pathToModule,"symDicts")
		self.symImgPath = path.join(pathToModule,"symImg")

		self.unusedDicts = listdir(self.symDictPath)[:1]
		self.currDicts = listdir(self.symDictPath)[1:]
		self.cdf = ChangeDictFrame(self, self.unusedDicts, self.currDicts)

		#self.confParser = RawConfigParser()
		#self.configFile = pathToModule+"/../config.conf"
		#self.confParser.read(self.configFile)
		self.imgBoxSize = (800,100)
		self.inputTxtSize = (800,32)

		self.currWord = ""
		self.definition = ""
		self.img_box_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.LAST = False

		self.currImgHolder = []
		self.prevImgHolder = []

		self.loadSymDicts()

		self.topSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.prevImgSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.prevImgNLabelSizer = wx.BoxSizer(wx.VERTICAL)

		self.currImgSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.currImgNLabelSizer = wx.BoxSizer(wx.VERTICAL)

		self.imgBoxSizer = wx.BoxSizer(wx.VERTICAL)

		self.inputTxtSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.addPrevImgBox()
		self.addCurrImgBox()
		self.addInputTxt()

		self.imgBoxSizer.Add(self.prevImgNLabelSizer, flag=wx.ALIGN_CENTRE)
		self.imgBoxSizer.AddSpacer(20)
		self.imgBoxSizer.Add(self.currImgNLabelSizer, flag=wx.ALIGN_CENTRE)
		self.imgBoxSizer.Add(self.inputTxtSizer, flag=wx.ALIGN_CENTRE)

		self.topSizer.Add(self.imgBoxSizer, proportion=1, flag=wx.ALIGN_CENTRE)

		self.SetSizer(self.topSizer)
		self.Layout()

		self.Bind(wx.EVT_CLOSE, self.closeHandler)
		self.cdf.Hide()

	def closeHandler(self, evt=None):
		"""
		Method bound to closing event

		argument:
			evt -- generated event when this function is called by an event handler

		Destroys the parent - MainFrame
		"""

		self.parent.Destroy()

	def loadSymDicts(self):
		"""
		Load all dictionaries (from self.currDicts) in to self.wordDict
		self.currDicts contains the name of the dictionary files which is used to construct the full file path by joining the name with self.symDictPath
		"""

		temp = {}
		self.wordDict = {}
		for file in self.currDicts:
			lineList = open(path.join(self.symDictPath, file)).readlines()
			for line in lineList:
				japanesePhoneticWord, englishTranslation = map(strip, line.split(":"))
				self.wordDict[japanesePhoneticWord] = englishTranslation

	def getImage(self, filename):
		"""
		uses given filename argument to to create a bitmap image
		bitmap image is then used to create StaticBitmap

		args:
			filename -- the filename of the image

		returns StaticBitmap image for given filename
		"""

		img = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		imgRes = wx.StaticBitmap(self, -1, img, (img.GetWidth(), img.GetHeight()))
		return imgRes

	def drawWord(self, fileList, targSizer, storage):
		"""
		places images of syllables in to targSizer (prevImgSizer or currImgSizer)

		arguments:
			fileList -- list of files containing the syllables used to produce a word
			targSizer -- the sizer to add the images in to
			storage -- a list that holds the image objects themselves to prevent them from being garbage collected
		"""

		for f in fileList:
			imgObj = self.getImage(path.join(self.symImgPath,f))
			imgObj.Hide()  #hide all images until they are all ready to be shown
			storage.append(imgObj)
			targSizer.Add(imgObj, proportion=0, flag=wx.ALL, border=0)

		[img.Show() for img in storage]  #show all images once they have all been made

		self.imgBoxSizer.Layout()
		self.Layout()

	def fileListForWord(self, word):
		"""
		create syllables by splitting the word and then create the filenames for the syllables
		e.g:
			word = "ta-be-ma-su"
			syllables = [ta, be, ma, su]
			list of filenames = [ta.png, be.png, ma.png, su.png]

		arguments:
			word -- the word to be used to create syllables from

		returns a list of filenames for each syllable to construct the given word
		"""
		return [syllable.lower()+".png" for syllable in word.split('-')]

	def addCurrImgBox(self):
		"""
		create the container that will hold the current word/image of syllables
		the chosen starting word is initalized by random selection from self.wordDict
		create sylabble images for the word and add them to the self.currImgSizer which will display the images
		"""

		self.currWord = randChoice(self.wordDict.keys())
		self.definition = self.wordDict[self.currWord]
		self.wordDict.pop(self.currWord)

		self.currWordLabel = wx.StaticText(self)
		self.currWordLabel.SetFont(self.img_box_font)

		fileList = self.fileListForWord(self.currWord)

		self.drawWord(fileList, self.currImgSizer, self.currImgHolder)
		self.currImgNLabelSizer.Add(self.currImgSizer, flag=wx.ALIGN_CENTRE)

		self.currWordLabel.SetLabel(self.definition)
		self.currImgNLabelSizer.Add(self.currWordLabel, flag=wx.ALIGN_CENTRE)

	def addPrevImgBox(self):
		"""
		create the container that will hold the previous word/image of syllables after the user enters their first input
		"""

		self.prevWordLabel = wx.StaticText(self)
		self.prevWordLabel.SetFont(self.img_box_font)

		self.prevWordLabel.SetLabel("")
		self.prevImgNLabelSizer.Add(self.prevWordLabel, flag=wx.ALIGN_CENTRE)

		self.prevImgNLabelSizer.Add(self.prevImgSizer, flag=wx.ALIGN_CENTRE)

	def addInputTxt(self):
		"""
		create the textbox that the user will use to enter their answer
		"""

		self.inputTxt = wx.TextCtrl(self, size=self.inputTxtSize, style=wx.TE_PROCESS_ENTER)
		self.inputTxt.SetValue("Enter syllables")

		self.inputTxt.Bind(wx.EVT_TEXT_ENTER, lambda evt :handleInput(self, evt) )
		self.inputTxt.Bind(wx.EVT_KILL_FOCUS, lambda evt : evt.GetEventObject().SetValue("Enter syllables"))

		self.inputTxt.Bind(wx.EVT_LEFT_DOWN, handleClickInputBox)
		self.inputTxt.Bind(wx.EVT_SET_FOCUS, handleClickInputBox)

		self.inputTxt.SetFocus()

		self.inputTxtSizer.Add(self.inputTxt, proportion=0, flag=wx.ALL, border=25)

	def displayAlert(self, alertMsg):
		"""
		Displays warning message as a popup

		arguments:
				alertMsg -- message to display in dialog message box

		no return value
		"""

		self.alertDlg = GMD(
			parent=self, message=alertMsg, caption="Alert!",
			agwStyle=wx.OK | wx.ICON_EXCLAMATION)

		self.alertDlg.ShowModal()
		if self.alertDlg:
			self.alertDlg.Destroy()


class MainFrame(wx.Frame):
	def __init__(self):
		self.WindowSize = (1175, 450)
		wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="Hiragana Memorization", size=self.WindowSize, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)#use default frame style but disable border resize and maximize

		self.HIDE_DEFINITION_ID = 1
		self.CHANGE_DICT_ID = 2
		self.VIEW_STATS_ID = 3
		self.VIEW_HIRAGANA_CHART_ID = 4

		self.mp = MainPanel(self)

		self.addMenuBar()
		self.addHideDefOption()
		self.addChangeDictOption()
		self.addViewStats()
		self.addViewHiraganaChart()

		self.Center()
		self.Show()

	def addMenuBar(self):
		"""
		create the menu bar and menus
		"""

		self.menuBar = wx.MenuBar()
		self.gameOptionsMenu = wx.Menu()
		self.viewMenu = wx.Menu()
		self.menuBar.Append(self.gameOptionsMenu, "Game Op&tions")
		self.menuBar.Append(self.viewMenu, "&View")
		self.SetMenuBar(self.menuBar)

	def addHideDefOption(self):
		"""
		togglable menu bar option for hiding the definition of the word
		Game Options -> Hide definition
		Shortcut: Ctrl+F or ALT+T+F
		"""

		self.hideDefinitionMenuItem = wx.MenuItem(self.gameOptionsMenu, self.HIDE_DEFINITION_ID, "Hide de&finition\tCtrl+F", kind=wx.ITEM_CHECK)
		self.gameOptionsMenu.AppendItem(self.hideDefinitionMenuItem)
		self.hideDefinitionMenuItem.Check(False)
		self.Bind(wx.EVT_MENU, lambda evt: hideDefinitionHandler(self, self.mp), id=self.HIDE_DEFINITION_ID)

		self.gameOptionsMenu.AppendSeparator()

	def addChangeDictOption(self):
		"""
		menu bar option that launches ChangeDictFrame which allows the user to change which dictionaries they want to use
		Game Options -> Change dictionary
		Shortcut: Ctrl+D or ALT+T+D
		"""

		self.changeDictMenuItem = wx.MenuItem(self.gameOptionsMenu, self.CHANGE_DICT_ID, "Change &dictionary\tCtrl+D")
		self.gameOptionsMenu.AppendItem(self.changeDictMenuItem)
		self.Bind(wx.EVT_MENU, lambda evt: changeDictHandler(self.mp), id=self.CHANGE_DICT_ID)

	def addViewStats(self):
		"""
		menu bar option for viewing stats
		WIP
		"""

		self.viewStatsMenuItem = wx.MenuItem(self.viewMenu, self.VIEW_STATS_ID, "&Statistics")
		self.viewMenu.AppendItem(self.viewStatsMenuItem)
		self.Bind(wx.EVT_MENU, lambda evt: self.mp.displayAlert("Work in Progress"), id=self.VIEW_STATS_ID)


	def addViewHiraganaChart(self):
		"""
		menu bar option for viewing hiragana characters
		"""

		self.viewHirChartMenuItem = wx.MenuItem(self.viewMenu, self.VIEW_HIRAGANA_CHART_ID, "&Hiragana Chart")
		self.viewMenu.AppendItem(self.viewHirChartMenuItem)
		self.Bind(wx.EVT_MENU, lambda evt: self.mp.displayAlert("Work in Progress"), id=self.VIEW_HIRAGANA_CHART_ID)


if __name__ == "__main__":
	app = wx.App(False)
	frame = MainFrame()
	frame.Show()
	app.MainLoop()