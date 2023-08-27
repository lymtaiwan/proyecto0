
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
    for digito in numero_str:
        if digito not in memoria[tipo]:
            return False
    return True

def chao_pescado(base_argument):
    
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

#print(oneValueArg("(((((12222)))))",memoria,"numeros")) # comprobacion oneValueArg    

def twoValueArg(token:str,memoria:str, tipo1:str, tipo2):
    
    base_argument = token.lstrip(" ").rstrip(" ")
    
    works = True
        
    chao_pez = chao_pescado(base_argument) # chao pez seria los argumentos sin los '(' ')'
    if chao_pez != None:
        base_argument = chao_pez
        
    print(base_argument)
    
    lista_valores = base_argument.split(",")
    
    if len(lista_valores) != 2:
        works = False
        
    else:
        
        valor1 = lista_valores[0].lstrip(" ").rstrip(" ")
        works = works and enMemoria(valor1,memoria,tipo1)
        
        valor2 = lista_valores[1].lstrip(" ").rstrip(" ")
        works = works and enMemoria(valor2,memoria,tipo2)
        
    return works

# print(twoValueArg("(((((12, left )))))",memoria,"numeros","direccion2")) # comprobacion twoValueArg