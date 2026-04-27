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


def calcular_color(fecha_ingreso):
    dias = dias_habiles(fecha_ingreso)

    if dias >= 55:
        return "rojo"
    elif dias >= 30:
        return "amarillo"
    else:
        return "verde"