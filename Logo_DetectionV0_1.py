#!/usr/bin/python
# -*- coding: utf-8 -*-
#Este script tiene como finalidad detectar la presencia y ausencia del logotipo de un canal de TV (Deteccion de publicidad)
#Programador: Juan Agustín Coutinho

#----------------------------------------------------FUNCIONAMIENTO--------------------------------------------------------------------------------
"""
Su funcionamiento es simple: partiendo de una imagen (de un archivo de video o camara web en vivo apuntando al Televisor por ejemplo),
se selecciona con el mouse donde se encuentra el logo del canal y posteriormente se irán comparando los frames
de la zona seleccionada. Si el logo permanece en pantalla se deduce que NO HAY PUBLICIDAD y cuando el logo no se detecta mas, se
deduce que HAY PUBLICIDAD (En la mayoría de los canales de TV de Argentina esto se cumple).
Pudiendo detectar esto, este script propone reproducir un video de Youtube del agrado del usuario o una playlist que
se desee. Esta parte aun no se encuentra bien definida, pero es cuestion de jugar con las opciones de la aplicacion 'mps-youtube'.
Actualmente se reproduce un video fijo de youtube mediante su URL (queda a disposicion del programador elegir que hacer al detectar publicidad)
"""

#----------------------------------------------------OBJETIVO-----------------------------------------------------------------------------------
"""El objetivo de este proyecto es lograr implementarlo en un sistema que permita a cualquier televidente NO VER LA PUBLICIDAD si lo desea y ver
en su lugar algo que sea de su agrado"""

#----------------------------------------------------ACLARACIONES-----------------------------------------------------------------------------------
"""
En el programa existen variables que deberan ajustarse (Actualmente posee valores para analizar video HD). 
Estas son:
-> MARGEN_SUPERIOR: 
-> MARGEN_INFERIOR:
-> MARGEN_TOTAL:
Cada vez que hay aciertos o desaciertos, se suma o resta respectivamente la variable "contador_aciertos". 
Acorde a su valor se determina si el logo esta en patalla o no.

|============MARGEN_INFERIOR|MARGEN_SUPERIOR==================|MARGEN_TOTAL

-> FRECUENCIA_FRAMES: Cada cuantos frames se tomarán las muestras que serán comparadas entre sí

Los pesos son valores positivos y definen en cuanto se incrementará o decrementará la variable "contador_aciertos"
-> PESO_ACIERTO:
-> PESO_DESACIERTO:


Dependen de:
-> La calidad del video analizado (ciertas camaras web tienen muy baja calidad de imagen)
-> Los fps del video a analizar
-> El tipo de logo del canal ya que algunos poseen logos animados (en este caso debe reducirse la frecuencia con la que se toman las muestras,
esto tiene sus pro y sus contras en cuanto a eficacia de deteccion)
-> La variación del brillo, saturación o contraste de los distintos frames

Con funciones específicas de la librería OpenCV se puede lograr reducir considerablemente el impacto de los factores anteriormente mencionados.
En éste código se utiliza un procesamiento básico de imágenes.
"""

#----------------------------------------------------CONTACTO-------------------------------------------------------
"""
Por favor, cuéntenme sus ideas, mejoras o modificaciones a mi correo electrónico: cou_647@hotmail.com
También por cualquier duda pueden escribirme.
"""
#-------------------------------------------------------------------------------------------------------------------

import numpy as np
import cv2
import os
import time

# superior izquierdo, superior derecho, inferior izquierdo, inferior derecho
pts = [(0,0),(0,0),(0,0),(0,0)]
pointIndex = 0
dst_logo = [0,0]
frameIndex = 0

cap = cv2.VideoCapture('/home/cou/Escritorio/Vivo TV Pública-3.mp4')

#------------QUITARLO SI SE UTILIZA UN ARCHIVO DE VIDEO O UNA FILMACION CON UN AJUSTE DE BRILLO FIJO---------------------------------------
for i in range(1,25): #Se toman 25 frames para que se autoajuste el brillo y se vea una imagen clara y estable al tomar la muestra del logo
	ret, img = cap.read()
if ret == False:
	print "No se ha podido leer el archivo de video"
	os._exit(0)
#------------------------------------------------------------------------------------------------------------------------------------------


#-----------------------------------VARIABLES AJUSTABLES--------------------------------------------------------------------------
MARGEN_SUPERIOR = 40
MARGEN_INFERIOR = 40
MARGEN_TOTAL = 80
#"MARGEN_SUPERIOR" no puede ser inferior al "MARGEN_INFERIOR" y tampoco superior a "MARGEN_TOTAL"

FRECUENCIA_FRAMES = 5 #Valor que define cada cuantos frames se realizará la comparación

UMBRAL_DETECCION = 0.8 #Cada comparación arroja un valor entre 0 y 1. Todos aquellos con valores mayores al definido en "UMBRAL_DETECCION" se considerarán aciertos

#El valor de los pesos deberan ser siempre positivos. Ajustarlos hasta obtener un optimo resultado
PESO_ACIERTO = 2
PESO_DESACIERTO = 1
#------------------------------------------------------------------------------------------------------------------------------------------

# mouse callback function
def draw_circle(event,x,y,flags,param):
	global pointIndex
	if event == cv2.EVENT_LBUTTONDBLCLK:
		pts[pointIndex] = (x,y)
		print "Coordenada ingresada: " + str(pts[pointIndex])
		pointIndex = pointIndex + 1

def selectFourPoints():
	while(pointIndex < 4):
		cv2.imshow('image',img)
		key = cv2.waitKey(20) & 0xFF
		if key == 27: #SE PRESIONO "ESC"
			return False

	return True

