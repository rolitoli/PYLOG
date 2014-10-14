print("                        PYLOG			@vuelvase.loco@")
print
print(">>Para agregar Hechos o Reglas ingrese el comando		<define>")
print(">>Para salir de este modo ingrese				</define>")
print(">>Para mostrar la Base de Conocimientos ingrese el comando	<base>")
print

#Lista global para manejar la base de conocimientos a la cual se anadira de manera volatil o temporal
global BaseConocimientos
BaseConocimientos=['nl','fail','write(args)'] 

#Lista global para manejar la validacion de los tokens admitidos por prolog en la validacion de sintaxis.
global Lexico
Lexico = ['_','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',',','.','(',')','[',']','-',':']

#Funcion que maneja el programa 
def main():
	linea=raw_input("?- ")
	if linea=='base':
		print
		print("Base de Conocimientos")
		print
		for i in range(0,len(BaseConocimientos)):
			print(BaseConocimientos[i])
		print
	elif linea=='define':
		#modo definicion de hechos y reglas.
		print("Ingresar Reglas o Hechos")
		MenuHechosReglas()
	elif linea[:5]=="write":
		if linea[len(linea)-3]=="(":
			print("Debe contener valores para imprimir")
			print("NO")
			return main()
		elif linea[len(linea)-1]!=".":
			print("Debe terminar con un punto")
			print("NO")
			return main()
		else:
			print(linea[(linea.index("(")+1):(linea.index(")"))])	
			print("YES")	
			return main()
	elif linea=="nl.":
		print
		print("YES")
		return main()
	else:
		return Consultas(linea)

#Funcion que maneja el menu para agre
def MenuHechosReglas():
	ingresar=raw_input(":- ")
	if ingresar=="":
		return MenuHechosReglas()
	elif ingresar=="/define":
		return main()
	elif EsRegla(ingresar):
		return GuardarRegla(ingresar)
	elif EsRegla(ingresar)==False:
		return GuardarHechos(ingresar)
	else:
		print("Entrada no valida")
		return MenuHechosReglas()
		

#Funcion que no recibe ningun vaalor y retorna un llamado a una funcion auxiliar
#Funcion que al leer un <define> se abre el modo de hechos
def GuardarHechos(hecho):
	if AnalizaLexicoHecho(hecho) and AnalizaSintaxisHecho(hecho): #Se le hace un analisis lexico y sintactico al hecho que se desea guardar
		BaseConocimientos.append(hecho) #Se agrega el hecho a la base de conocimientos
		print("Hecho ingresado")
		return MenuHechosReglas()
	else:
		print("Error al ingresar hecho a la Base de Conocimiento") 
		return MenuHechosReglas()

#Funcion que recibe el hecho y retorna true si es valido  el lexico y false caso contrario		
def AnalizaLexicoHecho(hecho):
	for caracter in hecho:
		#Si esta en mayuscula se pasa a minuscula y se revisa si esta en la lista de Lexico
		if caracter.lower() in Lexico[:-2]:
			True
		else:
			print("Error de scanner: "+caracter+" no es token valido")
			return False
	return True
	
#Funcion que recibe el hecho y valida la sintaxis 
def AnalizaSintaxisHecho(hecho):
	parentisis = False #bandera si se cumplen los parantesis
	if hecho[-1] != '.': #Validacion del punto al final
		print("Un hecho tiene que terminar con punto")
		return False
	else:
	
		for i in range(0,len(hecho)):
		
			#print (hecho[i])

			if i==0 and (hecho[i].islower() == False): #Validacion del hecho inicie con minuscula
				print("Un hecho tiene que empezar con Minuscula")
				return False
		
			elif hecho[i] == '(' :
				parentisis = True
				if ((hecho[i+1].isalnum() == False) and (hecho[i+1] != "_")):
					print("Error despues del ( ")
					return False
				elif parentisis == True:
					if hecho[-2] !=')':
						print("No se cerro parentesis")
						return False
			#validacion de que luego de la coma vaya un valor alfanumerico
			elif hecho[i] == ',':
				if ((hecho[i+1].isalnum() == False) and (hecho[i+1] != "_")):
					print("Error despues de la ,")
					return False
			
		return True 
			

#Funcion menu para guardar reglas.
def GuardarRegla(regla):
	if AnalizaLexicoRegla(regla) and AnalizaSintaxisRegla(regla) and ComprobarAridad(regla): 
		BaseConocimientos.append(regla)#Se agrega a la base de conocimientos si cumple el analisis lexico, sintactico y de aridad
		print("Regla ingresada")
		return MenuHechosReglas()
	else: 
		#capta si la regla no cumple las reglas
		print("Error al ingresar regla a la Base de Conocimiento") 
		return MenuHechosReglas()


