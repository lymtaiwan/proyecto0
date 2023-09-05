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
    "comandos_funcion" : {}
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
                
                try:
    
                    if "defproc" in lista_lineas[-2]:
                        contenido_linea = lista_lineas[-2] + linea_sin_salto
                        lista_lineas[-2] = contenido_linea
                    else:
                        contenido_linea = lista_lineas[-1] + linea_sin_salto
                        lista_lineas[-1] = contenido_linea
                except:
                    contenido_linea = lista_lineas[-1] + linea_sin_salto
                    lista_lineas[-1] = contenido_linea
                
            if corchetes_abiertos == corchetes_cerrados:
                corchetes_abiertos = 0
                corchetes_cerrados = 0
                lista_lineas.append("")

        lista_filtrada = [elemento for elemento in lista_lineas if elemento != ""]
    memoria["contenido_programa"] = lista_filtrada
    
    return
#(lecturaPrograma("ejemplo_programa.txt")) 
#print(memoria["contenido_programa"])#Probando la lectura de las lineas """



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

    
    if base_argument.count("(") != base_argument.count(")"):
        works = works and False

    if nombre_funcion == "":
        works = works and False
    
    if chao_pez != None:
        base_argument = chao_pez   
    else:
        works = works and False
        
    
    lista_valores = base_argument.split(",")
    memoria["funciones_definidas"][nombre_funcion] = lista_valores
    
    for valor in lista_valores:
        memoria["numeros"].append(valor)
        memoria["punto_cardinal"].append(valor)
        memoria["direccion1"].append(valor)
        memoria["direccion2"].append(valor)
    
    if len(line_content) != 3 :
        works = works and False
    
    return works

#print(defProcFuncional_parte1(["defProc", "himalaya", "(  ( ( )))"],memoria))
#print(memoria["funciones_definidas"]["himalaya"])#"""

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

def parentesis(base_argument):
    
    """_summary_

    Args:
        base_argument (_type_): cadena entre "()"

    Returns:
        _type_: True si se logran quitar los "()", false si no.
    """
    
 
    
    try:
        
        while (base_argument.count("(") > 1) and (base_argument.count("(") == base_argument.count(")")) and (auxiliar_parentesis(base_argument)):
            
            base_argument = base_argument.rstrip(" ").lstrip(" ")
            if  ((base_argument[0] not in [" ", "("]) or  (base_argument[-1] not in [" ", "", ")"])):
                x = "0"-1 # forzando un error porque buenas practicas 
            
            new_index1 = base_argument.find("(")
            new_index2 = base_argument.rfind(")")
            base_argument = base_argument[new_index1+1:new_index2]
            
        
        base_argument = base_argument.rstrip(" ").lstrip(" ")
        
        return base_argument
    
    except:
        
        return False

def tokenizacion_acciones(text:str):
    """
    La función recibe una linea de codigo y se encarga de buscar si existen acciones
    dentro de la linea, extraerlas junto a sus parametros y retornar esta información
    """
    
    commands = ['jump', 'walk', 'leap', 'turnto', 'turn', 'drop', 'get', 'grab', 'letgo', 'nop','facing']
    pattern =  r'(' + '|'.join(commands) + r')\s*(.*);\s*$'
    match = re.search(pattern, text)
    if match:
        return [match.group(1), match.group(2)]
    else:
        return False
#print(tokenizacion_acciones(("jumpy(x     ,y); ")))

def check_while(text: str) -> str:
    text = text.replace(" ", "")
    if ('while' in text) and (text.startswith("while")):
        index = text.index('while')
        value = text[index + len('while'):]
        info = check_condicional(value)
        return info
    else:
        return False
    

    
