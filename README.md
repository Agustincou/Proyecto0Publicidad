# Proyecto0Publicidad
 
  Script Python que hace uso de OpenCV para la detección de logos de un canal de TV para diferenciar entre los programas y el espacio publicitario.

<h1>Implementación Casera</h1>
![Alt text](https://github.com/Agustincou/Proyecto0Publicidad/blob/master/Expicativo%20Proyecto%200P.png "Posible Implementación Casera")

  El script correrá en la PC, la cual puede obtener las imágenes de la TV ya sea por una camara web o archivo de video pregrabado(métodos implementados en el código). También podrían obtenerse las imágenes de transmisiones streaming de video (habria que modificar un poco el código en este caso)
  
cap = cv2.VideoCapture(0) #Webcam
ó
cap = cv2.VideoCapture('/home/cou/Escritorio/Vivo TV Publica-3.mp4') #Archivo de Video

La PC al detectar que ha comenzado el espacio publicitario (al dejar de detectar el logo del canal) realizará una determinada acción. En este caso se pensó en reproducir un video de Youtube que desee el usuario/programador. Por el momento la reproducción del video se produce únicamente en la PC utilizando la aplicación mps-youtube que permite mediante comandos de consola reproducir cualquier video de Youtube.

  Se tiene pensado que el video que se reproduce sea enviado por la salida HDMI de la PC, de manera tal que el dispositivo 3 input- 1 output HDMI sacará a su salida (en la TV) el video de Youtube. Luego cuando comience nuevamente el programa, desactivará la salida HDMI y el dispositivo 3 input - 1 output HDMI conmutará automticamente seleccionando la única entrada HDMI que quedará activa y que será la del cable de televisión.

![Alt text](http://www.dhresource.com/0x0s/f2-albu-g2-M00-BB-77-rBVaG1bZlfuAI-CcAAFV4Utvrgs510.jpg/hdmi-splitter-3-input-1-output-hdmi-adapter.jpg "3 input 1 output")
  Éste modelo de conmutador HDMI tiene la particularidad que cambia automáticamente la entrada seleccionada HDMI a la última que se haya activado (la PC cuando detecte publicidad) y cuando se interrumpe la entrada HDMI seleccionada, retoma una entrada HDMI que se encuentre activa (cable de televisión estaría siempre activo). 
En caso de no tener este comportamiento del conmutador, podría implementarse una conmutación por hardware, siendo la PC la encargada de seleccionar que entrada HDMI desea que se muestre. Por ejemplo utilizando un microcontrolador Arduino.

<h1>Cablevisión Flow</h1>
 Puede que resulte engorrosa o costosa la implementación propuesta anteriormente, pero cada vez más se tienen a disposición live streaming de canales de TV, por ejemplo mediante la aplicación de Cablevisión llamada "Flow"
![Alt text](http://www.aletecno.com.ar/imagenes/cablevision-flow-plataforma-de-contenidos-online-cablevision-flow/1-pr.jpg "Cablevisión Flow")
 De esta manera se tendría acceso a las imágenes ya digitalizadas y en alta calidad. Haria falta un pequeño ajuste en el script para tomar dichos streamings de video como entradas para procesarlos.
 
<h1>HDMI Recorder</h1>
 Otra opción es ir grabando la señal HDMI de la TV, procesarla en la PC y enviarla luego a la TV. Ésto podría incrementar el delay entre la transmisión en vivo y lo que el usuario ve. Además el costo de éste tipo de aparatos suele ser elevado
 http://www.datapro.net/images/HDR-100.jpg
 
  
 <h1>Requisitos de Software*</h1>
    <ol>
    <li>Python</li>
    <li>"numpy" python</li>
    <li>"OpenCV" python</li>
    <li>mps-youtube</li>
    </ol>
*Por favor si se tiene algún problema comunicarse conmigo, es posible que haya olvidado algún requisito de software

Cualquier consulta mi correo electrónico es: cou_647@hotmail.com
