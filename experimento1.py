def quieroAmor(a):
    print(a)
    return True

def noQuieroAmor(b):
    print(b)
    return False

espacio_vectorial = {}

espacio_vectorial["uno"] = quieroAmor

#print(espacio_vectorial["uno"]("me das un besito? uwu"))

a = 10 # este no afecta

exec("quieroAmor(a)")

defProc = lambda a, b : exec("quieroAmor(a)") and exec("noQuieroAmor(b)")

print(defProc("holamundooo", "espejito rebotin")) 

### se me ocurre hacer una lista con las acciones y hacerle replace a los parametros como si fueran una llave. tipo [] 1 y [] 2, remplazar []1[1] con []2[1]