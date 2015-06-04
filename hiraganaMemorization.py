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


def loadSymDicts(wD):
	temp={}
	targs=["verbs"]
	for t in targs:
		d=open( path.join("symDicts",t) ).read().replace("\n","")
		d=d.lower()
		exec("temp="+"{"+d+"}")
		wD.update(temp)




wD={}
loadSymDicts(wD)

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

def generateCorrectAns(tokens):
	correctAns=""
	vowels=['a','e','o','i','u']
	for i in range(0,len(tokens)):

		if tokens[i]=="minitsu":
			if i<len(tokens)-1 and tokens[i+1][0] not in vowels:
				correctAns=correctAns+tokens[i+1][0]
			else:
				raise ValueError("Last syllable can't be a Sokuon(little tsu) and must not be a vowel" + ". Tokens="+ str(tokens))
		else:
			correctAns=correctAns+tokens[i]

	return correctAns

prevCanvas=None
deletePrev=False
def handleUserInput(master, canvas, textFrame, inputBox, inputLabel, imgFileList, wordFileDict):

	global prevCanvas
	global canvasCount
	global deletePrev

	userInput=inputBox.get()

	if userInput!="quit":


		correctAns= generateCorrectAns(  tokens )
		if correctAns==userInput:
			print userInput, "is correct!"


		else:
			print userInput, "is wrong! Answer is: ", correctAns


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
		if len(wD)>0:
			createWord(imgFileList,wordFileDict)

			canvas=drawSyllables(master, canvas, wordFileDict)
			(inputLabel, inputBox)=drawInputBox(master,  canvas, textFrame, inputBox, inputLabel, imgFileList, wordFileDict)

			userInput=inputBox.get()

		else:
			master.destroy()

	else:
		master.destroy()

tokens=[]
def createWord(imgFileList, wordFileDict):

	wordFileDict.clear()
	global tokens
	i=0
	word=""


	syllables=randChoice(wD.keys())
	tokens=syllables.split('-')
	for t in tokens:
		wordFileDict[ t ] = t+".png"



imgHolder=[]
def drawSyllables(master, canvas, wordFileDict):
	global imgHolder


	startWidth=0
	canvas_width=len(tokens)*100
	canvas_height=100

	canvas = Canvas(master, width=canvas_width, height=canvas_height)
	for t in tokens:
		fileName= 	t.title()+".png"
		filePath=path.join( SYLLABLE_LIST_DIR, fileName )
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
	wordLabel["text"]=wD[ "-".join( tokens ) ]
	wD.pop(  "-".join( tokens ) , None)
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

	SYLLABLE_LIST_DIR="./symImg"
	mistakesLog="mistakes.log"


	if ("p" in argv):
		pass
		#createHistogram()
	else:
		main()