def check_condicional(text:str):
    text = text.replace(" ", "")
    if "facing" in text and (text.startswith("facing")):
        if '{' in text:
            index = text.index('{')
            code_afterb = text[index:]
            code_beforeb = text[:index] + ";"
        else:
            return False 
        token = tokenizacion_acciones(code_beforeb)
        value = simpleCommand(token)
        value_2 = revisar_bloque(code_afterb)
        return value and value_2
    elif ("can" in text) and (text.startswith("can")):
        index = text.index('can')
        text_after_can = text[index + len("can"):]
        value = check_after_can(text_after_can)
        return value
    elif "not:" in text and (text.startswith("not:")):
        index = text.index('not:')
        condition =  text[index + len('not:'):]
        value = check_condicional(condition)
        return value
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
            code_beforeb = text[:index]
        else:
            return False 
        result_1 = check_after_canp(code_beforeb)
        if result_1 == False:
            return False
        result_2 = revisar_bloque(code_afterb)
        if result_2 == False:
            return False
        else:
            return True
            
def check_after_canp(text):
    
    old_text =text
    newtext = parentesis(text) 
    if newtext == old_text or newtext == False:
        return False
    else:
        newtext = newtext + ";"
        token = tokenizacion_acciones(newtext)
        result = simpleCommand(token)
        return result
    
def check_whilebr(text:str):
    text = text.replace(" ", "")
    new_text = bracket_c(text)
    if text != new_text and text.startswith("{"):
        start = text.index('{') + 1
        end = text.index('}')
        if end == len(text) - 1:
            value = text[start:end]
        else:
            return False
    else:
        return False
    
    if value == "":
        return True
    lista_acciones = value.split(";")
    for accion in lista_acciones:
        token = tokenizacion_acciones(accion + ";")
        if token == False:
            return False
        valor = simpleCommand(token)
        if valor == False:
            return False
            break
    return valor

        
#print(check_while(" while can(walk(1 , north ) ) { walk(1 , north ) ;jump(2,3) }"))

def check_if(text:str):
    text.replace(" ", "")
    text = text.lower()
    if ("if" in text) and (text.startswith("if")) and ("else" in text):
        text = extract_if_else(text)
        text_if = text[0]
        text_else = text[1]
        index = text_if.index('if')
        value_if = text_if[index + len('if'):]
        
        index_else = text_else.index('else')
        value_else = text_else[index_else + len('else'):]
        
        info = check_condicional(value_if)
        info2 = check_else(value_else)
        return info and info2
    else:
        return False    
    
def check_else(text:str):
    text = text.replace(" ", "")
    info = check_whilebr(text)
    return info
        
            
def extract_if_else(text: str):
    index_if = text.index("if")
    index_else = text.index("else")
    after_if = text[index_if:index_else]
    after_else = text[index_else:]
    return after_if, after_else    



def check_rep(text: str):
    text = text.replace(" ", "")
    text = text.lower()
    pattern = r'^repeat\s*\d+\s*times\s*\{.*\}$'
    match = re.search(pattern, text)
    index = text.index("times")
    text_at = text[index + len("times"):]
    bracket_ceck = bracket_c(text_at)
    if bracket_ceck == text_at or bracket_ceck == False:
        return False
    value = check_whilebr(text_at)
    
    return bool(match) and value
    



def bracket_c(base_argument):
    
    """_summary_

    Args:
        base_argument (_type_): cadena entre "()"

    Returns:
        _type_: True si se logran quitar los "()", false si no.
    """
    
 
    
    try:
        
        while (base_argument.count("{") > 0) and (base_argument.count("{") == base_argument.count("}")) and (auxiliar_bracket(base_argument)):
            
            base_argument = base_argument.rstrip(" ").lstrip(" ")
            if  ((base_argument[0] not in [" ", "{"]) or  (base_argument[-1] not in [" ", "", "}"])):
                x = "0"-1 # forzando un error porque buenas practicas 
            
            new_index1 = base_argument.find("{")
            new_index2 = base_argument.rfind("}")
            base_argument = base_argument[new_index1+1:new_index2]
            
        
        base_argument = base_argument.rstrip(" ").lstrip(" ")
        
        return base_argument
    
    except:
        
        return False
    
def auxiliar_bracket(stringconparentesis:str) -> bool:
    """ revisa que los '(' se cierren de manera correcta, solo funciona para cada único par """
    
    index1 = stringconparentesis.find("{")
    index2 = stringconparentesis.find("}")
    
    works = True
    if index1 > index2:
        works = works and False

    return works

