import wx
from hiraganaMemorization.wxHiraganaMemorization import MainFrame

if __name__ == "__main__":
	app = wx.App(False)
	frame = MainFrame()
	frame.Show()
	app.MainLoop()