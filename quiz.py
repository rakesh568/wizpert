""" quiz.py
    example of a quiz game
"""

from Tkinter import *
from tkMessageBox import *
import time
import operator

#change this number if more number of questions are added in questions.txt
NUM_QUESTIONS = 10

class Problem(object):
  def __init__(self, question = "", a = "", b = "", c = "", d = "", correct = ""):
    object.__init__(self)
    self.question = question
    self.a = a
    self.b = b
    self.c = c
    self.d = d
    self.correct = correct
    def __repr__(self):
      return str(self)

class App(Tk):
  def __init__(self):
    Tk.__init__(self)

    self.prizeDict={1:'$2000', 2:'$4000', 3:'$8000',4:'$15000',5:'$30000',6:'$62,5000',7:'$125,000',8:'$250,000',9:'$500,000',10:'$1,000,000'}
    self.problems = []
    self.counter = 0
    self.timeVal=0.0

    self.welcomeMsg()    
    self.mainloop()

  def addComponents(self):
    """ add components to the GUI """
    self.title("Quiz")
    self.grid()
    self.columnconfigure(0, minsize = 200)
    self.columnconfigure(1, minsize = 200)
    self.columnconfigure(2, minsize = 200)
    self.columnconfigure(3, minsize = 200)

    self.title("Who wants to be a millionaire")
    #self.geometry('650x300+300+300')

    menubar = Menu(self)
    filemenu = Menu(menubar,tearoff=0)
    filemenu.add_command(label="Start game", command=self.startGame)
    filemenu.add_command(label="Highest scores", command=self.showScorecard)

    filemenu.add_separator()
    
    filemenu.add_command(label="Quit", command=self.quit)
    menubar.add_cascade(label="File",menu=filemenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Instructions", command=self.instructions)
    menubar.add_cascade(label="Help",menu=helpmenu)
    self.config(menu=menubar)

  def welcomeMsg(self):
    self.addComponents()
    photo = PhotoImage(file="millionaire.gif")
    self.wlcmLabel = Label(self, image=photo, justify=RIGHT)
    self.wlcmLabel.photo = photo
    self.wlcmLabel.grid(column=2,rowspan=8, sticky = "w")
    self.wlcmText = Label(self, text = "Who wants to be a millionaire?",font=("Helvetica", 16), justify=LEFT)
    self.wlcmText.grid(padx=10, row=1,column=0, sticky = "e")


  def startGame(self):
    self.nameLabel = Label(self, text = "Enter your name: ",justify=LEFT)
    self.nameLabel.grid(padx=10, row=2,column=0, sticky = "w")
    self.playerName = StringVar(None)
    self.yourName = Entry(self, textvariable=self.playerName)
    self.yourName.grid(padx=10, row=3,column=0, sticky = "w")
    self.submitButton = Button(self, text = "Submit", command = self.submitName)
    self.submitButton.grid(padx=10, row=4,column=0, sticky = "w")


  def playGame(self):
    self.wlcmLabel.grid_forget()
    self.wlcmText.grid_forget()
    self.nameLabel.grid_forget()
    self.yourName.grid_forget()
    self.submitButton.grid_forget()
    self.addComponents()
    self.lblQuestion = Label(self, text = "Question",bg='yellow', anchor=CENTER)
    self.lblQuestion.grid(columnspan=4, sticky = "we",pady=20)
    
    self.btnA = Button(self, text = "A", command = lambda: self.check("A"))
    self.btnA.grid(columnspan=4, sticky = "we")
    
    self.btnB = Button(self, text = "B", command = lambda: self.check("B"))
    self.btnB.grid(columnspan=4, sticky = "we")
    
    self.btnC = Button(self, text = "C", command = lambda: self.check("C"))
    self.btnC.grid(columnspan=4, sticky = "we")

    self.btnD = Button(self, text = "D", command = lambda: self.check("D"))
    self.btnD.grid(columnspan=4, sticky = "we")
    
    self.btnPrev = Button(self, text = "prev", command = self.prev)
    self.btnPrev.grid(row=6, column = 0)
    
    self.lblCounter = Label(self, text = "")
    self.lblCounter.grid(row=6,column = 1)

    self.lblTimer = Label(self, text = "0.0")
    self.lblTimer.grid(row=6,column = 2)
    
    self.btnNext = Button(self, text = "next", command = self.next)
    self.btnNext.grid(row=6,column = 3)
    self.numCorrect=0
    self.loadProblems()
    self.showProblem(0)


  def instructions(self):
    instr="This game will present you 5 questions.\nCorrect answer will reward you with 10$.\nOne wrong answer and your game's over. \nStart playing.!!"
    showinfo("Instructions", instr)

  def submitName(self):
    self.player=self.playerName.get().replace(" ", "")
    self.playGame()

  def showScorecard(self):
    d = {}
    with open("scoreboard.txt") as f:
      for line in f:
        (key, val) = line.split()
        d[key] = val

    score = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    highestScores=""
    for scr in score: 
      highestScores+= scr[0] +": "+ scr[1]+"\n"
    showinfo("Winners", highestScores)

  def check(self, guess):
    #compares the guess to the correct answer
    correct = self.problems[self.counter].correct
    self.answeredFlag=True
    if guess == correct:
      self.numCorrect+=1
      if guess=="A":
        self.btnA.configure(bg = "green")
      if guess=="B":
        self.btnB.configure(bg = "green")
      if guess=="C":
        self.btnC.configure(bg = "green")
      if guess=="D":
        self.btnD.configure(bg = "green")

      if self.numCorrect==10:
        score="Correct Answer!!\nWe've got a champion. You won: " + self.prizeDict[self.numCorrect]
        showinfo("Quiz", score)
        self.quit()
      else:
        score="Correct Answer!!\nCongrats you won "+self.prizeDict[self.numCorrect]
        showinfo("Quiz", score)
        self.next()
    else:
      if guess=="A":
        self.btnA.configure(bg = "red")
      if guess=="B":
        self.btnB.configure(bg = "red")
      if guess=="C":
        self.btnC.configure(bg = "red")
      if guess=="D":
        self.btnD.configure(bg = "red")

      score="Wrong Answer. Game over!!\nTotal money won $"+self.prizeDict[self.numCorrect] 
      showinfo("Quiz", score)
      with open("scoreboard.txt", 'a') as f:
        f.write(self.player + ' ' + self.prizeDict[self.numCorrect] + '\n')

      self.quit()
    
  
  def prev(self):
    self.counter -= 1
    if self.counter < 0:
      self.counter = 0
    self.showProblem(self.counter)
    
  def next(self):
    self.counter += 1
    if self.counter >= len(self.problems):
      self.counter = len(self.problems) - 1
    self.showProblem(self.counter)

  def showProblem(self, counter):
    self.lblQuestion["text"] = self.problems[counter].question
    self.btnA.configure(bg = "white")
    self.btnB.configure(bg = "white")
    self.btnC.configure(bg = "white")
    self.btnD.configure(bg = "white")
    self.btnA["text"] = self.problems[counter].a
    self.btnB["text"] = self.problems[counter].b
    self.btnC["text"] = self.problems[counter].c
    self.btnD["text"] = self.problems[counter].d
    self.lblCounter["text"] = self.counter+1
    self.answeredFlag=False
    self.startTimer()
    self.timeVal=0.0

  def loadProblems(self):
    with open("questions.txt", 'r') as f:
      lines = f.readlines()
      #here 5 is number of questions
      for i in range(0,NUM_QUESTIONS):
        self.problems.append(Problem(
          lines[6*i].strip(),
          lines[6*i+1].strip(),
          lines[6*i+2].strip(),
          lines[6*i+3].strip(),
          lines[6*i+4].strip(),
          lines[6*i+5].strip())                             
        )

  def startTimer(self):
      if self.answeredFlag==True:
        pass
      if int(self.timeVal)>=15:
        score="Time out. Game over!!\nTotal money won $"+self.prizeDict[self.numCorrect]
        showinfo("Quiz", score)
        with open("scoreboard.txt", 'a') as f:
          f.write(self.player + ' ' + self.prizeDict[self.numCorrect] + '\n')          
        self.destroy()

      self.lblTimer['text'] = str(self.timeVal)
      self.timeVal += 0.1
      self.lblTimer.after(100,self.startTimer)



def main():
  a = App()

if __name__ == "__main__":
  
  main()
