 ORG 1000h ; área de memoria para datos por convención, por ejemplo variables y constantes
texto DB ? ; define una etiqueta 'texto' que funciona como variable


 ORG 2000h
MOV AL, 1 ; inicializa en 1 AL
MOV BX, OFFSET texto ; carga en BX la dirección de texto
R:INT 6 ; queda a la espera de input del teclado
CMP BYTE PTR [BX], 0Ah ; chequea si lo que se leyó es ENTER
JZ F ; si la comparación da cero salta a F
CMP BYTE PTR [BX], 41h ; chequea si es 'A'
JS N
CMP BYTE PTR [BX], 5Bh ; chequea si es 'Z'
JNS N
CMP BYTE PTR [BX], 61h ; chequea si es 'a'
JS N
CMP BYTE PTR [BX], 7Bh ; chequea si es 'z'
JNS N
INT 7 ; imprime en pantalla AL caracteres, leyendo desde la dirección guardada en BX
N: JMP R ; salta incondicionalmente a R
F: HLT ; finaliza la ejecución del ciclo de instrucciones

END ; fin del programa