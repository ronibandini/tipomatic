# Tipomatic
# Roni Bandini, August 2024, MIT License
# Buenos Aires, Argentina
# pip install SpeechRecognition
# pip install OpenAI

from unihiker import Audio
from unihiker import GUI
from pinpong.board import Board, Pin
from pinpong.board import *
from pinpong.extension.unihiker import *
from openai import OpenAI
import time
import os
import speech_recognition as sr

howManySeconds=25
numWords=0
howManyTipo=0
tipoRate=0

chatGPTKey      =""
model           = "gpt-3.5-turbo-instruct"
temperature     =0.3
prompt		="Reescribir en tono erudito y excluyendo la palabra tipo la frase que sigue: "

myAudio = Audio()  
Board().begin() 
gui = GUI()
client = OpenAI(api_key=chatGPTKey,)

os.system('clear')
print("Tipomatic 1.0 Roni Bandini")
print("")

def printScreen():
	global numWords
	global howManyTipo
	global tipoRate

	gui.clear()

	img = gui.draw_image(x=0, y=0, w=240, h=320, image='images/background.png')

	gui.draw_text(x=175,y=30,text=howManyTipo, font_size=10, color="black", origin='top')
	gui.draw_text(x=175,y=65,text=numWords, font_size=10, color="black", origin='top')
	gui.draw_text(x=175,y=105,text=round(tipoRate, 2), font_size=10, color="black", origin='top')


def clickRecord():

	global numWords
	global howManyTipo
	global tipoRate

	numWords=0
	howManyTipo=0
	tipoRate=0
	printScreen()

	print("Recording...")
	buzzer.pitch(494)  
	printScreen()
	gui.draw_text(x=50,y=240,text="Grabando...", font_size=10, color="black", origin='top')
	buzzer.stop()

	myAudio.start_record('tipo.wav')
	time.sleep(1)
	
	while button_a.is_pressed() == False: 
		time.sleep(1)

	buzzer.pitch(494)  

	myAudio.stop_record()
	buzzer.stop()
	gui.draw_text(x=55,y=260,text="Analizando...", font_size=10, color="black", origin='top')
	
	print("Recognizing...")

	r = sr.Recognizer()
	with sr.WavFile("tipo.wav") as source:              
		audio = r.record(source)                         
		try:
			result=r.recognize_google(audio,language="es-ES",key=None)
		except:                                 
			print("Could not understand audio")
			result =""
	         
	if result!="":

		wordList = result.split()
		numWords = len(wordList)

		howManyTipo=wordList.count('tipo')
		tipoRate=howManyTipo/numWords*100

		print("Words: "+str(numWords))
		print("Tipo counter: "+str(howManyTipo))
		print("Tipo rate:"+str(tipoRate))
		printScreen()
		
		while button_a.is_pressed() == False: 
			time.sleep(1)

		buzzer.pitch(494)  
		buzzer.stop()

		# chatGPT
	
		completion = client.completions.create(
                    model=model,
                    prompt=prompt+" "+result,
                    max_tokens=200,
                    n=1,
                    stop=None,
                    temperature=temperature,
               	)

		chatGPTAnswer=completion.choices[0].text
		chatGPTAnswer=chatGPTAnswer.strip('\n')

		print("Reescritura:"+chatGPTAnswer)
		gui.clear()
		img = gui.draw_image(x=0, y=0, w=240, h=320, image='images/sugerencia.png')
		gui.draw_text(x=12,y=45,text=chatGPTAnswer, font_size=10, color="black", w=225)

		while button_a.is_pressed() == False: 
			time.sleep(1)

		buzzer.pitch(494)  
		printScreen()
	
		gui.draw_text(x=65,y=240,text="Botón para grabar", font_size=10, color="black", origin='top')
		buzzer.stop()  
	else:
		printScreen()
	
		gui.draw_text(x=65,y=240,text="Error en audio", font_size=10, color="black", origin='top')

printScreen()
gui.draw_text(x=65,y=240,text="Botón para grabar", font_size=10, color="black", origin='top')

while True:

	if button_a.is_pressed() == True: 
		clickRecord()

	time.sleep(1)



