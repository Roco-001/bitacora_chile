from django import template
import pandas as pd
from ..models import Incidencia, Elemento
from django.utils import  timezone

register = template.Library()

@register.filter(name='get_color')
def get_color(id):
    incidencias =Incidencia.objects.get(id=id)
    now = timezone.now()
    if incidencias.proxima_actualizacion and incidencias.estado != 'Resuelto':
        tiempo_excedido = now - incidencias.proxima_actualizacion

        tiempo_segundos = tiempo_excedido.total_seconds()

        if tiempo_segundos <= 0:
            return "#2838AD"
        elif tiempo_segundos <= 900:
            return "#1D8127"
        elif tiempo_segundos <= 1800:
            return "#F5A00B"
        else:
            return "#E53115"
    else:
        return '0BA3F5'
    


@register.filter(name='get_elementos')
def get_elementos(id):
    elementos = Elemento.objects.filter(get_elementos = id)
    name =[]
    for elemento in elementos:
        name.append(elemento.nombre)

    if len(name) == 0:
        return 'No hay elementos asociados'
    else:
        nama_str = ", ".join(name)
        return nama_str