#Funcion que recibe la regla y analiza que cumpla las reglas de Lexico
def AnalizaLexicoRegla(regla):
	for caracter in regla:
		if caracter.lower() in Lexico:
			True
		else:
			print("Error de scanner: "+caracter+" no es token valido")
			return False
	return True


#Funcion que recible la regla y revisa la sintaxis
def AnalizaSintaxisRegla(regla):
	dospuntos = False #bandera para revisar los dos puntos de la regla
	#Validacion de que termine con un punto la regla
	if regla[-1] != '.': 
		print("Una regla tiene que terminar con punto")
		return False
	
	else:
		regla = regla[:-1] 
		
		for i in range(0,len(regla)):
			if regla[i] == ':':
				dospuntos=True
				#Separa las reglas
				listaRegla=splitcoma_aux(splitcoma(regla[i+2:],0).split(","))  
				#Se revisa que el encabezado de la regla este correcto y se verifica que termine en :-
				if AnalizaSintaxisHecho(regla[:i]+'.') and regla[i+1]=="-": 
					 True
				else:
					return False
		if dospuntos==False:
			print("Error: No tiene los dos puntos" )
			return False
		else:
			for hecho in  listaRegla: #Ciclo para recorrer la lista que contiene la regla.
				if AnalizaSintaxisHecho(hecho+".") == False: 
					return False
			return True	


#Funcion para acomodar los argumentos para poder splitearlos correctamente con .split
def splitcoma(cadena,cont):
    largo=len(cadena)
    contador1=0
    contador2=0
    #Condicion de parada
    if cont>=largo: 
        return (cadena)
    else:
        if cont<largo-1:
            for i in range (cont,largo): 
                if cadena[i]=='(':
                    contador1=i 
                   
                    break
		elif (i==largo-1):
			return splitcoma(cadena,largo)
        if contador1+1<=largo-1: 
            for f in range (contador1+1,largo):
                if cadena[f]==')': 
                    contador2=f+1 
		
            
                    return splitcoma((cadena[:contador1]+(cadena[contador1:contador2].replace(",","."))+cadena[contador2:]),contador2) # envia lo que esta antes del parentesis, lo que esta dentro remplaza las , por . y envia lo que esta despues del parentesis. Y como segundo parametro envia la nueva posicion inicial despues de que se cierre el parentesis.



#Funcion auxiliar de splitcoma que se quitaron con la funcion de splitcoma
def splitcoma_aux(lista):
	lista_retorno=[]
	for hecho in lista:
		lista_retorno.append(hecho.replace(".",","))
	return lista_retorno
       

#Comprueba la aridad
def ComprobarAridad(regla):
	encabezadobase = ""
	encabezadoregla = ""
	particionregla=""
	particionbase=""

	for caracter in range(0,len(regla)):
		if regla[caracter] == ':':
			encabezadoregla = regla[:caracter]
			particionregla = encabezadoregla.partition("(") #Separa el string en la primera ocurrencia del parametro, y retorna una tupla de 3 elementos: la parte antes del separador, el separador mismo, y lo que esta despues del separador.

			

	
	for i in range(0,len(BaseConocimientos)):
		particionbase =  BaseConocimientos[i].partition("(") #Separa el string en la primera ocurrencia del parametro, y retorna una tupla de 3 elementos: la parte antes del separador, el separador mismo, y lo que esta despues del separador.

		
		if BaseConocimientos[i] == regla:
			print ("Regla ya existe en la Base")
			return False
		elif particionbase[0] == particionregla[0]:
			subparticionregla=particionregla[2].partition(")")
			subparticionbase=particionbase[2].partition(")")
			if len(subparticionbase[0]) == len(subparticionregla[0]):
				print ("Regla ya existe con la misma aridad")
				return False
	
	return True






#Funcion donde se realizan las consultas
def Consultas(consulta):
	#Si no se ingresa nada se reinicia la consulta
	if consulta=="": 
		return main()
	elif AnalizaLexicoHecho(consulta)==True and AnalizaSintaxisHecho(consulta)==True: 
		if Unificar(CrearLista(consulta))==True: 
			print("YES") 
		else:
			print("NO") 
		return main() 
	else:
		return main()

#Funcion que recibe los argumentos de la regla y la convierte en una lista
def CrearLista(argumento): 
	if EsBuiltIn(argumento)==3: 
		ListaConsulta=[] 
		for i in range(0,len(argumento)): 
			if argumento[i] == '(' : 
				functor = argumento[:i]
				predicado= argumento[i+1:-2]
		parametros=predicado.split(",") 
		ListaConsulta+=[functor]
		ListaConsulta+=[parametros] 
		return ListaConsulta
	else:
		return argumento