#print(check_rep("repeat 8 times {}"))
#print(check_if("if can(walk(3)){}else{}"))

def revisar_bloque(text:str):
    
    valor = True
    lista_verdad = []
    lista_posible_i = ["walk","jump","leap","turn","turnto","drop","get","grab","letgo","nop","while","repeat","if"]
    text = text.replace(" ", "")
    check_1 = bracket_c(text)
    if text[1:len(text)-1].startswith("if") or text[1:len(text)-1].startswith("while") or text[1:len(text)-1].startswith("repeat"):
        check_1 = "dif"
    if text == "{}":
        return True
    
    if text == check_1 or not text.endswith("}") or not text.startswith("{"):
        return False
    else:
        text = text[1:len(text)-1]
        if text.startswith("if"):
            block_content = []
            block_content.append(text)
        else:
            block_content = split_text(text)
        
        for item in block_content:
            item = item.lower()
            funcion_propia = False
            inicio = False
            if item.startswith(lista_posible_i[0]) or item.startswith(lista_posible_i[1]) or item.startswith(lista_posible_i[2]) or item.startswith(lista_posible_i[3]) or item.startswith(lista_posible_i[4]) or item.startswith(lista_posible_i[5]) or item.startswith(lista_posible_i[6]) or item.startswith(lista_posible_i[7]) or item.startswith(lista_posible_i[8]) or item.startswith(lista_posible_i[9]):
                token = tokenizacion_acciones(item + ";")
                value = simpleCommand(token)
                if value == False:
                    return False
                else:
                    lista_verdad.append(True)
            if item.startswith(lista_posible_i[10]):
                value = check_while(item)
                if value == False:
                    return False
                else:
                    lista_verdad.append(True)
                
            if item.startswith(lista_posible_i[11]):
                value = check_rep(item)
                if value == False:
                    return False
                else:
                    lista_verdad.append(True)
            if item.startswith(lista_posible_i[12]):
                value = check_if(item)
                if value == False:
                    return False
                else:
                    lista_verdad.append(True)
                    
            for key in memoria["funciones_definidas"].keys():
                if item.startswith(key):
                    funcion_propia =  True
                    
            if funcion_propia == True:
                value = lector_funciones(item)  
                if value == False:
                    return value
                else:
                    lista_verdad.append(True)  
            
            if funcion_propia != True:    
                for v in lista_posible_i:
                    if v in item:
                        inicio = True
                lista_verdad.append(inicio)
                
        for verdad in lista_verdad:
            valor = valor and verdad
        return valor
                
                
            

def split_text(text: str):
    result = []
    start = 0
    level = 0
    for i, char in enumerate(text):
        if char == "{":
            level += 1
        elif char == "}":
            level -= 1
        elif char == ";" and level == 0:
            result.append(text[start:i].strip())
            start = i + 1
    result.append(text[start:].strip())
    return result

def bloque_proc(text:str):
    text = text.replace(" ", "")
    index1 = text.index("{")
    index2 = text.index("(")
    bloque = text[index1:]
    nombre_proc = text[len("defProc"):index2]
    parametros = text[index2:index1]
    lista_val = ["defProc",nombre_proc,parametros]
    value = defProcFuncional_parte1(lista_val,memoria)
    if value == False:
        return False
    memoria["comandos_funcion"][nombre_proc] = bloque
    if nombre_proc in bloque:
        index1 = bloque.index(nombre_proc)
        if bloque[index1-1:index1] == ";":
            bloque = bloque[:index1 -1] + bloque[index1+len(nombre_proc)+2:]
            bloque = bloque.replace(nombre_proc,"")
        if bloque[index1-1:index1] == ";" and bloque[index1 + len(nombre_proc)+ 3] == ";":
            bloque = bloque[:index1 -1] + bloque[index1+len(nombre_proc)+3:]
            bloque = bloque.replace(nombre_proc,"")
        else:
            bloque = bloque.replace(nombre_proc,"")
            
            
    valor = revisar_bloque(bloque)
    values_to_remove = chao_pescado(parametros)
    values_to_remove = values_to_remove.split(",")
    memoria["numeros"] = [x for x in memoria["numeros"] if x not in values_to_remove]
    memoria["direccion1"] = [x for x in memoria["direccion1"] if x not in values_to_remove]
    memoria["direccion2"] = [x for x in memoria["direccion2"] if x not in values_to_remove]
    memoria["punto_cardinal"] = [x for x in memoria["punto_cardinal"] if x not in values_to_remove]

    
    return valor

