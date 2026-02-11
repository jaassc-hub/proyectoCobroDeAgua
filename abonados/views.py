from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.http import HttpResponse

from abonados.models import Abonado
from abonados.forms import AbonadoForm
from pegues.models import Pegue

MESES_ABREVIADOS = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
MESES_NUMEROS = list(range(1, 13))
meses = list(zip(MESES_NUMEROS, MESES_ABREVIADOS))


# Abonados
def abonados_index(request):
    abonados = Abonado.objects.all()
    return render(request, "abonados_index.html", {"abonados": abonados})

def buscar_abonado(request, nombre):
    abonados = Pegue.objects.filter(abonado__nombre__icontains=nombre).select_related('id').values('codigo_pegue', 'abonado__nombre', 'barrio', 'abonado__dni')
    abonadosBusqueda = [{"codigo": abonado['codigo_pegue'], "nombre": abonado['abonado__nombre'] , "dni": abonado['abonado__dni']} for abonado in abonados]
    return JsonResponse({"abonadosBusqueda": abonadosBusqueda})

def agregar_abonado_buscador(request, codigo_pegue):

    try:
        pegue_seleccionado = Pegue.objects.get(codigo_pegue=codigo_pegue)
    except Pegue.DoesNotExist:

        return JsonResponse({'Pegue no encontrado'}, status=404)
    pegue = get_object_or_404(Pegue, codigo_pegue=codigo_pegue)

    return JsonResponse({
        'codigo_pegue': pegue_seleccionado,
    })

def crear_abonado(request):
    if(request.method == 'POST'):
        form = AbonadoForm(request.POST)
        if form.is_valid():
            form.save()
            response = HttpResponse()
            response['HX-Redirect'] = reverse('abonados:view')
            print("Si lo guarda")

            return response
        else:
            return redirect('abonados:view')
            print("No lo guarda")
        
    else:
        form = AbonadoForm()
    
    return render(request, 'crear_abonado.html', {'form': form})

