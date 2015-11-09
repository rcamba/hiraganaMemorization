from ConfigParser import RawConfigParser
from os import path
import wx
from evtHandler import statsBtnHandler, changesDictBtnHandler, resetToggleOpt, hideDefinitionHandler, hideSyllableImgHandler, handleClickInputBox, handleInput
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
		self.unusedDicts = ["test"]
		self.currDicts = ["verbs"]
		self.cdf = ChangeDictFrame(self, self.unusedDicts, self.currDicts)

		#self.confParser = RawConfigParser()
		#self.configFile = pathToModule+"/../config.conf"
		#self.confParser.read(self.configFile)
		self.imgBoxSize = (800,100)
		self.inputTxtSize = (800,32)
		self.symDictPath = path.join(pathToModule,"symDicts")
		self.symImgPath = path.join(pathToModule,"symImg")
		self.currWord = ""
		self.definition = ""
		self.img_box_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.LAST = False

		self.currImgHolder = []
		self.prevImgHolder = []

		self.loadSymDicts()
		self.hideSyllableImgFlag = False

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

		self.imgBoxSizer.Add(self.currImgNLabelSizer, flag=wx.ALIGN_CENTRE)
		self.imgBoxSizer.Add(self.inputTxtSizer, flag=wx.ALIGN_CENTRE)

		self.topSizer.Add(self.imgBoxSizer, proportion=1, flag=wx.ALIGN_CENTRE)

		self.SetSizer(self.topSizer)
		self.Layout()

		self.Bind(wx.EVT_CLOSE, self.closeHandler)
		self.cdf.Hide()

	def closeHandler(self,evt=None):
		self.parent.Destroy()

	def loadSymDicts(self):
		temp = {}
		self.wordDict = {}
		for file in self.currDicts:
			d = open( path.join(self.symDictPath,file) ).read().replace("\n","")
			d = d.lower()
			exec("temp="+"{"+d+"}")
			self.wordDict.update(temp)

	def getImage(self, filename):
		img = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
		imgRes = wx.StaticBitmap(self, -1, img, (img.GetWidth(), img.GetHeight()))
		return imgRes

	def drawWord(self, fileList, targSizer, storage, hidden=False):
		for f in fileList:
			imgObj = self.getImage(path.join(self.symImgPath,f))
			if hidden:
				imgObj.Hide()
			storage.append(imgObj)
			targSizer.Add(imgObj, proportion=0, flag=wx.ALL, border=0)

		if self.hideSyllableImgFlag is False:
			[img.Show() for img in storage]

		self.imgBoxSizer.Layout()
		self.Layout()

	def fileListForWord(self, word):
		return [syllable.lower() + ".png" for syllable in word.split('-')]

	def addCurrImgBox(self):
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
		self.prevWordLabel = wx.StaticText(self)
		self.prevWordLabel.SetFont(self.img_box_font)

		self.prevWordLabel.SetLabel("")
		self.prevImgNLabelSizer.Add(self.prevWordLabel, flag=wx.ALIGN_CENTRE)

		self.prevImgNLabelSizer.Add(self.prevImgSizer, flag=wx.ALIGN_CENTRE)

	def addInputTxt(self):
		self.inputTxt = wx.TextCtrl(self, size=self.inputTxtSize, style=wx.TE_PROCESS_ENTER)
		self.inputTxt.SetValue("Enter syllables")

		self.inputTxt.Bind(wx.EVT_TEXT_ENTER, lambda evt :handleInput(self, evt) )
		self.inputTxt.Bind(wx.EVT_KILL_FOCUS, lambda evt : evt.GetEventObject().SetValue("Enter syllables"))

		self.inputTxt.Bind(wx.EVT_LEFT_DOWN, handleClickInputBox)
		self.inputTxt.Bind(wx.EVT_SET_FOCUS, handleClickInputBox)

		self.inputTxt.SetFocus()

		self.inputTxtSizer.Add(self.inputTxt, proportion=0, flag=wx.ALL, border=25)


class MainFrame(wx.Frame):
	def __init__(self):
		self.WindowSize = (1175,400)
		wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="Hiragana Memorization", size=self.WindowSize, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)#use default frame style but disable border resize and maximize

		self.addMenuBar()

		self.mp = MainPanel(self)
		self.Center()
		self.Show()

	def addMenuBar(self):
		self.menuBar = wx.MenuBar()
		self.gameOptionsMenu = wx.Menu()
		self.menuBar.Append(self.gameOptionsMenu, "Game Op&tions")
		self.SetMenuBar(self.menuBar)


if __name__ == "__main__":
	app = wx.App(False)
	frame = MainFrame()
	frame.Show()
	app.MainLoop()