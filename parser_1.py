



program_info = {
    "initialized_vars": {},
                }

# defVar

def defVar(line_content:list, program_info:dict) -> bool:
    
    works = True
    
    var_name = str(line_content[1])
    var_value = float(line_content[2])
    
    if len(line_content) != 3 :
        works = False  
    else:
        program_info["initialized_vars"][var_name] = var_value
    
    return works


# Assigment 

def assigment():
    return None

# jump 

def jump(command_jump:str)-> bool:
    
    """ 
    lo ideal es que reciba un 'jump(valor_1 : int, valor_2 : int)' sin valores de espacio al rededor.
    
    si taka lo quiere romper creo que no lo puede romper
    
    """ 
    
    command_info = command_jump.replace("jump","").lstrip(" ")
    
    works = True
    
    works = works and command_info.count("(") == command_info.count(")")
    works = works and (command_info.count(",") == 1)
    works = works and ("jump" in command_jump[:4])
    
    

    info_str = str(command_info[1 :-1]) # str "12, 34" - no tiene ()
    
    
    info_list = []
    try:
        for num in info_str.split(','):
            try:
                
                info_list.append(int(num))
            except:
                
                num = num.lstrip(" ").rstrip(" ")
                
                possible_vars = ["0","1","2","3","4","5","6","7","8","9","(",")"," "]
                possible_argument = True
                
                for elemet in list(num):
                    possible_argument = possible_argument and possible_vars.__contains__(elemet)
                    
                if possible_argument:
                    print("XD")
                    
                    while num.count("(") == num.count(")") and num.count("(") > 0 and auxiliarParentesis(num):
                        num = num[1 :-1]
                        print("XDXD")
                    
                info_list.append(int(num))
        print(info_list)
        works = works and True
    except:
        works = works and False
        info_list = []
        
    works = works and len(info_list) == 2  
    
    return works
    
#print(jump("jump  (   (12),   13  )" ))

def nop(command_nop:str) -> bool:
    """
    nop( "no p() ") -> false
    nop( "    nop   () " ) -> true

    """
    filtered_command = ""
    
    if "nop" in command_nop:
        filtered_command = command_nop.strip("nop")
    
    filtered_command = filtered_command.replace(" ", "")
    
    works = True
    
    if filtered_command.count("()") != 1 or len(filtered_command) > 2:
        works = False
    
    return works



def oneValueArg(one_value_arg_command:str):
    
    one_value_arg_command = one_value_arg_command.rstrip(" ").lstrip(" ")
    
    works = True
    
    # condicion 1
    index1 = str(one_value_arg_command).rfind("(")
    works = works and True if index1 != -1 else works and False # si no hay "(" está mal escrito
    
    # condicion 2 - palabra permitida
    base_command = one_value_arg_command[:index1].lstrip(" ")
    possible_base_command = ["walk", "leap", "drop","get", "grab", "letgo","turn","turnto"]
    works = works and True if base_command in possible_base_command else works and False
    
    # condicion 3 - parametros correctos 
    
    base_argument = one_value_arg_command.rstrip(base_command).rstrip(" ")
    
    if base_command not in ["turn", "turnto"]:
        try:
            while (base_command.count("(") > 0) and (base_command.count("(") == base_command.count(")")):
                base_command.rstrip("(").rsplit(")")
                break
            
            
            
        except:
            print("a llorar")
    
    
    
    
    
    return False

"""print("Hola taiwanes")
print("arabia saudita")"""

def auxiliarParentesis(stringconparentesis:str) -> bool:
    """ revisa que los '(' se cierren de manera correcta, solo funciona para cada único par """
    
    index1 = stringconparentesis.find("(")
    index2 = stringconparentesis.find(")")
    
    works = True
    if index1 > index2:
        works = False

    return works


