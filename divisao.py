def dividir(a, b):
    try:
        r = int(a) / int(b)
    except ZeroDivisionError:
        return 'zero!'
    except ValueError:
        return 'texto!'
    else:
        return r

print(dividir('9', '3'))   # ①
print(dividir('9', '0'))   # ②
print(dividir('9', 'x'))   # ③
print(dividir("9", None))