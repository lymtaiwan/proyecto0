import re

# variable para almacenar datos

memoria = {
    
    "contenido_programa": [], # se mete aquí el contenido del programa
    "numeros": [(str(i)) for i in range(0,10)],
    "punto_cardinal":["north", "south", "west", "east"],
    "direccion1": ["front", "right", "left", "back"], # direccion 1 no tiene 'around'
    "direccion2":["left", "right", "around"], # direccion 2 no tiene ni 'front' ni 'back'
    "funciones": [], # aquí se van a almacenar las funciones que cree el ususario
    "funciones_definidas" : {}, # {funcion:cantidad de parametros que recibe}
    
}



# lectura de datos

def lecturaPrograma(nombre_archivo:str):
    """
    El archivo queda cargado en 'memorias["contenido_programa"]'
    El archivo que se quiere leer tiene que epecificar su tipo, ej: 'ejemplo_programa.txt'
    
    """
    
    lista_lineas = []
    
    corchetes_abiertos = 0
    corchetes_cerrados = 0
    contenido_linea = " "
    
    
    with open(nombre_archivo) as archivo:
        for linea in archivo:
            linea_sin_salto = linea.strip()
            linea_sin_salto = linea_sin_salto.lower()
            
            if linea_sin_salto.rstrip(" ").lstrip(" ") == "{":
                corchetes_abiertos += 1
            if linea_sin_salto.rstrip(" ").lstrip(" ") == "}":
                corchetes_cerrados += 1
            
            
            if corchetes_abiertos == 0:
                lista_lineas.append(linea_sin_salto)
            else:
                contenido_linea = lista_lineas[-1] + " " + linea_sin_salto
                lista_lineas[-1] = contenido_linea
                
            if corchetes_abiertos == corchetes_cerrados:
                corchetes_abiertos = 0
                corchetes_cerrados = 0
                lista_lineas.append("")

        lista_filtrada = [elemento for elemento in lista_lineas if elemento != ""]
    memoria["contenido_programa"] = lista_filtrada
    
    return

(lecturaPrograma("ejemplo_programa.txt")) 
print(memoria["contenido_programa"])#Probando la lectura de las lineas """



# funciones auxiliares: 

def auxiliar_parentesis(stringconparentesis:str) -> bool:
    """ revisa que los '(' se cierren de manera correcta, solo funciona para cada único par """
    
    index1 = stringconparentesis.find("(")
    index2 = stringconparentesis.find(")")
    
    works = True
    if index1 > index2:
        works = works and False

    return works

def auxiliar_numero_en_memoria(numero_str,memoria,tipo) -> bool:
    
    """ 
    Revisa si el string se encuentra en la memoria, no necesariamente tiene que ser un número
    
    """
    
    
    for digito in numero_str:
        if digito not in memoria[tipo]:
            return False
    return True

def chao_pescado(base_argument):
    
    """_summary_

    Args:
        base_argument (_type_): cadena entre "()"

    Returns:
        _type_: True si se logran quitar los "()", false si no.
    """
    
 
    
    try:
        
        while (base_argument.count("(") > 0) and (base_argument.count("(") == base_argument.count(")")) and (auxiliar_parentesis(base_argument)):
            
            base_argument = base_argument.rstrip(" ").lstrip(" ")
            if  ((base_argument[0] not in [" ", "("]) or  (base_argument[-1] not in [" ", "", ")"])):
                x = "0"-1 # forzando un error porque buenas practicas 
            
            new_index1 = base_argument.find("(")
            new_index2 = base_argument.rfind(")")
            base_argument = base_argument[new_index1+1:new_index2]
            
        
        base_argument = base_argument.rstrip(" ").lstrip(" ")
        
        return base_argument
    
    except:
        
        return None

def enMemoria(cadena, memoria, tipo):
    works = True
    if (cadena not in memoria[tipo]):
        if not auxiliar_numero_en_memoria(cadena,memoria,tipo):
            works = works and False
    
    return works

