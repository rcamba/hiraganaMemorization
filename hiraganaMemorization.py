from Tkinter import *
import Image
import ImageTk
import tkMessageBox

from os import listdir, chdir, system, getcwd, path
from random import randint
from time import sleep
from threading import Thread
from sys import argv 
import functools

global entryWidget
global correctAns

global numOfCorrectAns
global nuMOfWrongAns
"""
TODO: 
	add scoring
	create log to display which characters that I make mistakes on
	input will now have to be separated in spaces to allow counting mistakes to create the log
"""

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

def get(event,param):
	
	global numOfCorrectAns
	global nuMOfWrongAns
	
	
	
	if ( entryWidget.get()=="quit"):
		if numOfCorrectAns>0:
			print "Score : ", (numOfCorrectAns/(numOfCorrectAns+nuMOfWrongAns*1.0))*100, " %"
		param.destroy()
		#exit()
	
	else:
		userAns=entryWidget.get()
		print userAns
		if(userAns.lower()==correctAns):
			print "Correct answer!"
			numOfCorrectAns=numOfCorrectAns+1
			param.destroy()
			
			runQuiz()
			#system("testImageDisplay.py")
			#Thread(target=system,args=("testImageDisplay.py",)).start()
			
			
		else:
			print "Wrong answer! Correct answer: " + correctAns
			nuMOfWrongAns=nuMOfWrongAns+1
			createLog(userAns)
			entryWidget.delete(0, END)#Tkinter.END

def createLog(userAns):
	
	uAnsList=userAns.split()
	cAnsList=correctAns.split()
	
	for i in range(0,len(uAnsList)):
		if(uAnsList[i].lower()!=cAnsList[i].lower()):
			increaseErrorCount(cAnsList[i])
			
def increaseErrorCount(error):
	#finds the error in the log and increases it by 1
	eList=ErrorList.load(eCountLog)
	
	for e in eList:
		if(e.getCharacter().lower()==error.lower()):
			e.increaseCount()
			
			break
	
	
	ErrorList.writeLog(eCountLog, eList)
	
	
			
def getImageFileList():

	
	fList=listdir(CHAR_LIST_DIR)
	
	return fList
	



def createImage(master, imgFileList):
	
	global correctAns
	correctAns=""
	
	chosenImgs=[]
	canvas_width=0
	canvas_height=100
	
	master.title("Hiragana")
	master["padx"] = 20
	master["pady"] = 20 
	
	
	
	i=0
	counter=randint(1,4)
	
	while(i<counter):
		randNum=randint(0,len(imgFileList)-1)
		
		#print imgFileList[randNum]
		imageFile=Image.open( CHAR_LIST_DIR+"\\"+imgFileList[ randNum ] ) 
		img=ImageTk.PhotoImage(imageFile)
		
		chosenImgs.append(img)
		correctAns="".join([correctAns," ",(imgFileList[randNum].replace(".png","").replace('_',''))]).lower().strip()
		
		canvas_width+=img.width()
		#canvas_height+=img.height()+5
		
		i=i+1
	
	canvas = Canvas(master, width=canvas_width, height=canvas_height)
	canvas.pack()
	
	startWidth=0
	
	
	for i in range(0,len(chosenImgs)):
		chosenImg=chosenImgs[i]
		canvas.create_image(startWidth, 0, anchor=NW,  image=chosenImg)
		startWidth+=img.width()
		
	
	createEntryWidget(master)
	
	mainloop()
	
	

def createEntryWidget(master):
	
	global entryWidget
	
	master["padx"] = 20
	master["pady"] = 20   
	textFrame = Frame(master)
	
	#Create a Label in textFrame
	entryLabel = Label(textFrame)
	entryLabel["text"] = "Enter syllables:"
	entryLabel.pack(side=LEFT)

	# Create an Entry Widget in textFrame
	entryWidget = Entry(textFrame)
	entryWidget["width"] = 50
	entryWidget.pack(side=LEFT)
	#entryWidget.focus_set()
	entryWidget.focus_force()

	#entryWidget.bind("<Return>",get)
	entryWidget.bind("<Return>",functools.partial(get, param=master))
	
	entryWidget.pack()
	textFrame.pack()
	


