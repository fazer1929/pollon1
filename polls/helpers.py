def inttohex(s):
    val =  hex(int(s)*1234)
    return str(val)

def hextoint(s):
    
    val  = int(str(s), 16)
    return val//1234