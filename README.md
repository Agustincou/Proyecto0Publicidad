# Proyecto0Publicidad
 <h1>Proyecto 0 Publicidad</h1>
 
  Script Python que hace uso de OpenCV para la detección de logos de un canal de TV para diferenciar entre los programas y el espacio publicitario.

![Alt text](https://github.com/Agustincou/Proyecto0Publicidad/blob/master/Expicativo%20Proyecto%200P.png "Posible Implementación Casera")

  El script correrá en la PC, la cual puede obtener las imágenes de la TV ya sea por una camara web (implementado en el código), por streaming de video (no implementado pero posible) o archivo de video pregrabado.
La PC al detectar que ha comenzado el espacio publicitario (al dejar de detectar el logo del canal) realizará una determinada acción. En este caso se pensó en reproducir un video de Youtube que desee el usuario/programador. Por el momento la reproducción del video se produce únicamente en la PC utilizando la aplicación mps-youtube que permite mediante comandos de consola reproducir cualquier video de Youtube.

  Se tiene pensado que el video que se reproduce sea enviado por la salida HDMI de la PC, de manera tal que el dispositivo 3 input- 1 output HDMI sacará a su salida (en la TV) el video de Youtube. Luego cuando comience nuevamente el programa, desactivará la salida HDMI y el dispositivo 3 input - 1 output HDMI conmutará automticamente seleccionando la única entrada HDMI que quedará activa y que será la del cable de televisión.

![Alt text](http://www.dhresource.com/0x0s/f2-albu-g2-M00-BB-77-rBVaG1bZlfuAI-CcAAFV4Utvrgs510.jpg/hdmi-splitter-3-input-1-output-hdmi-adapter.jpg "3 input 1 output")
  Éste modelo de conmutador HDMI tiene la particularidad que cambia automáticamente la entrada seleccionada HDMI a la última que se haya activado (la PC cuando detecte publicidad) y cuando se interrumpe la entrada HDMI seleccionada, retoma una entrada HDMI que se encuentre activa (cable de televisión estaría siempre activo). 
En caso de no tener este comportamiento del conmutador, podría implementarse una conmutación por hardware, siendo la PC la encargada de seleccionar que entrada HDMI desea que se muestre. Por ejemplo utilizando un microcontrolador Arduino.



 <h1>Requisitos de Software*</h1>
    <ol>
    <li>Python</li>
    <li>"numpy" python</li>
    <li>"OpenCV" python</li>
    <li>mps-youtube</li>
    </ol>
*Por favor si se tiene algún problema comunicarse conmigo

Cualquier consulta mi correo electrónico es: cou_647@hotmail.com
