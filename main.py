## importing libraries and necessary resources
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from tkinter import *
import pyttsx3 as pp
import speech_recognition as s
import threading

## initializing the speech engine
eng1 = pp.init()

## retrieving the value of a property of the current TTS engine.
voices = eng1.getProperty('voices')
print(voices)

## setting the voice property to the desired voive
## voices[1] indicates it ia a female voice
eng1.setProperty('voice', voices[1].id)

## function used for the text to be spoken by the engine
def speak(word):
     eng1.say(word)
     eng1.runAndWait()


my_bot = ChatBot("Coffee Shop Bot")

# load custom training data
with open('coffee_convo.txt', 'r') as f:
    coffee_convo = f.read().splitlines()

# add custom training data to the chatbot trainer
trainer2 = ListTrainer(my_bot)
trainer2.train(coffee_convo)

## creating GUI window of size 650x650
main = Tk()
main.geometry("650x650")
main.title("Coffee Shop Bot")

 ## displaying image using PhotoImage class and Label widget
img = PhotoImage(file="bot1.png")
photoL = Label(main, image=img)
photoL.pack(pady=5)


# # function used to convert audio input from the user into the string
def takeQuery():
    sr = s.Recognizer()
    sr.pause_threshold = 1
    print("your bot is listening try to speak")

    with s.Microphone() as m:
        try:
            audio = sr.listen(m)
            qry = sr.recognize_google(audio, language='eng-US')
            print(qry)
            textF.delete(0, END)
            textF.insert(0, qry)
            ask_from_cf_bot()
        except Exception as e:
            print(e)
            print("not recognized")

## function used to get user input from textF and generate the appropiate response and display to the Listbox widget
def ask_from_cf_bot():
     query1 = textF.get()
     answer_from_cf_bot = my_bot.get_response(query1)
     queries.insert(END, "You : " + query1)
     queries.insert(END, "Chan : " + str(answer_from_cf_bot))
     speak(answer_from_cf_bot)
     textF.delete(0, END)
     queries.yview(END)

## creating a frame and a scrollbar within the main window
fm = Frame(main)
sb = Scrollbar(fm)
queries = Listbox(fm, width=80, height=15, yscrollcommand=sb.set)
queries.insert(END,"Hi, I am Chan. Welcome to our coffee shop")
queries.insert(END,"You can either type or speak to place your order")

sb.pack(side=RIGHT, fill=Y)
queries.pack(side=LEFT, fill=BOTH, pady=5)
fm.pack()

# # creating text field for user query
textF = Entry(main, font=("helvetica", 15))
textF.pack(ipadx=75, pady=10 )

## creating button
btn = Button(main, text="Get Answers from Chan", font=("helvetica", 15), command=ask_from_cf_bot,fg='white',bg='grey')
btn.pack()


# # function is used to invoke the button
def enter_function(event):
     btn.invoke()


# # binding main window with enter key...
main.bind('<Return>', enter_function)

## infinite loop for user query
def repeatL():
    while True:
        takeQuery()

## threading is used so that the GUI works fine while continuously listening to the user input at the bg
th = threading.Thread(target=repeatL)

th.start()

main.mainloop()

th.stop()