def hideDefinitionHandler(obj):
	print "hideDefinitionHandler"

def hideRomajiHandler(obj):
	print "hideRomajiHandler"

def handleClickInputBox(evt):
	evt.GetEventObject().SetValue("")
	evt.GetEventObject().SetFocus()


def fileListForWord(word):
	return [syllable.lower()+".png" for syllable in word.split('-')]

def correctAnsForFileList(fileList):

	word=""
	vowels=['a','e','o','i','u']

	for i in range (0,len(fileList)) :
		fileList[i]=fileList[i].replace(".png","")

		if fileList[i]=="minitsu":
			if i<len(fileList)-1:
				if fileList[i+1][0] not in vowels:
					word=word+(fileList[i+1][0])
				else:
					raise ValueError("Last syllable must not be a vowel")
			else:
				raise ValueError("Last syllable can't be a Sokuon(little tsu)")

		else:
			word=word+(fileList[i])

	return word

def drawNextWord(wordDict):
	randWord=randChoice(wordDict.keys())
	wordDict.pop(randWord)
	fileList=fileListForWord(randWord)

	return fileList

