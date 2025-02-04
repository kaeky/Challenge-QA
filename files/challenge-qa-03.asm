 ORG 1000h ; área de memoria para datos por convención, por ejemplo variables y constantes
texto DB ? ; define una etiqueta 'texto' que funciona como variable


 ORG 2000h
MOV AL, 0 ; inicializa en 0 AL
MOV BX, OFFSET texto ; carga en BX la dirección de texto
R:INT 6 ; queda a la espera de input del teclado
CMP BYTE PTR [BX], 0Ah ; chequea si lo que se leyó es ENTER
JZ F ; si la comparación da cero salta a F
INC AL ; incrementa AL
JC O ; el tamaño máximo de AL es 255 por lo que finaliza
INC BX ; incrementa BX, que es la dirección de destino
JMP R ; salta incondicionalmente a R
F: MOV BX, OFFSET texto ; carga en BX la dirección de texto
INT 7 ; imprime en pantalla AL carácteres, leyendo desde la dirección guardada en BX
O: MOV AL, 255
JMP F
HLT ; finaliza la ejecución del ciclo de instrucciones

END ; fin del programa