# funciones para leer argumentos:

def oneValueArg(token:str, memoria:dict, tipo:str):
    
    """
    Args:
        token (str): (((( valor ))))
        memoria (dict): memoria
        tipo (str): tipo de dato en memoria. ej: numeros

    Returns:
        _type_: bool
    """
    
    base_argument = token.rstrip(" ").lstrip(" ")
    
    works = True
        
    chao_pez = chao_pescado(base_argument)  # chao pez seria los argumentos sin los '(' ')'
    if chao_pez != None:
        base_argument = chao_pez
    
    
    works = works and enMemoria(base_argument,memoria,tipo)
        
    
    return works

#print(oneValueArg("(  ((( (12222)) )))",memoria,"numeros")) # comprobacion oneValueArg"""    

def twoValueArg(token:str,memoria:dict, tipo1:str, tipo2):
    
    base_argument = token.lstrip(" ").rstrip(" ")
    
    works = True
        
    chao_pez = chao_pescado(base_argument) # chao pez seria los argumentos sin los '(' ')'
    if chao_pez != None:
        base_argument = chao_pez
        
    
    lista_valores = base_argument.split(",")
    
    if len(lista_valores) != 2:
        works = works and False
        
    else:
        
        valor1 = lista_valores[0].lstrip(" ").rstrip(" ")
        works = works and enMemoria(valor1,memoria,tipo1)
        
        valor2 = lista_valores[1].lstrip(" ").rstrip(" ")
        works = works and enMemoria(valor2,memoria,tipo2)
        
    return works

"""print(twoValueArg("(((((1212, left)))))",memoria,"numeros","direccion2")) # comprobacion twoValueArg"""

def iValueArg(token:str, lista_parametros:list):
    
    """
    Funciona igual que los otros valueArg solo que este recibe la lista de los posibles parametros de la función
    
    La cantidad de datos que se le ingresa se puede encontrar con ' memoria["funciones_definidas"][ # nombre de la funcion # ] '
    
    """
    cantidad_datos = len(lista_parametros)
    
    base_argument = token.lstrip(" ").rstrip(" ")
    works = True
    
    chao_pez = chao_pescado(base_argument) # chao pez seria los argumentos sin los '(' ')'
    
    if chao_pez != None:
        base_argument = chao_pez
    
    lista_valores = base_argument.split(",")
    
    
    
    if len(lista_valores) != cantidad_datos: 
        if cantidad_datos == 0:
            if base_argument != "":
                works = works and False
    elif cantidad_datos == 1:
        if base_argument == "":
                works = works and False
    
    for argumento in lista_valores:
        if argumento not in lista_parametros:
            works = works and False
    
    # en este no se hace lo del tipo ya que si lo del tipo 
    
    return works

"""print(iValueArg("(((( 1,as ))))", ["1","a"])) # comprobacion iValueArg"""


def noneValueArg(token:str):
    
    base_argument = token.rstrip(" ").lstrip(" ")
    works = True
    chao_pez = chao_pescado(base_argument)  # chao pez seria los argumentos sin los '(' ')'
    
    if chao_pez != None:
        base_argument = chao_pez.rstrip(" ")
    
    if base_argument != "":
        works = works and False
    
    return works

""" print(noneValueArg("( (((((( ))))))     )")) # comprobacion noneValueArg """


# funciones de definicion 

def defProcFuncional_parte1(line_content: list, memoria:dict) -> bool:
    
    """
    line_conntent = ["defProc", nombre_funcion, parametros]
    
    
    """
    
    works = True
    
    nombre_funcion = line_content[1]
    base_argument = line_content[2]
    
    works = True
    
    chao_pez = chao_pescado(base_argument) # chao pez seria los argumentos sin los '(' ')'

    if chao_pez != None:
        base_argument = chao_pez   
    else:
        works = works and False
        
    
    lista_valores = base_argument.split(",")
    memoria["funciones_definidas"][nombre_funcion] = lista_valores
    
    if len(line_content) != 3 :
        works = works and False
    
    return works

