import wx
from evtHandler import searchBarHandler, unusedDictBoxHandler, insertDictBtnHandler, removeDictHandler
class ChangeDictFrame(wx.Frame):

	#renaming on unused/used?
	def __init__(self, parent=None, dictList=[]):
		self.parent=parent
		self.WindowSize=(400,600)
		self.LIST_BOX_SIZE=(100,200)

		wx.Frame.__init__(self, parent, title="Change dictionary", size=self.WindowSize)

		self.topSizer = wx.BoxSizer(wx.VERTICAL)

		self.all_container = wx.BoxSizer(wx.HORIZONTAL)
		self.leftSizer = wx.BoxSizer(wx.VERTICAL)
		self.midButtonSizer = wx.BoxSizer(wx.VERTICAL)
		self.rightSizer = wx.BoxSizer(wx.VERTICAL)

		self.usedDictSizer = wx.BoxSizer(wx.VERTICAL)

		self.dictList=dictList#temp, get from parent (which loads from config file)
		self.addSearchBar()
		self.addCloseBtn()
		self.addUnusedDictListBox()
		self.addInsertRemoveButtons()
		self.addUsedSearchBar()
		self.addUsedDictLisBox()


		self.all_container.Add(self.leftSizer, flag=wx.ALIGN_CENTER | wx.EXPAND)
		self.all_container.Add(self.midButtonSizer, flag=wx.ALIGN_CENTER)
		self.all_container.Add(self.usedDictSizer, flag=wx.ALIGN_CENTER | wx.EXPAND)

		ac_height = self.all_container.GetMinSize()[1]
		self.topSizer.Add(self.all_container, flag=wx.ALIGN_CENTER | wx.TOP, border=(self.WindowSize[1]-ac_height)/2)

		self.topSizer.AddStretchSpacer()
		self.topSizer.Add(self.rightSizer, flag=wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT)

		self.SetSizer(self.topSizer)
		self.Layout()

		self.Bind(wx.EVT_CLOSE, self.closeChangeDict)

	def addSearchBar(self):
		self.searchBar=wx.TextCtrl(self)

		self.searchBar.Bind(wx.EVT_TEXT, lambda evt :searchBarHandler(self, evt) )

		self.leftSizer.Add(self.searchBar, flag=wx.ALIGN_CENTER)

	def addCloseBtn(self):
		self.closeBtn=wx.Button(self, label="Close")
		self.closeBtn.Bind(wx.EVT_BUTTON, lambda evt :self.closeChangeDict(evt))

		self.rightSizer.Add(self.closeBtn, flag=wx.ALIGN_BOTTOM)

	def addUnusedDictListBox(self):
		self.unusedDictBox=wx.ListBox(self, choices=self.dictList, size=self.LIST_BOX_SIZE, style=wx.LB_EXTENDED)
		self.leftSizer.Add(self.unusedDictBox, flag=wx.ALIGN_CENTER)
		self.unusedDictBox.Bind(wx.EVT_LISTBOX, lambda evt :unusedDictBoxHandler(self, evt) )

	def addInsertRemoveButtons(self):
		self.insertDictBtn=wx.Button(self, label=">>")
		self.removeDictBtn=wx.Button(self, label="<<")

		self.midButtonSizer.Add(self.insertDictBtn, flag=wx.ALIGN_CENTER | wx.EXPAND)
		self.midButtonSizer.Add(self.removeDictBtn, flag=wx.ALIGN_CENTER | wx.EXPAND)

		self.removeDictBtn.Bind(wx.EVT_BUTTON, lambda evt :removeDictHandler(self, evt))
		self.insertDictBtn.Bind(wx.EVT_BUTTON, lambda evt :insertDictBtnHandler(self, evt))

	def addUsedSearchBar(self):
		self.usedSearchBar=wx.TextCtrl(self)

		#self.usedSearchBar.Bind(wx.EVT_TEXT, lambda evt :usedSearchBarHandler(self, evt) )

		self.usedDictSizer.Add(self.usedSearchBar, flag=wx.ALIGN_CENTER)

	def addUsedDictLisBox(self):

		self.usedDictBox=wx.ListBox(self, choices=self.dictList, size=self.LIST_BOX_SIZE, style=wx.LB_EXTENDED)

		#self.usedDictBox.Bind(wx.EVT_LISTBOX, lambda evt :usedDictBoxHandler(self, evt) )

		self.usedDictSizer.Add(self.usedDictBox, flag=wx.ALIGN_CENTER)

	def closeChangeDict(self, evt):

		if self.parent == None:
			self.Destroy()
		else:
			self.Hide()

if __name__ == "__main__":
	app = wx.App(False)
	frame = ChangeDictFrame()
	frame.Show()
	app.MainLoop()