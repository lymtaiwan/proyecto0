import re

# variable para almacenar datos

memoria = {
    
    "numeros": [(str(i)) for i in range(0,10)],
    "punto_cardinal":["north", "south", "west", "east"],
    "direccion1": ["front", "right", "left", "back"], # direccion 1 no tiene 'around'
    "direccion2":["left", "right", "around"], # direccion 2 no tiene ni 'front' ni 'back'
    "funciones": [], # aquí se van a almacenar las funciones que cree el ususario
    "funciones_definidas" : {}, # {funcion:cantidad de parametros que recibe}
    
}

# funciones auxiliares: 

def auxiliar_parentesis(stringconparentesis:str) -> bool:
    """ revisa que los '(' se cierren de manera correcta, solo funciona para cada único par """
    
    index1 = stringconparentesis.find("(")
    index2 = stringconparentesis.find(")")
    
    works = True
    if index1 > index2:
        works = False

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
                print("XD")
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
            works = False
    
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
        works = False
        
    else:
        
        valor1 = lista_valores[0].lstrip(" ").rstrip(" ")
        works = works and enMemoria(valor1,memoria,tipo1)
        
        valor2 = lista_valores[1].lstrip(" ").rstrip(" ")
        works = works and enMemoria(valor2,memoria,tipo2)
        
    return works

#print(twoValueArg("(((((1212, left)))))",memoria,"numeros","direccion2")) # comprobacion twoValueArg"""

def iValueArg(token:str, cantidad_datos):
    
    """
    Funciona igual que los otros valueArg solo que este no revisa que el tipo de dato
    
    La cantidad de datos que se le ingresa se puede encontrar con ' memoria["funciones_definidas"][ # nombre de la funcion # ] '
    
    """
    
    base_argument = token.lstrip(" ").rstrip(" ")
    works = True
    
    chao_pez = chao_pescado(base_argument) # chao pez seria los argumentos sin los '(' ')'
    
    if chao_pez != None:
        base_argument = chao_pez
    
    lista_valores = base_argument.split(",")
    
    if len(lista_valores) != cantidad_datos:
        works = False
    
    # en este no se hace lo del tipo ya que si lo del tipo 
    
    return works

"""print(iValueArg("(   ((( a, b,c   ))))", 3)) # comprobacion iValueArg"""


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
        works = False
        
    
    lista_valores = base_argument.split(",")
    memoria["funciones_definidas"][nombre_funcion] = lista_valores
    
    if len(line_content) != 3 :
        works = works and False
    
    return works

"""print(defProcFuncional_parte1(["defProc", "himalaya", "(  ( (a, b,s)))"],memoria))
print(memoria["funciones_definidas"]["himalaya"])#"""

def defVarFuncional(line_content:list, memoria:dict) -> bool:
    
    """
    Le llegan valores así: ["defVar", "nom","0"]
    """
    works = True
    
    var_name = line_content[1]
    var_value = line_content[2]
    
    if len(line_content) != 3 :
        works = works and False
        
    else:
        
        for i in memoria:
            if enMemoria(var_value,memoria,i):
                memoria[i].append(var_name) # en caso de extender el codigo aquí habria que agregar un espacio donde se almacene el valr de la variable

        
    return works


"""print(defVarFuncional(["defVar", "nom","123"],memoria)) # comprobacion defvar
print(twoValueArg("(((((nom, left)))))",memoria,"numeros","direccion2")) # comprobacion twoValueArg"""



# funciones de lectura

def tokenizacion_while(cadena:str)->list:
    return list





"""
me acabo de enterar que hay una libreria que lit hace lo que yo hice 

input_string = "((((((((( a aa, asd  ))))))"

# Eliminar los paréntesis y espacios en blanco redundantes
cleaned_string = re.sub(r'\s*[\(\)]\s*', '', input_string)

print(cleaned_string)"""