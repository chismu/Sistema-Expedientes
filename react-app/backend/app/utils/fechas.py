from datetime import date, timedelta

def dias_habiles(fecha_inicio):
    hoy = date.today()
    dias = 0
    actual = fecha_inicio

    while actual < hoy:
        if actual.weekday() < 5:
            dias += 1
        actual += timedelta(days=1)

    return dias


from datetime import date

def calcular_estado(fecha_ingreso):
    hoy = date.today()
    dias = (hoy - fecha_ingreso).days

    if dias < 30:
        return "verde", "baja", dias
    elif dias < 45:
        return "amarillo", "media", dias
    elif dias < 55:
        return "naranja", "alta", dias
    elif dias < 60:
        return "rojo", "urgente", dias
    else:
        return "rojo_oscuro", "critica", dias