def child():
	print('\nA new child ',  os.getpid())
	os.system('mpsyt playurl "https://www.youtube.com/watch?v=TvOmxdf_hvc"')
	os._exit(0) 

def deteccion_Logo():
	global dst_logo

	if contador_frames < 5:#Los primeros 5 frames los tomo a todos como aciertos, hasta que se estabilice el control de brillo de la camara
		return True
	elif frameIndex == 1:
		frame_anterior = cv2.cvtColor (dst_logo[frameIndex-1], cv2.COLOR_BGR2GRAY)
		frame_actual = cv2.cvtColor (dst_logo[frameIndex], cv2.COLOR_BGR2GRAY)
		res = cv2.matchTemplate(frame_actual,frame_anterior,cv2.TM_CCOEFF_NORMED)
		threshold = UMBRAL_DETECCION
		for fila_de_pixels in res:
			for pixel in fila_de_pixels:
				if pixel > threshold:
					return True
	return False

def reproducir_Youtube():
	newpid = os.fork() #Creo un proceso hijo que reproducira el video
	if newpid == 0:
		child() #Si es el hijo que reproduzca el video
	else:
		print "REPRODUCIENDO VIDEO!"
		
def finalizar_Youtube():
	os.system('killall -9 mpsyt') #MATAMOS EL PROCESO QUE REPRODUCE EL VIDEO


cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_circle)
#-----------------------------------------------------------------------------------------------------

print "Por favor seleccione 4 puntos en la imagen haciendo doble click en los vertices de la imagen en el siguiente orden: \n\
superior izquierdo, superior derecho, inferior izquierdo, inferior derecho."


if(selectFourPoints()):
	cv2.destroyWindow('image')
	# Los cuatro puntos de la pantalla donde se encuentra el logo del canal
	pts1 = np.float32([\
		[pts[0][0],pts[0][1]],\
		[pts[1][0],pts[1][1]],\
		[pts[2][0],pts[2][1]],\
		[pts[3][0],pts[3][1]] ])

	contador_aciertos = 100
	divisor_frames = 0 #Valor que se utilizara para registrar la cantidad de frames que se leen
	bandera_Youtube = 0 #Bandera que cambiara entre 0 y 1, para inicializar youtube y finalizarlo cuando corresponda
	contador_frames = 0
	
	while(1):
		ret,frame = cap.read()
		if divisor_frames == FRECUENCIA_FRAMES:# Es decir se analizaran y comparan los frames cada "FRECUENCIA_FRAMES"
			if ret == True:				
				# Crop from x, y, w, h -> 100, 200, 300, 400
				# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
				dst_logo[frameIndex] = frame[pts[0][1]:pts[2][1], pts[0][0]:pts[1][0]] #Recortamos los frames y aislamos el logo
				
				cv2.imshow("output_original",frame)
				cv2.imshow("output_logo",dst_logo[frameIndex])
				cv2.imshow("output_logo0",dst_logo[0])	

				#Con el siguiente bloque se va a lograr que cuando el contador de aciertos este por encima de "MARGEN_SUPERIOR" de positivo, por debajo negativo (para manejar falsos positivos y negativos)
				if (deteccion_Logo()):
					if contador_aciertos > MARGEN_SUPERIOR:
						print "LOGO EN PANTALLA DETECTADO"
						if bandera_Youtube == 0:
							#finalizar_Youtube()
							print "1"
							bandera_Youtube = 1
					elif contador_aciertos < MARGEN_INFERIOR:
						print "NO HAY MAS LOGO (PUBLICIDAD!)"
						if bandera_Youtube == 1:
							#reproducir_Youtube()
							print "2"
							bandera_Youtube = 0
					if contador_aciertos < (MARGEN_TOTAL-(PESO_ACIERTO-1)):
						contador_aciertos = contador_aciertos + PESO_ACIERTO #Se le da mas peso a los aciertos (esto soluciona algunos problemas de deteccion en algunos casos)
					dst_logo[0] = dst_logo[1] #Con cada acierto paso el frame [1] al [0] donde estara la muestra base
						
				elif (frameIndex == 1):
					if contador_aciertos < MARGEN_INFERIOR:
						print "NO HAY MAS LOGO (PUBLICIDAD!)"
						if bandera_Youtube == 1:
							#reproducir_Youtube()
							print "3"
							bandera_Youtube = 0
					elif(contador_aciertos > MARGEN_SUPERIOR):
						print "LOGO EN PANTALLA DETECTADO"
						if bandera_Youtube == 0:
							#finalizar_Youtube()
							print "4"
							bandera_Youtube = 1
							
					if contador_aciertos > (PESO_DESACIERTO-1):
						contador_aciertos = contador_aciertos - PESO_DESACIERTO
					frameIndex = 0 #Lo pongo igual a 0 para que cuando no hay acierto el frame 0 (del logo) se mantenga siempre para comparar hasta que vuelva a haber un logo
				
				if frameIndex == 0:
					frameIndex = 1 #Luego de la primera iteracion el frameIndex quedara siempre en 1. Allí se irán almacenando los nuevos frames
					
				if cv2.waitKey(1) & 0xFF == ord('q'):
					salir = 1
					break
				contador_frames = contador_frames + 1	
				
			else:
				print "No se pudo leer imagen del video o camara"
				break
			
			#print str(contador_aciertos)
			divisor_frames = 0; #Reseteamos el contador de frames
		
		else:
			divisor_frames = divisor_frames + 1

else:
	print "Se presionó la tecla 'ESC'(Escape)"

cap.release()
os.system('killall -9 mpsyt')
#cv2.waitKey(0)
cv2.destroyAllWindows()
