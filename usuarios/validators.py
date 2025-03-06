# usuarios/validators.py
import re

def validar_rut_chileno(value):
    """
    Valida que el RUT chileno tenga el formato correcto y dígito verificador válido.
    Formato aceptado: 12345678-9 o 12.345.678-9
    """
    rut = value.upper().replace(".", "").replace("-", "")
    rut_regex = re.compile(r"^(\d{7,8})(\d|K)$")
    if not rut_regex.match(rut):
        raise ValidationError("Formato de RUT inválido")
    
    cuerpo, dv = rut_regex.match(rut).groups()
    cuerpo = cuerpo.zfill(8)  # Completa con ceros a la izquierda si es necesario
    
    # Cálculo del dígito verificador
    suma = 0
    multiplos = [3, 2, 7, 6, 5, 4, 3, 2]
    for i in range(8):
        suma += int(cuerpo[i]) * multiplos[i]
    
    resto = 11 - (suma % 11)
    if resto == 11:
        dv_calculado = "0"
    elif resto == 10:
        dv_calculado = "K"
    else:
        dv_calculado = str(resto)
    
    if dv != dv_calculado:
        raise ValidationError("Dígito verificador inválido")