def lector_funciones(text:str):
    text = text.replace(" ","")
    funcion_propia = False
    for key in memoria["funciones_definidas"].keys():
        if text.startswith(key):
            funcion_propia =  True 
            nombre_funcion = key
            
    if funcion_propia == True:
        index1 = text.index(nombre_funcion)
        text_after_name = text[index1 + len(nombre_funcion):]
        lista_parametros = memoria["funciones_definidas"][nombre_funcion]
        if text_after_name.startswith("("):
            parametros = chao_pescado(text_after_name)
            if parametros == text_after_name:
                return False
            parametros = parametros.split(",")
            if len(parametros) != len(lista_parametros):
                return False
            
            bloque_funcion = memoria["comandos_funcion"][nombre_funcion]
            bloque_funcion = replace_parameters(bloque_funcion,parametros,lista_parametros)
            value = revisar_bloque(bloque_funcion)
        else:
            return False
    return value    
             
def replace_parameters(text:str,values:list,parameters:list):
    for i in range(len(values)):
        text = text.replace(f'({parameters[i]})', f'({values[i]})')
        text = text.replace(f',{parameters[i]})', f',{values[i]})')
        text = text.replace(f'({parameters[i]},', f'({values[i]},')
        text = text.replace(f',{parameters[i]},', f',{values[i]},')
    return text
      
            
def coronador(lista_archivo:list):  
    lista_posible_i = ["walk","jump","leap","turn","turnto","drop","get","grab","letgo","nop","while","repeat","if"]
    funcion_propia = False
    inicio = False
    try:
  
        for linea in lista_archivo:
            #linea = linea.replace(" ", "")
            if linea.startswith("{"):
                value = revisar_bloque(linea)
                if value == False:
                    return False
                
            elif linea.startswith("defproc"):
                value = bloque_proc(linea)
                if value == False:
                    return False
                
                
            elif linea.startswith("defvar"):
                lista = linea.split(" ")
                value = defVarFuncional(lista,memoria)
                if value == False:
                    return False
                
            elif linea.startswith(lista_posible_i[0]) or linea.startswith(lista_posible_i[1]) or linea.startswith(lista_posible_i[2]) or linea.startswith(lista_posible_i[3]) or linea.startswith(lista_posible_i[4]) or linea.startswith(lista_posible_i[5]) or linea.startswith(lista_posible_i[6]) or linea.startswith(lista_posible_i[7]) or linea.startswith(lista_posible_i[8]) or linea.startswith(lista_posible_i[9]):
                value = simpleCommand(linea)
                if value == False:
                    return False
                
            elif linea.startswith(lista_posible_i[10]):
                value = check_while(linea)
                if value == False:
                    return False
                
            elif linea.startswith(lista_posible_i[11]):
                value = check_rep(linea)
                if value == False:
                    return False
                
            elif linea.startswith(lista_posible_i[12]):
                value = check_if(linea)
                if value == False:
                    return False
                
            for key in memoria["funciones_definidas"].keys():
                    if linea.startswith(key):
                        funcion_propia =  True
            
            if funcion_propia == True:
                value = lector_funciones(linea)
                if value == False:
                    return False
        
            if funcion_propia != True:    
                    for v in lista_posible_i:
                        if v in linea or "defvar" in linea or "defproc" in linea:
                            inicio = True
                    
        return inicio
    except Exception as e:
        print(repr(e))
        
lecturaPrograma("ejemplo_programa2.txt")
#print(memoria["contenido_programa"])
print(coronador(memoria["contenido_programa"]))