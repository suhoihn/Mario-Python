digit = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
base = 4#Should be smaller than 36 inclusive
def Converter(num):
    if num // base == 0: return digit[num % base]
    return Converter(num // base) + digit[num % base]
    
print(Converter(36))

