import wx
from evtHandler import unused_sb_handler, unused_dlb_handler, curr_sb_handler, curr_dlb_handler, insertDictHandler, removeDictHandler
class ChangeDictFrame(wx.Frame):

	def __init__(self, parent=None, unusedDicts=[], currDicts=[]):
		self.parent=parent
		self.WindowSize=(400,600)
		self.LIST_BOX_SIZE=(100,200)
		self.LABEL_FONT_SIZE=12
		self.WX_FONT=wx.Font(self.LABEL_FONT_SIZE, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

		wx.Frame.__init__(self, parent, title="Change dictionary", size=self.WindowSize)

		self.topSizer = wx.BoxSizer(wx.VERTICAL)

		self.main_container = wx.BoxSizer(wx.HORIZONTAL)
		self.unusedDictSizer = wx.BoxSizer(wx.VERTICAL)
		self.midButtonSizer = wx.BoxSizer(wx.VERTICAL)
		self.currDictSizer = wx.BoxSizer(wx.VERTICAL)
		self.closeBtnSizer = wx.BoxSizer(wx.VERTICAL)

		self.currDicts=currDicts
		self.unusedDicts = unusedDicts

		self.addUnusedDictsLabel()
		self.addUnusedDictsSearchBar()
		self.addUnusedDictListBox()

		self.addInsertRemoveButtons()

		self.addCurrDictLabel()
		self.addCurDictSearchBar()
		self.addCurrDictListBox()
		self.addCloseBtn()

		self.main_container.Add(self.unusedDictSizer, flag=wx.ALIGN_CENTER | wx.EXPAND)
		self.main_container.Add(self.midButtonSizer, flag=wx.ALIGN_CENTER)
		self.main_container.Add(self.currDictSizer, flag=wx.ALIGN_CENTER | wx.EXPAND)

		ac_height = self.main_container.GetMinSize()[1]
		self.topSizer.Add(self.main_container, flag=wx.ALIGN_CENTER | wx.TOP, border=(self.WindowSize[1]-ac_height)/2)

		self.topSizer.AddStretchSpacer()
		self.topSizer.Add(self.closeBtnSizer, flag=wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT)

		self.SetSizer(self.topSizer)
		self.Layout()

		self.Bind(wx.EVT_CLOSE, self.closeChangeDict)

	def addUnusedDictsLabel(self):

		self.unused_dict_label=wx.StaticText(self, label="Unused")
		self.unused_dict_label.SetFont(self.WX_FONT)
		self.unusedDictSizer.Add(self.unused_dict_label, flag=wx.ALIGN_CENTER)

	def addUnusedDictsSearchBar(self):

		self.unused_dict_search_bar=wx.TextCtrl(self)
		self.unused_dict_search_bar.Bind(wx.EVT_TEXT, lambda evt :unused_sb_handler(self, evt) )

		self.unusedDictSizer.Add(self.unused_dict_search_bar, flag=wx.ALIGN_CENTER)

	def addUnusedDictListBox(self):

		self.unused_dict_box=wx.ListBox(self, choices=self.unusedDicts, size=self.LIST_BOX_SIZE, style=wx.LB_EXTENDED)
		self.unused_dict_box.Bind(wx.EVT_LISTBOX, lambda evt :unused_dlb_handler(self, evt) )

		self.unusedDictSizer.Add(self.unused_dict_box, flag=wx.ALIGN_CENTER)

	def addInsertRemoveButtons(self):

		self.insertDictBtn=wx.Button(self, label=">>")
		self.removeDictBtn=wx.Button(self, label="<<")

		self.midButtonSizer.Add(self.insertDictBtn, flag=wx.ALIGN_CENTER | wx.EXPAND)
		self.midButtonSizer.Add(self.removeDictBtn, flag=wx.ALIGN_CENTER | wx.EXPAND)

		self.removeDictBtn.Bind(wx.EVT_BUTTON, lambda evt :removeDictHandler(self, evt))
		self.insertDictBtn.Bind(wx.EVT_BUTTON, lambda evt :insertDictHandler(self, evt))

	def addCurrDictLabel(self):

		self.curr_dict_label=wx.StaticText(self, label="Current")
		self.curr_dict_label.SetFont(self.WX_FONT)
		self.currDictSizer.Add(self.curr_dict_label, flag=wx.ALIGN_CENTER)

	def addCurDictSearchBar(self):

		self.curr_dict_search_bar=wx.TextCtrl(self)
		self.curr_dict_search_bar.Bind(wx.EVT_TEXT, lambda evt : curr_sb_handler(self, evt) )

		self.currDictSizer.Add(self.curr_dict_search_bar, flag=wx.ALIGN_CENTER)

	def addCurrDictListBox(self):

		self.curr_dict_box=wx.ListBox(self, choices=self.currDicts, size=self.LIST_BOX_SIZE, style=wx.LB_EXTENDED)
		self.curr_dict_box.Bind(wx.EVT_LISTBOX, lambda evt :curr_dlb_handler(self, evt) )

		self.currDictSizer.Add(self.curr_dict_box, flag=wx.ALIGN_CENTER)

	def addCloseBtn(self):

		self.closeBtn=wx.Button(self, label="Close")
		self.closeBtn.Bind(wx.EVT_BUTTON, lambda evt :self.closeChangeDict(evt))

		self.closeBtnSizer.Add(self.closeBtn, flag=wx.ALIGN_BOTTOM)

	def closeChangeDict(self, evt):

		if self.parent == None:
			self.Destroy()
		else:
			self.parent.loadSymDicts()
			self.Hide()


if __name__ == "__main__":
	app = wx.App(False)
	frame = ChangeDictFrame()
	frame.Show()
	app.MainLoop()