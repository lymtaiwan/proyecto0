
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

def auxiliar_numero_en_memoria(numero_str,memoria) -> bool:
    for digito in numero_str:
        if digito not in memoria["numeros"]:
            return False
    return True


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
        
    try:
        
        while (base_argument.count("(") > 0) and (base_argument.count("(") == base_argument.count(")")) and (auxiliar_parentesis(base_argument)):
            
            new_index1 = base_argument.find("(")
            new_index2 = base_argument.rfind(")")
            base_argument = base_argument[new_index1+1:new_index2]
            
            print(base_argument)
        
        base_argument = base_argument.rstrip(" ").lstrip(" ")
        
        print(base_argument)
        
    except:
        works = works and False
    
    
    if (base_argument not in memoria[tipo]):
        if not auxiliar_numero_en_memoria(base_argument,memoria):
            works = False
        
    
    return works
    

def twoValueArg(token:str,memoria:str, tipo1:str, tipo2):
    
    return
    