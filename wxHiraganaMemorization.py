from ConfigParser import RawConfigParser
from os import path
import wx
from evtHandler import *


pathToModule=path.dirname(__file__)
if len(pathToModule)==0:
	pathToModule='.'


class MainPanel(wx.Panel):

	def __init__(self, parent):
		self.parent=parent
		wx.Panel.__init__(self, parent)

		#self.confParser=RawConfigParser()
		#self.configFile=pathToModule+"/../config.conf"
		#self.confParser.read(self.configFile)
		self.imgBoxSize=(800,100)
		self.symDictPath=path.join(pathToModule,"symDicts")
		self.symImgPath=path.join(pathToModule,"symImg")
		self.prevWord=""
		self.definition=""

		self.topSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.toggleOptSizer = wx.BoxSizer(wx.VERTICAL)


		self.prevImgSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.prevImgNLabelSizer = wx.BoxSizer(wx.VERTICAL)

		self.currImgSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.currImgNLabelSizer = wx.BoxSizer(wx.VERTICAL)

		self.imgBoxSizer= wx.BoxSizer(wx.VERTICAL)

		self.clickableOptSizer = wx.BoxSizer(wx.VERTICAL)

		self.inputTxtSizer = wx.BoxSizer(wx.HORIZONTAL)

		#self.imgHolder=[]
		#self.prevImgHolder=[]
		#self.defaultDict=["verbs"]
		#self.wordDict=self.loadSymDicts()

		self.addToggleOptions()
		#self.addPrevImgBox()
		#self.addClickableOptions()
		#self.addCurrImgBox()
		#self.addInputTxt()


		self.topSizer.Add(self.toggleOptSizer)

		self.imgBoxSizer.Add(self.prevImgNLabelSizer, flag=wx.ALIGN_CENTRE)
		self.imgBoxSizer.Add(self.currImgNLabelSizer, flag=wx.ALIGN_CENTRE)
		self.imgBoxSizer.Add(self.inputTxtSizer, flag=wx.ALIGN_CENTRE)

		self.topSizer.Add(self.imgBoxSizer, flag=wx.ALIGN_CENTRE)

		self.topSizer.Add(self.clickableOptSizer)

		self.SetSizer(self.topSizer)
		self.Layout()

		#self.parent.Bind(wx.EVT_CLOSE, self.closeHandler)

	def addToggleOptions(self):

		self.hideRomaji= wx.CheckBox(parent=self, id=-1, label="Hide romaji")
		self.hideDefinition= wx.CheckBox(parent=self, id=-1, label="Hide definition")


		self.toggleOptSizer.Add(self.hideRomaji, proportion=0, flag=wx.ALL, border=20)
		self.toggleOptSizer.Add(self.hideDefinition, proportion=0, flag=wx.ALL, border=20)


		self.Bind(wx.EVT_CHECKBOX, hideRomajiHandler, self.hideRomaji)

		self.Bind(wx.EVT_CHECKBOX, hideDefinitionHandler, self.hideDefinition)

		tip="Hide english definition of the world"
		self.hideDefinition.SetToolTipString(tip)

		tip="Hide phonetic pronounciation of the word"
		self.hideRomaji.SetToolTipString(tip)

	'''
	def addPrevImgBox(self):

		imgFile=self.getImage(path.join(pathToModule,"symImg","ko.png"),True)
		self.prevImgSizer.Add(imgFile, proportion=0, flag=wx.ALL)
		self.prevImgNLabelSizer.Add(self.prevImgSizer)
		#imgFile.Destroy()


	def addClickableOptions(self):
		self.statsButton =wx.Button(self, label="View Statistics")
		self.changeDict =wx.Button(self, label="Change dictionary")

		self.clickableOptSizer.Add(self.statsButton ,proportion=0, flag=wx.ALL, border=20)
		self.clickableOptSizer.Add(self.changeDict,proportion=0, flag=wx.ALL, border=20)



	def getImage(self, filename, n=False):
		img = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()

		imgRes=wx.StaticBitmap(self, -1, img, (img.GetWidth(), img.GetHeight()))
		if n==False:

			imgRes.Hide()
			self.imgHolder.append(imgRes)
			self.prevImgHolder.append(wx.StaticBitmap(self, -1, img, (img.GetWidth(), img.GetHeight())))
		return imgRes

	def drawImage(self, imageFileName, targSizer):

		imgObj=self.getImage(path.join(self.symImgPath,imageFileName))
		#print dir(imgObj)



		targSizer.Add(imgObj, proportion=0, flag=wx.ALL, border=0)



	def addCurrImgBox(self):

		randWord=randChoice(self.wordDict.keys())
		self.prevWord=randWord
		self.definition=self.wordDict[randWord]
		self.randWordLabel=wx.StaticText(self)
		self.randWordLabel.SetLabel(self.wordDict[randWord])
		self.wordDict.pop(randWord)
		fileList=fileListForWord(randWord)

		font=wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTWEIGHT_NORMAL, wx.FONTWEIGHT_NORMAL)
		self.randWordLabel.SetFont(font)
		self.currImgNLabelSizer.Add(self.randWordLabel, flag=wx.ALIGN_CENTRE)

		for filename in fileList:
			self.drawImage(filename, self.currImgSizer)

		for i in self.imgHolder[:]:
			i.Show()

		self.currImgNLabelSizer.Add(self.currImgSizer)



	def addInputTxt(self):
		self.inputTxt= wx.TextCtrl(self, size=(800,32), style=wx.TE_PROCESS_ENTER)
		self.inputTxt.SetValue("Enter syllables")


		self.inputTxt.Bind(wx.EVT_TEXT_ENTER, lambda evt :handleInput(self, evt) )
		self.inputTxt.Bind(wx.EVT_LEFT_DOWN, handleClickInputBox)
		self.inputTxt.Bind(wx.EVT_SET_FOCUS, handleClickInputBox)
		self.inputTxt.Bind(wx.EVT_KILL_FOCUS, lambda evt : evt.GetEventObject().SetValue("Enter syllables"))

		self.inputTxt.SetFocus()

		self.inputTxtSizer.Add(self.inputTxt, proportion=0, flag=wx.ALL, border=25)

	'''

class MainFrame(wx.Frame):
	def __init__(self):
		self.WindowSize=(1175,400)
		wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="Hiragana Memorization", size=self.WindowSize, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)#use default frame style but disable border resize and maximize

		self.mp=MainPanel(self)
		self.Center()
		self.Show()


if __name__ == "__main__":
	app = wx.App(False)
	frame = MainFrame()
	frame.Show()
	app.MainLoop()