from Tkinter import *
import Image
import ImageTk
import tkMessageBox

from copy import deepcopy
from os import listdir, chdir, system, getcwd, path
from random import randint, choice as randChoice
from time import sleep
from threading import Thread
from sys import argv 

from collections import OrderedDict

"""
TODO: 
	add scoring
	create log to display which characters that I make mistakes on
	input will now have to be separated in spaces to allow counting mistakes to create the log
"""

wD={"ta-be-ma-su":"to eat", 
"na-ra-i-ma-su":"to learn", 
"wa-su-re-ma-su":"to forget", 
"no-mi-ma-su":"to drink", 
"ka-i-ma-su":"to buy", 
"mi-ma-su":"to watch, look,see", 
"mi-se-ma-su":"to show",
"ka-ki-ma-su":"to write, draw, paint",
"o-ku-ri-ma-su":"to send",
"tsu-ku-ri-ma-su":"to make, produce, cook",
"tsu-ka-i-ma-su":"to use",
"i-ki-ma-su":"to go",
"ki-ma-su":"to come",
"ka-e-ri-ma-su":"to return",
"a-ri-ma-su":"to have, be at, exist(inanimate object)",
"i-ma-su":"to have, be at, exist(animate object)",
"ha-na-shi-ma-su":"to talk, speak",
"ya-ku-shi-ma-su":"to translate",
"ne-ma-su":"to lie down, go to bed",
"o-ki-ma-su":"to get up, wake up, happen, occur",
"ko-wa-re-ma-su":"to be broken",
"na-o-shi-ma-su":"to repair, fix",
"a-ge-ma-su":"to give, present/ to raise, lift up",
"mo-ra-i-ma-su":"to receive, be given",
"ka-ri-ma-su":"to borrow, rent",
"a-ga-ri-ma-su":"to go up, rise",
"sa-ga-ri-ma-su":"to go down, drop"
}

class ErrorList:
	
	def __init__(self, characterEr, erCount):
		self.characterError=characterEr
		self.count=int(erCount)
	
	@staticmethod	
	def load(errorLogFile):
		
		errorList=[]
		dataError=open(errorLogFile).read().split('\n')
		
		for data in dataError:
			
			dataSplit=data.split(':')
			if (len(dataSplit)>1 ):
				errorList.append(ErrorList(dataSplit[0],dataSplit[1]))
			
		return errorList
	
	@staticmethod	
	def writeLog(errorLogFile, errorList):
		#writes errorList to errorLog
		writer=open(errorLogFile,'w')
		for err in errorList:
			
			writer.write("".join([err.getCharacter(),':',str(err.getCount())]))
			writer.write('\n')
		writer.close()
		
	def getCharacter(self):
		return self.characterError
		
	def getCount(self):
		return self.count
		
	def increaseCount(self):
		self.count=int(self.count)+1
			
	def __str__(self):
		return "".join([ self.characterError, ':', str(self.count)])

def createLog(userAns):
	
	uAnsList=userAns.split()
	cAnsList=correctAns.split()
	
	for i in range(0,len(uAnsList)):
		if(uAnsList[i].lower()!=cAnsList[i].lower()):
			increaseErrorCount(cAnsList[i])
			
def increaseErrorCount(error):
	#finds the error in the log and increases it by 1
	eList=ErrorList.load(mistakesLog)
	
	for e in eList:
		if(e.getCharacter().lower()==error.lower()):
			e.increaseCount()
			
			break
	
	ErrorList.writeLog(mistakesLog, eList)

prevCanvas=None
deletePrev=False
def handleUserInput(master, canvas, textFrame, inputBox, inputLabel, imgFileList, wordFileDict):
	
	global prevCanvas
	global canvasCount
	global deletePrev
	
	userInput=inputBox.get()
	
	if userInput!="quit":	
		print userInput
		
		correctAns= " ".join(  wordFileDict.keys() )
		if correctAns==userInput:
			print "Correct"
		
		else:
			print "Wrong. Answer is: ", correctAns
		
		
		if deletePrev==False:
			deletePrev=True
			if prevCanvas!=None:
				prevCanvas=canvas
				canvas.destroy()
			else:
				prevCanvas=canvas
			
		
		elif deletePrev==True:
			prevCanvas.destroy()
			prevCanvas=canvas
			
		textFrame.destroy()
		
		inputLabel.destroy()
		inputBox.destroy()
		
		createWord(imgFileList,wordFileDict)
		
		canvas=drawSyllables(master, canvas, wordFileDict)
		(inputLabel, inputBox)=drawInputBox(master,  canvas, textFrame, inputBox, inputLabel, imgFileList, wordFileDict)
		
		userInput=inputBox.get()
	
	else:
		master.destroy()

