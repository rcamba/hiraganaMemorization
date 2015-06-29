import wx
from evtHandler import searchBarHandler
class ChangeDictFrame(wx.Frame):

	def __init__(self, parent=None, dictList=["verbs"]):
		self.parent=parent
		self.WindowSize=(400,600)
		#wx.Panel.__init__(self, parent)
		wx.Frame.__init__(self, parent, title="Change dictionary", size=self.WindowSize)

		self.topSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.leftSizer = wx.BoxSizer(wx.VERTICAL)
		self.rightSizer = wx.BoxSizer(wx.VERTICAL)

		self.dictList=dictList#temp, get from parent (which loads from config file)
		self.addSearchBar()
		self.addCloseBtn()


		self.topSizer.Add(self.leftSizer)
		self.topSizer.Add(self.rightSizer)

		self.SetSizer(self.topSizer)
		self.Layout()

		self.Bind(wx.EVT_CLOSE, self.closeChangeDict)

	def addSearchBar(self):
		self.searchBar=wx.TextCtrl(self)

		self.searchBar.Bind(wx.EVT_TEXT, lambda evt :searchBarHandler(self, evt) )

		self.leftSizer.Add(self.searchBar)

	def addCloseBtn(self):
		self.closeBtn=wx.Button(self, label="Close")
		self.closeBtn.Bind(wx.EVT_BUTTON, lambda evt :self.closeChangeDict(evt))

		self.rightSizer.Add(self.closeBtn)

	def closeChangeDict(self, evt):
		self.Hide()

if __name__ == "__main__":
	app = wx.App(False)
	frame = ChangeDictFrame()
	frame.Show()
	app.MainLoop()