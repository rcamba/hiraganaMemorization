def hideDefinitionHandler(obj):
	print "hideDefinitionHandler"

def hideRomajiHandler(obj):
	print "hideRomajiHandler"

def handleClickInputBox(evt):
	evt.GetEventObject().SetValue("")
	evt.GetEventObject().SetFocus()