from ConfigParser import RawConfigParser
from os import path
import wx
from hm_eventHandlers import *

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



		self.topSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.toggleOptSizer = wx.BoxSizer(wx.VERTICAL)

		self.prevImgBoxSizer = wx.BoxSizer(wx.VERTICAL)
		self.currImgBoxSizer= wx.BoxSizer(wx.VERTICAL)
		self.imgBoxSizer= wx.BoxSizer(wx.VERTICAL)

		self.clickableOptSizer= wx.BoxSizer(wx.VERTICAL)

		self.inputTxtSizer = wx.BoxSizer(wx.HORIZONTAL)



		self.addToggleOptions()
		self.addPrevImgBox()
		self.addClickableOptions()
		self.addCurrImgBox()
		self.addInputTxt()



		self.topSizer.Add(self.toggleOptSizer)

		self.imgBoxSizer.Add(self.prevImgBoxSizer)
		self.imgBoxSizer.Add(self.currImgBoxSizer)
		self.imgBoxSizer.Add(self.inputTxtSizer)

		self.topSizer.Add(self.imgBoxSizer, flag=wx.ALIGN_CENTRE)

		self.topSizer.Add(self.clickableOptSizer)


		self.SetSizer(self.topSizer)
		self.Layout()

		#self.parent.Bind(wx.EVT_CLOSE, self.closeHandler)


	def addToggleOptions(self):
		"""

		"""

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

	def addPrevImgBox(self):
		self.placeHolder= wx.TextCtrl(self, size=(500,100))
		self.prevImgBoxSizer.Add(self.placeHolder, proportion=0, flag=wx.ALL, border=25)

	def addClickableOptions(self):
		self.statsButton =wx.Button(self, label="View Statistics")
		self.changeDict =wx.Button(self, label="Change dictionary")

		self.clickableOptSizer.Add(self.statsButton ,proportion=0, flag=wx.ALL, border=20)
		self.clickableOptSizer.Add(self.changeDict,proportion=0, flag=wx.ALL, border=20)

	def addCurrImgBox(self):
		self.currplaceHolder= wx.TextCtrl(self, size=(500,100))
		self.currImgBoxSizer.Add(self.currplaceHolder, proportion=0, flag=wx.ALL, border=25)

	def addInputTxt(self):
		self.inputTxt= wx.TextCtrl(self, size=(500,32))
		self.inputTxt.SetValue("Enter syllables")

		self.inputTxt.Bind(wx.EVT_LEFT_DOWN, handleClickInputBox, self.inputTxt)
		self.inputTxt.Bind(wx.EVT_SET_FOCUS, handleClickInputBox)
		self.inputTxt.Bind(wx.EVT_KILL_FOCUS, lambda evt : evt.GetEventObject().SetValue("Enter syllables"))

		self.inputTxtSizer.Add(self.inputTxt, proportion=0, flag=wx.ALL, border=25)



class MainFrame(wx.Frame):
	def __init__(self):
		self.WindowSize=(875,400)
		wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="Hiragana Memorization", size=self.WindowSize, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)#use default frame style but disable border resize and maximize

		self.mp=MainPanel(self)
		self.Center()
		self.Show()


if __name__ == "__main__":
	app = wx.App(False)
	frame = MainFrame()
	frame.Show()
	app.MainLoop()