def createWord(imgFileList, wordFileDict):
	
	wordFileDict.clear()
	
	i=0
	word=""
	
	
	syllables=randChoice(wD.keys())
	tokens=syllables.split('-')
	print tokens
	for t in tokens:
		wordFileDict[ t ] = t+".png"
	
	
	
imgHolder=[]
def drawSyllables(master, canvas, wordFileDict):
	global imgHolder
	
	startWidth=0
	canvas_width=len(wordFileDict.keys())*100
	canvas_height=100
	
	canvas = Canvas(master, width=canvas_width, height=canvas_height)
	for key in wordFileDict.keys()[:]:
		fileName=wordFileDict[key]
		
		filePath=SYLLABLE_LIST_DIR+"\\"+ fileName
		imageFile=Image.open( filePath ) 
		imgHolder.append(  ImageTk.PhotoImage( imageFile) )
		#store because PhotoImage copy issues; "wrapper for their copy() method is botched"
		
		canvas.create_image(startWidth, 0, anchor=NW,  image=imgHolder[len(imgHolder)-1])
		startWidth+=imageFile.size[0]
		
	canvas.pack()
	
	return canvas


def drawInputBox(master, canvas, textFrame, inputBox, inputLabel,  imgFileList, wordFileDict):
	
	#Create a Label in textFrame
	
	textFrame= Frame(master)
	
	
	wordLabel=Label(textFrame)
	wordLabel["text"]=wD[ "-".join( wordFileDict.keys() ) ]
	wD.pop(  "-".join( wordFileDict.keys() ) , None)
	wordLabel.pack()
	
	inputLabel = Label(textFrame)
	inputLabel["text"] = "Enter syllables:"
	inputLabel.pack(side=LEFT)

	# Create an Entry Widget in textFrame
	inputBox = Entry(textFrame)
	inputBox["width"] = 50
	inputBox.pack(side=LEFT)
	
	inputBox.focus_force()

	inputBox.bind("<Return>", lambda func:handleUserInput(master, canvas, textFrame,  inputBox, inputLabel, imgFileList, wordFileDict) )
	
	
	
	inputBox.pack()
	textFrame.pack()
	
	return (inputLabel, inputBox)


def createHistogram():
	erList=ErrorList.load(mistakesLog)
	
	#count all errors then make chart
	histogram=[]
	numOfErrors=0
	for e in erList:
		
		if ( e.getCount() >0):
			numOfErrors=numOfErrors+1
			histogram.append(e)
	
	#printing
	for h in histogram:
		print h.getCharacter(), "\t:\t", getNumOfBars(h.getCount()/(numOfErrors*1.0)), round((h.getCount()/((numOfErrors)*1.0))*100,2),"%"
		
def getNumOfBars(num):
	result=""
	
	for i in range(0,int(num*100)):
		result="".join([result,"[]"])
	
	return result

def main():
	
	master = Tk()
	
	master.title("Hiragana")
	master["padx"] = 20
	master["pady"] = 20 
	
	wordFileDict={}
	wordFileDict=OrderedDict(wordFileDict)
	textFrame=None
	inputBox=None
	inputLabel=None
	
	imgFileList=listdir(SYLLABLE_LIST_DIR)
	createWord(imgFileList, wordFileDict)
	
	canvas=None
	canvas=drawSyllables(master,  canvas, wordFileDict)
	(inputLabel, inputBox)=drawInputBox(master,  canvas, textFrame, inputBox, inputLabel, imgFileList, wordFileDict)
	
	
	mainloop()
	
	
if __name__ == "__main__":
	
	SYLLABLE_LIST_DIR="symImg"
	mistakesLog="mistakes.log"

	
	if ("p" in argv):
		createHistogram()
	else:
		main()
	
	