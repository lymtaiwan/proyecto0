



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
    
    si taka lo quiere romper, no creo que lo pueda romper * felicidad
    
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
                    
                    while num.count("(") == num.count(")") and num.count("(") > 0 :
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
    
print(jump("jump  (   (12),   13  )" ))

print("Hola taiwanes")

