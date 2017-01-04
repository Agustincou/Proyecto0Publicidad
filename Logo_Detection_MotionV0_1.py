#!/usr/bin/python

#Este script hace una transformacion de perspectiva sobre un televisor HD (relacion 16:9)
#Su funcionamiento es sencillo, debemos tener un video a camara fija en perspectiva de un TV
#y luego cargando dicho video y seleccionando sus vertices haciendo doble click
#sobre ellos en el orden que indica la consola se realizara la correccion de perspectiva.

import numpy as np
import cv2
import os
import signal
import time

# superior izquierdo, superior derecho, inferior izquierdo, inferior derecho
pts = [(0,0),(0,0),(0,0),(0,0)]
pts_logo = [(0,0),(0,0),(0,0),(0,0)]
pointIndex = 0
pointIndex_logo = 0
dst_logo = [0,0]
frameIndex = 0

cap = cv2.VideoCapture('/home/cou/Documentos/PlayWithOpenCV/Proyecto 0P/untitled.mp4')

_, img = cap.read()

# Con relacion de aspecto 16:9 FUll HD seria:
# 500 * 1.778 = 889 -> (889X500)
#ASPECT_RATIO = (500,889)
# Con relacion de aspecto 4:3 (Camara WEB) seria (800x600)
ASPECT_RATIO = (500,889)
INV_ASPECT_RATIO = (889, 500)
INV_ASPECT_RATIO_LOGO = (300, 300)

pts2 = np.float32([[0,0],[ASPECT_RATIO[1],0],[0,ASPECT_RATIO[0]],[ASPECT_RATIO[1],ASPECT_RATIO[0]]])
# mouse callback function
def draw_circle(event,x,y,flags,param):
	global pointIndex
	if event == cv2.EVENT_LBUTTONDBLCLK:
		pts[pointIndex] = (x,y)
		print "Coordenada ingresada: " + str(pts[pointIndex])
		pointIndex = pointIndex + 1

def draw_circle_logo(event,x,y,flags,param):
	global pointIndex_logo
	if event == cv2.EVENT_LBUTTONDBLCLK:
		pts_logo[pointIndex_logo] = (x,y)
		print "Coordenada ingresada: " + str(pts_logo[pointIndex_logo])
		pointIndex_logo = pointIndex_logo + 1

def selectFourPoints():
	while(pointIndex < 4):
		cv2.imshow('image',img)
		key = cv2.waitKey(20) & 0xFF
		if key == 27: #SE PRESIONO "ESC"
			return False

	return True

def selectFourPointsLogo():
	while(pointIndex_logo < 4):
		cv2.imshow('output_corregido',dst)
		key = cv2.waitKey(20) & 0xFF
		if key == 27: #SE PRESIONO "ESC"
			return False
			
	return True

def child():
	print('\nA new child ',  os.getpid())
	os.system('mpsyt playurl "https://www.youtube.com/watch?v=TvOmxdf_hvc"')
	os._exit(0) 

def deteccion_Logo():
	global frame_logo
	#if frameIndex == 0:
		#return True #Si es la primera vez que entra, se tiene la muestra del logo recien tomada, se devolvera True
	if frameIndex == 1:
		frame_anterior = cv2.cvtColor (dst_logo[frameIndex-1], cv2.COLOR_BGR2GRAY)
		frame_actual = cv2.cvtColor (dst_logo[frameIndex], cv2.COLOR_BGR2GRAY)
		res = cv2.matchTemplate(frame_actual,frame_anterior,cv2.TM_CCOEFF_NORMED)
		threshold = 0.6
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
cv2.namedWindow('output_corregido')
cv2.setMouseCallback('image',draw_circle)
#cv2.setMouseCallback('output_corregido',draw_circle_logo)

#-----------------------------------------------------------------------------------------------------

print "Por favor seleccione 4 puntos en la imagen haciendo doble click en los vertices de la imagen en el siguiente orden: \n\
superior izquierdo, superior derecho, inferior izquierdo, inferior derecho."

while(1):
	if(selectFourPoints()):
		cv2.destroyWindow('image')
		# Los cuatro puntos de la pantalla de aspecto 16:9
		pts1 = np.float32([\
			[pts[0][0],pts[0][1]],\
			[pts[1][0],pts[1][1]],\
			[pts[2][0],pts[2][1]],\
			[pts[3][0],pts[3][1]] ])

		M = cv2.getPerspectiveTransform(pts1,pts2)
		contador_aciertos = 100
		divisor_frames = 0
		bandera_Youtube = 0 #Bandera que cambiara entre 0 y 1, para inicializar youtube y finalizarlo cuando corresponda
		contador_frames = 0
		
		while(1):
			if divisor_frames == 20:# Es decir se analizaran y comparan los frames cada 10
				ret,frame = cap.read()
				if ret == True:				
					# Crop from x, y, w, h -> 100, 200, 300, 400
					# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
					dst_logo[frameIndex] = frame[pts[0][1]:pts[2][1], pts[0][0]:pts[1][0]]
					
					#frame = cv2.resize(frame, (640,480))
					cv2.imshow("output_original",frame)
					cv2.imshow("output_logo",dst_logo[frameIndex])
					cv2.imshow("output_logo0",dst_logo[0])	
	
					#Con el siguiente bloque se va a lograr que cuando el contador de aciertos este por encima de 50 de positivo, por debajo negativo (para manejar falsos positivos y negativos)
					if (deteccion_Logo()):
						if contador_aciertos > 50:
							print "LOGO EN PANTALLA DETECTADO"
							if bandera_Youtube == 0:
								#reproducir_Youtube()
								print "1"
								bandera_Youtube = 1
						else:
							print "NO HAY MAS LOGO (PUBLICIDAD!)"
							if bandera_Youtube == 1:
								#finalizar_Youtube()
								print "2"
								bandera_Youtube = 0
						if contador_aciertos < 99:
							contador_aciertos = contador_aciertos + 2
					elif (frameIndex == 1):
						if contador_aciertos < 50:
							print "NO HAY MAS LOGO (PUBLICIDAD!)"
							if bandera_Youtube == 1:
								#finalizar_Youtube()
								print "2"
								bandera_Youtube = 0
						else:
							print "LOGO EN PANTALLA DETECTADO"
							if bandera_Youtube == 0:
								#reproducir_Youtube()
								print "1"
								bandera_Youtube = 1
								
						if contador_aciertos > 0:
							contador_aciertos = contador_aciertos - 1
						
						if contador_frames > 20: #Luego de los primeros 20 frames tomados recien me quedo con la ultima muestra si no hay matcheo, esto es por el tema del ajuste de brillo de la camara
							frameIndex = 0 #Lo pongo igual a 0 para que cuando no hay acierto el frame 0 (del logo) se mantenga siempre para comparar hasta que vuelva a haber un logo
					
					if(frameIndex == 0):
						frameIndex = 1 #Luego de la primera iteracion el frameIndex quedara siempre en 1. La primera muestra quedara guardada como el logo a detectar
					else:
						frameIndex = 0
						
					if cv2.waitKey(1) & 0xFF == ord('q'):
						salir = 1
						break
					
					contador_frames = contador_frames + 1
					
				else:
					print "No se pudo capturar mas imagenes del video o camara"
					break
				
				#print str(contador_aciertos)
				divisor_frames = 0; #Reseteamos el contador de frames
			
			else:
				divisor_frames = divisor_frames + 1
			
	break


cap.release()
os.system('killall -9 mpsyt')
#cv2.waitKey(0)
cv2.destroyAllWindows()
