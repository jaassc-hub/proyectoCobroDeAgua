from collections import defaultdict
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont # Para fuentes personalizadas si es necesario
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import mm, inch



from cobros.models import Pago, Pegue

MESES_ABREVIADOS = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
MESES_NUMEROS = list(range(1, 13))
meses = list(zip(MESES_NUMEROS, MESES_ABREVIADOS))

def index(request):
    return render(request, "cobros/index.html")

def cobro(request):
    pegues = Pegue.objects.all().select_related('abonado')
    anios = [2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
    print(meses)
    return render(request, "cobros/cobro.html", {"anios": anios, "meses": meses, "pegues": pegues})



#Pagos
def pagos_index(request):
   # Obtener todos los pagos, ordenados para asegurar que las fechas de pago    
    # se procesen correctamente y las sumas sean consistentes.
    todos_pagos = Pago.objects.all().select_related('pegue__abonado').prefetch_related('pegue__servicios').order_by('pegue__codigo_pegue', '-fecha_pago')
    
    # Estructura de agrupamiento: defaultdict para agrupar las transacciones
    pagos_agrupados = defaultdict(lambda: {
        'id': None,
        'codigo': '',
        'abonado': '',
        'barrio': '',
        'fecha_pago': None, 
        'monto_total': 0,
        'tarifa_actual': 0,
        'meses_pagados_str': []
    })

    for pago in todos_pagos:
        
        codigo = pago.pegue.codigo_pegue
        clave_agrupacion = (codigo, pago.fecha_pago)
        fila = pagos_agrupados[clave_agrupacion]

        if not fila['codigo']:
            fila['id'] = pago.id
            fila['codigo'] = codigo
            fila['abonado'] = pago.pegue.abonado.nombre
            fila['barrio'] = pago.pegue.barrio
            fila['fecha_pago'] = pago.fecha_pago # Fecha de la transacción


        fila['monto_total'] += pago.monto        
        pegue = pago.pegue 
        tarifa_calculada = sum(servicio.monto for servicio in pegue.servicios.filter(activo=True))
        fila['tarifa_actual'] = tarifa_calculada
        
        num_mes = (pago.mes)-1 # Usamos el mes del pago -1 porque la lista 'meses' es 0-indexada

        try:
            nombre_mes = meses[num_mes]
            fila['meses_pagados_str'].append(nombre_mes)
        except IndexError:
            # Manejo de error si el número de mes no es válido (ej. 0 o > 12)
            fila['meses_pagados_str'].append(f"Mes Inválido ({num_mes})")

    # Convertir a lista para pasar a la plantilla
    lista_final_pagos = list(pagos_agrupados.values())

    return render(request, "cobros/pagos.html", {
        "pagos": lista_final_pagos, 
    })

def registrar_pago(request):

    if request.method == "POST":
        data = request.POST
        codigo_pegue = data.get("pegue-id")
        anio_cobrado = data.get("anio-cobro")
        meses_cobrados = data.getlist("meses-cobro")
        metodo_pago = data.get("forma-cobro")
        total_pagar = data.get("total-pagar")


        print(meses_cobrados)
        print(metodo_pago)

        try:
            pegue_obj = Pegue.objects.get(codigo_pegue=codigo_pegue)
        except Pegue.DoesNotExist:
            return HttpResponse("Error: Código de Pegue no válido o faltante.", status=400)
        
        try:
            # Convertir Año a entero y Total a float o Decimal
            anio_cobrado = int(anio_cobrado)
            total_pagar = float(total_pagar)
            tarifa = total_pagar/len(meses_cobrados)
        except (TypeError, ValueError):
            return HttpResponse("Error: Datos numéricos (año/total) no válidos.", status=400)
        
        if not meses_cobrados:
            return HttpResponse("Error: Debe seleccionar al menos un mes.", status=400)
             
        try:
            with transaction.atomic():
                
                # Iteramos sobre la lista de meses para crear un registro por cada mes cobrado
                for mes in meses_cobrados:
                    
                    # Convertimos el valor del mes (ej. '1', '2') a entero
                    mes_cobrado = int(mes) 
                    
                    # Creamos la instancia de Pago y asignamos todos los atributos
                    Pago.objects.create(
                        pegue=pegue_obj,              # Objeto Pegue relacionado
                        anio=anio_cobrado,            # Año entero
                        mes=mes_cobrado,              # Mes entero (ej. 1, 2, 3)
                        monto=tarifa,                  # Monto calculado
                        forma_pago=metodo_pago,      # 'EFEC' o 'TRNF'
                        registrado_por_id= 1,           #Siempre lo registra con el usuario 1
                        # Asignar fecha_pago si tu modelo lo requiere
                    )
            
            # Si todo sale bien, redirigir a una página de éxito
            return redirect('cobro') 
        
        except Exception as e:
            # Manejar cualquier error de base de datos o lógica
            return HttpResponse(f"Error al guardar los pagos: {e}", status=500)


    return render(request,"cobros/registrar_pago.html")

pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))

def imprimir_recibo(request, id):
    pago = get_object_or_404(Pago, id=id)
    # Nombre del archivo
    filename = f"{pago.fecha_pago.strftime('%d_%m_%Y')}-{pago.pegue.codigo_pegue}_{pago.pegue.abonado}.pdf"

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Crea el canvas
    c = canvas.Canvas(response, pagesize=(76*mm, 290*mm))

    # Configura la fuente (Courier es ideal para matriciales)
    c.setFont("Courier", 8)
    data= {
        'Fecha': pago.fecha_pago.strftime('%d/%m/%Y'),
        'Monto' : f"L {pago.monto}",
        'Tarifa': pago.pegue.tarifa_mensual,
    }


    c.drawString(10*mm, 280*mm, "JUNTA DE AGUA Y SANEAMIENTO")
    c.drawString(10*mm, 275*mm, "      Santa Cruz           ")
    posicion_y = 260
    for clave, valor in data.items():
        c.drawString(10*mm, posicion_y*mm, f"{clave}: {valor}")
        posicion_y -= 5 # Baja la posición para la siguiente línea
        
    # Finaliza el PDF
    c.showPage()
    c.save()
    return response
