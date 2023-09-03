import re

# variable para almacenar datos

memoria = {
    
    "numeros": [(str(i)) for i in range(0,10)],
    "punto_cardinal":["north", "south", "west", "east"],
    "direccion1": ["front", "right", "left", "back"], # direccion 1 no tiene 'around'
    "direccion2":["left", "right", "around"], # direccion 2 no tiene ni 'front' ni 'back'
    "funciones": [] # aquí se van a almacenar las funciones que cree el ususario
    
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

"""print(oneValueArg("(((((12222)))))",memoria,"numeros")) # comprobacion oneValueArg"""    

def twoValueArg(token:str,memoria:str, tipo1:str, tipo2):
    
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

"""print(twoValueArg("(((((1212, left)))))",memoria,"numeros","direccion2")) # comprobacion twoValueArg"""

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


def tokenizacion_acciones(text:str):
    """
    La función recibe una linea de codigo y se encarga de buscar si existen acciones
    dentro de la linea, extraerlas junto a sus parametros y retornar esta información
    """
    
    commands = ['jump', 'walk', 'leap', 'turn', 'turnto', 'drop', 'get', 'grab', 'letGo', 'nop','facing']
    pattern =  r'(' + '|'.join(commands) + r')\s*(.*);\s*$'
    match = re.search(pattern, text)
    if match:
        return [match.group(1), match.group(2)]
    else:
        return False
"""print(tokenizacion_acciones(("jumpy(x     ,y) ")))"""

def check_while(text: str) -> str:
    if 'while' in text:
        index = text.index('while')
        value = text[index + len('while'):]
        info = check_condicional(value)
        return info
    else:
        return "The word 'while' is not in the text."
    

    
def check_condicional(text:str):
    if "facing" in text:
        #HAY QUE CORREGIR LA FUNCION A USAR PARA REVISAR FACING (ESTA EN MAIN)!!!!
        token = tokenizacion_acciones(text)
        value = oneValueArg(token)
        return value
    elif "can" in text:
        index = text.index('can')
        value = check_after_can(text)
        return value
    elif "not:" in text:
        index = text.index('not')
        return text[index + len('not'):]
    else:
        return False
    
def check_after_can(text:str):
    text = text.replace(" ","")
    if text[0] != "(":
        return False
    else:
        if '{' in text:
            index = text.index('{')
            code_afterb = text[index:]
            code_beforeb = text[:index-1]
        else:
            return False 
        result_1 = check_after_canp(code_beforeb)
        if result_1 == False:
            return False
        result_2 = check_whilebr(code_afterb)
        if result_2 == False:
            return False
        else:
            return True
            
def check_after_canp(text):
    
    info = chao_pescado(text)
    if info == False:
        return False
    else:
        token = tokenizacion_acciones(info)
        result = oneValueArg(token)
        return result
    
def check_whilebr(text:str):
    text = text.replace(" ", "")
    if text.count('{') == 1 and text.count('}') == 1:
        start = text.index('{') + 1
        end = text.index('}')
        if end == len(text) - 1:
            value = text[start:end]
        else:
            return False
    else:
        return False
    
    lista_acciones = value.split(";")
    for accion in lista_acciones:
        valor = oneValueArg(accion)
        if valor == False:
            return False
            break
            
    

print(check_while(" while cand(accion){accion}"))

    
    

        