from django.test import TestCase

from datetime import datetime ,date, timedelta



def nombreDia(n):
    if n==1:
        return f"lunes"
    if n==2:
        return "Martes"
    if n==3:
        return "Miercoles"
    if n==4:
        return "Jueves"
    if n==5:
        return "Viernes"
    if n==6:
        return "Sabado"
    if n==7:
        return "Domingo"

def current_date_format(date):
    months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    day = date.day  
    month = months[date.month - 1]
    year = date.year
    messsage = "{} de {} del {}".format(day, month, year)
    n = datetime.today().isoweekday()
    dia = nombreDia(n)
    return f"{dia} {messsage}"

now = date.today()

mañana = now + timedelta(days=1)
pasado = now + timedelta(days=2)

# print(mañana)
# print(pasado)
print(current_date_format(now))
# print(current_date_format(mañana))
# print(current_date_format(pasado))
# nombredia= datetime.today().weekday()

numeroDia = datetime.today().isoweekday()


def nombreDia(n):
    if n==1:
        return f"lunes"
    if n==2:
        return "Martes"
    if n==3:
        return "Miercoles"
    if n==4:
        return "Jueves"
    if n==5:
        return "Viernes"
    if n==6:
        return "Sabado"
    if n==7:
        return "Domingo"
    



def queDiaes():
    n = datetime.today().isoweekday()
    print(n)
    seisDia = n + 5
    nombre_dia =nombreDia(seisDia)
    return nombre_dia


print(queDiaes())