"""print(defProcFuncional_parte1(["defProc", "himalaya", "(  ( ( )))"],memoria))
print(memoria["funciones_definidas"]["himalaya"])#"""

def defVarFuncional(line_content:list, memoria:dict) -> bool:
    
    """
    Le llegan valores así: ["defVar", "nom","0"]
    """
    works = True
    
    var_name = line_content[1]
    var_value = line_content[2]
    
    if len(line_content) != 3:
        works = works and False
        
    else:
        
        count = 0
        for i in memoria:
            if enMemoria(var_value,memoria,i):
                memoria[i].append(var_name) # en caso de extender el codigo aquí habria que agregar un espacio donde se almacene el valr de la variable
                count += 1
        if count == 0:
            works = works and False
    
    return works


"""print(defVarFuncional(["defVar", "fotografia","123"],memoria)) # comprobacion defvar
print(twoValueArg("(((((fotografia, left)))))",memoria,"numeros","direccion2")) # comprobacion twoValueArg"""

def assigmentFuncional(line_content: list):
    """
    line_content[0] = nombre variable
    line_content[1] = '='
    line_content[2] = nuevo valor
    
    """
    nombre_variable = line_content[0]
    nuevo_valor = line_content[2]
    
    works = True
    
    count = 0 
    
    for i in memoria: # borra el registro que se tenia de la variable
        posibles_variables = memoria[i]
        if nombre_variable in posibles_variables: 
            posibles_variables = [elemento for elemento in posibles_variables if elemento != nombre_variable]
            memoria[i] = posibles_variables
            count += 1
    
    if count == 0:
        works = works and False # seria falso ya que no se ha declarado antes la variable
    
    if line_content[1] != "=":
        works = works and False 
    
    
    datos_acomodados = ["defvar", nombre_variable, nuevo_valor]
    defVarWorks = (defVarFuncional(datos_acomodados, memoria))
    works = works and defVarWorks
    
    return works

"""print(assigmentFuncional(["fotografia", "=", "8"])) # si se quiere un retorno positivo hay que agregar el nombre de la variable a memoria
print(memoria)#"""



# funciones acopladoras

def simpleCommand(line_content:list,):
    """
    Se le ingresa una lista de la forma [accion simple, argumento] y retorna si está bien o no. ej ["jump", "(12,3)"]. Ej 2. ["nop", "()"]
    """
    
    token = line_content[0]
    argumento = line_content[1]
    
    works = True
    
    if token == "jump":
        funciona = twoValueArg(argumento,memoria,"numeros","numeros")
        works = works and funciona
    elif token == "walk" or token == "leap":
        funciona = oneValueArg(argumento,memoria,"numeros") or twoValueArg(argumento,memoria,"numeros","direccion1") or twoValueArg(argumento,memoria,"numeros","punto_cardinal")
        works = works and funciona
    elif token == "turn":
        funciona = oneValueArg(argumento,memoria,"direccion2")
        works = works and funciona
    elif token in ["turnto","facing"]:
        funciona = oneValueArg(argumento,memoria,"punto_cardinal")
        works = works and funciona
    elif token in ["drop","get","grab","letgo"]:
        funciona = oneValueArg(argumento,memoria,"numeros")
        works = works and funciona
    elif token == "nop":
        funciona = noneValueArg(argumento)
        works = works and funciona
        
    return works

"""print(simpleCommand(["facing","( north)"])) #"""


# funciones de lectura

def tokenizacion_while(cadena:str)->list:
    return list





"""
me acabo de enterar que hay una libreria que lit hace lo que yo hice 

input_string = "((((((((( a aa, asd  ))))))"

# Eliminar los paréntesis y espacios en blanco redundantes
cleaned_string = re.sub(r'\s*[\(\)]\s*', '', input_string)

print(cleaned_string)"""