#Funcion para unificar las consultas
def Unificar(Consulta): 
	bandera=0
	largoBase=len(BaseConocimientos)
	for i in range(0,largoBase): 
		if EsBuiltIn(BaseConocimientos[i])!=3: 
			BuiltIn=EsBuiltIn(BaseConocimientos[i])
			if BuiltIn==1 and Consulta=="nl": 
				print
				bandera=1
			elif BuiltIn==2 and Consulta[:7]=="write(": 
				Escribir=Consulta[7:-1]
				if EsVariable(Escribir)==False: 
					print(Escribir)
					bandera=1
				else:
					print("es una variable")
		#Caso que se pueda unificar
		elif EsRegla(BaseConocimientos[i])!=True and EsBuiltIn(BaseConocimientos[i])==3: 
			listaBC=CrearLista(BaseConocimientos[i])
			#Verifica si se pueden unificar los elementos
			if Consulta[0]==listaBC[0] and len(Consulta[1])==len(listaBC[1]): 
				resultado=UnificacionArgumentos(Consulta[1],listaBC[1],len(Consulta[1]))
				if resultado==1: 
					return True #Que la unificacion fue correcta
				elif resultado==2: #backtracking
					bandera=1
				else:
					bandera=0 #No hubo unificacion
					
		#Trata de unificar con las reglas en las bases de conocimientos
		elif EsRegla(BaseConocimientos[i])==True and EsBuiltIn(BaseConocimientos[i])==3:
			regla=BaseConocimientos[i]
			#Separa predicado y regla
			for j in range(0,len(regla)): 
				if (regla[j] == ':') and (regla[j+1] == '-'): 
					parametros = regla[j+2:] 
					ListaRegla= CrearLista(regla[:j]+".") 
			#Verifica si la regla y la cantidad de argumentos son iguales
			if ListaRegla[0]==Consulta[0] and len(Consulta[1])==len(ListaRegla[1]): 
				#Se separan los parametros para poder compararlos
				ListaParametros = parametros[:-2].split('),') 
				for k in range(0,len(ListaParametros)):
					if ListaParametros[k][:3]=="nl,": 
						ListaParametros[k]+=")."
						ListaParametros=ListaParametros[:k]+['nl']+[ListaParametros[k][3:]]
					elif ListaParametros[k][:2]=="_,":
						ListaParametros[k]+=")."
						ListaParametros=ListaParametros[:k]+['_']+[ListaParametros[k][5:]]			
					elif ListaParametros[k][:7]=="write(": 
						ListaParametros[k]+=")"
					else:
						ListaParametros[k]+=")."
				#Se unifica
				for l in range(0,len(ListaParametros)): 
					if parametroslista[l]!="_": 
						if Unificar(CrearLista(ListaParametros[l])) == False: 
							return False
					else:
						True 
				return True
	if bandera==0: #Caso que no logro la unificacion
		return False
	elif bandera==1: #Caso de exito
		return True

#Funcion para poder distinguir una regla de un hecho y asi poder validar
def EsRegla(Consulta): 
	for i in range(0, len(Consulta)): 
		if Consulta[i] == ':' and Consulta[i+1] == '-':
			return True 
	return False

#Funcion para verificar si la palabra seleccionada es un built in function
def EsBuiltIn(letra): 
	if letra=="nl": 
		return 1
	elif letra[:7]=="write(" and letra[-1]==")":
		return 2
	else:
		return 3

#Funcion para unificar los argumentos
def UnificacionArgumentos(consulta, hecho, cantidad): 
	bandera=0 
	ValorBacktracking="" 
	n = 0 
	while (n<=((cantidad)-1)):
		#Caso de guion bajo siempre verdadero 
		if consulta[n]=="_": 
			n+=1
		
		#Comprueba que la consulta no sea una variable y el hecho si se unifican
		elif EsVariable(consulta[n]) == False and EsVariable(hecho[n]) == True:
			hecho[n] = consulta[n]
			n+=1 
		
		#Comprueba que la consulta no sea una variable y el hecho tampoco se unifican
		elif EsVariable(consulta[n]) == False and EsVariable(hecho[n]) == False: 
			if consulta[n] == hecho[n]:
				n+=1
				bandera=1 
			else:	
				return 0
		
		#Si la consulta es una variable y el hecho no unifica
		elif EsVariable(consulta[n]) == True and EsVariable(hecho[n])== False: 
			ValorBacktracking=consulta[n]+" = "+hecho[n] #Se guarda el backtraking
			n+=1
	#Se verifica si hay backtraking
	if ValorBacktracking!="": 
		res=raw_input(ValorBacktracking)
		if res==";":
			bandera=2 # 2 para indicar que si se desea backtracking.
		elif res=="":
			bandera=1 # 1 si solo desea continuar con la siguiente consulta.
		else:
			bandera=1
	return bandera # se retorna el valor de la unificacion de los parametros.

#Funcion para verificar si es una variable
def EsVariable(dato): 
	if dato.islower() == True: 
		return False 
	else: 
		return True
			
			

main()
