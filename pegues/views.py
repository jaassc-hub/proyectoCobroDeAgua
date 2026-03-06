from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from pegues.forms import PegueForm
from pegues.models import Pegue, Abonado
from django.urls import reverse



def obtener_informacion_pegue(request, codigo_pegue):  
    pegue = get_object_or_404(Pegue, codigo_pegue=codigo_pegue)
    ultimo_pago = pegue.pagos.all().first()
    nombre = pegue.abonado.nombre
    dni = pegue.abonado.dni
    barrio = pegue.barrio.nombre
    linea_distribucion = pegue.linea_distribucion.codigo if pegue.linea_distribucion else "N/A"
    tarifa = sum(servicio.monto for servicio in pegue.servicios.filter(activo=True))
    servicios = list([servicio.nombre for servicio in pegue.servicios.filter(activo=True)])

    if ultimo_pago:
        datos_ultimo_pago = {
            'id': ultimo_pago.id,
            'fecha_pago': ultimo_pago.fecha_pago if ultimo_pago.fecha_pago else None,
            'monto': ultimo_pago.monto,
            'mes': ultimo_pago.mes, 
            'anio': ultimo_pago.anio,
        }
    else:   
        datos_ultimo_pago = None

    return JsonResponse({'nombre': nombre , 'dni' : dni, 'tarifa_mensual': tarifa, 'barrio': barrio, 'linea_distribucion': linea_distribucion, 'servicios': servicios, 'ultimo_pago': datos_ultimo_pago})

def view(request):
    pegues = Pegue.objects.all().order_by('codigo_pegue')
    return render(request, "pegues/listado_pegues.html", {"pegues": pegues})

def create(request):

    if request.method == 'POST':
        form = PegueForm(request.POST)
        if form.is_valid():
            form.save()
            response = HttpResponse()
            response['HX-Redirect'] = reverse('pegues:view')
            return response         
    else: 
        form = PegueForm()

    return render(request, "pegues/create_pegue.html", {'form': form})



def edit(request, id):
    pegue = get_object_or_404(Pegue, id=id)

    if request.method == 'POST':
        form = PegueForm(request.POST, instance=pegue)
        if form.is_valid():
            form.save()
            response = HttpResponse()
            response['HX-Redirect'] = reverse('pegues:view')
            return response
    else:
        form = PegueForm(instance=pegue)

    return render(request, 'pegues/edit_pegue.html', {'form': form, 'pegue': pegue})

def delete(request, id):
    pegue = get_object_or_404(Pegue, id=id)

    if request.method == 'POST':
        pegue.delete()
        response = HttpResponse()
        response['HX-Redirect'] = reverse('pegues:view')
        return response

    return render(request, 'pegues/delete_pegue.html', {'pegue': pegue})
    
def pegues_mora(request):
    return render(request, "pegues/pegues_mora.html")

def pegues_inhabilitados(request):
    pegues = Pegue.objects.all().filter(estado='INH')
    return render(request, "pegues/pegues_inhabilitados.html", {"pegues": pegues})

def pegues_corrales(request):
    pegues = Pegue.objects.all().filter(tipo='COR')
    return render(request, "pegues/pegues_corrales.html", {"pegues": pegues})

def pegues_solares(request):
    pegues = Pegue.objects.all().filter(tipo='SOL')
    return render(request, "pegues/pegues_solares.html", {"pegues": pegues})

def pegues_vendidos(request):
    return render(request, "pegues/pegues_vendidos.html")

def pegues_futuro(request):
    return render(request, "pegues/pegues_futuro.html")

