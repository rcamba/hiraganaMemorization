import wx
from evtHandler import *
class ChangeDictPanel(wx.Panel):

	def __init__(self, parent, dictList=["verb"]):
		self.parent=parent
		wx.Panel.__init__(self, parent)
		self.dictList=dictList#temp, get from parent (which loads from config file)
		self.addSearchBar()

	def addSearchBar(self):
		self.searchBar=wx.TextCtrl(self)


		self.searchBar.Bind(wx.EVT_TEXT, lambda evt :searchBarHandler(self, evt) )


class MainFrame(wx.Frame):
	def __init__(self):
		self.WindowSize=(400,600)
		wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="Change dictionary", size=self.WindowSize, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)#use default frame style but disable border resize and maximize

		self.cdp=ChangeDictPanel(self)
		self.Center()
		self.Show()


if __name__ == "__main__":
	app = wx.App(False)
	frame = MainFrame()
	frame.Show()
	app.MainLoop()