def runQuiz():
	
	
	master = Tk()
	imgFileList=getImageFileList()

	createImage(master, imgFileList)
	
def tempCreateLog():
	writer=open(eCountLog,'w')
	flist=listdir(CHAR_LIST_DIR)
	
	for f in flist:
		
		
		if(path.isfile("".join([CHAR_LIST_DIR,"\\",f]))):
			writer.write("".join([f.replace(".png","").replace('_',''),':0']))
			writer.write('\n')
	writer.close()

def createHistogram():
	erList=ErrorList.load(eCountLog)
	
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
		
if __name__ == "__main__":
	
	CHAR_LIST_DIR="symImg"
	eCountLog="mistakes.log"
	nuMOfWrongAns=0	
	numOfCorrectAns=0	
	#tempCreateLog()
	if ("p" in argv):
		createHistogram()
	else:
		runQuiz()
		

	
	
	
	
	
	
		




"""
correctAns has no spaces
def get(event,param):
	
	
	
	if ( entryWidget.get()=="quit"):
		param.destroy()
		#exit()
	
	else:
		userAnswer=entryWidget.get()
		print userAnswer
		if(userAnswer.lower()==correctAns):
			print "Correct answer!"
			
			param.destroy()
			
			runQuiz()
			#system("testImageDisplay.py")
			#Thread(target=system,args=("testImageDisplay.py",)).start()
			
			
			
		else:
			print "Wrong answer! Correct answer: " + correctAns
			entryWidget.delete(0, END)#Tkinter.END
	

def getImageFileList():
	CHAR_LIST_DIR="C:\\Users\\Kevin\\Pictures\\ScreenShots\\Hiragana\\characters"
	fList=listdir(CHAR_LIST_DIR)
	fList.remove("testImageDisplay.py")
	return fList
	



def createImage(master, imgFileList):
	
	global correctAns
	correctAns=""
	
	chosenImgs=[]
	canvas_width=0
	canvas_height=100
	
	master.title("Hiragana")
	master["padx"] = 20
	master["pady"] = 20 
	
	
	i=0
	counter=randint(1,4)
	
	while(i<counter):
		randNum=randint(0,len(imgFileList)-1)
		
		#print imgFileList[randNum]
		imageFile=Image.open( imgFileList[ randNum ] ) 
		img=ImageTk.PhotoImage(imageFile)
		
		chosenImgs.append(img)
		correctAns="".join([correctAns,(imgFileList[randNum].replace(".png",""))]).lower()
		
		canvas_width+=img.width()
		#canvas_height+=img.height()+5
		
		i=i+1
	
	canvas = Canvas(master, width=canvas_width, height=canvas_height)
	canvas.pack()
	
	startWidth=0
	
	
	for i in range(0,len(chosenImgs)):
		chosenImg=chosenImgs[i]
		canvas.create_image(startWidth, 0, anchor=NW,  image=chosenImg)
		startWidth+=img.width()
		
	
	createEntryWidget(master)
	
	mainloop()
	
	

def createEntryWidget(master):
	
	global entryWidget
	
	master["padx"] = 20
	master["pady"] = 20   
	textFrame = Frame(master)
	
	#Create a Label in textFrame
	entryLabel = Label(textFrame)
	entryLabel["text"] = "Enter syllables:"
	entryLabel.pack(side=LEFT)

	# Create an Entry Widget in textFrame
	entryWidget = Entry(textFrame)
	entryWidget["width"] = 50
	entryWidget.pack(side=LEFT)
	#entryWidget.focus_set()
	entryWidget.focus_force()

	#entryWidget.bind("<Return>",get)
	entryWidget.bind("<Return>",functools.partial(get, param=master))
	
	entryWidget.pack()
	textFrame.pack()
	


def runQuiz():
	
	
	master = Tk()
	imgFileList=getImageFileList()

	createImage(master, imgFileList)
	
	
if __name__ == "__main__":
	
	
	
	
	#imgFileList=getImageFileList()

	#createImage(master, imgFileList)
	
	

	runQuiz()

"""