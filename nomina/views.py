from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Empleado, Cargo, Departamento, TipoContrato, Rol
from .forms import EmpleadoForm, CargoForm, DepartamentoForm, TipoContratoForm, RolForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

def home(request):
    data = {
        'title': 'PagoNET',
        'description': 'Sistema de Nomina de Pagos',
        'author': 'Estudiantes_POO_B2',
        'year': 2025,
    }
    # doctores = Doctor.objects.all()
    # data["doctores"]=doctores
    #return HttpResponse("<h1>Hola Mundo, Mi primer pagina con django</h1>")
    #return JsonResponse(data)  
    return render(request, 'home.html', data)

def singup(request):
    return HttpResponse("<h1>Hola Mundo, Mi primer pagina con django</h1>")

def empleado_list(request):
    query = request.GET.get('q', None)
    if query:
        empleados = Empleado.objects.filter(
            Q(nombre__icontains=query) |          # Búsqueda por nombre
            Q(cedula__icontains=query) |          # Búsqueda por cédula
            Q(direccion__icontains=query) |       # Búsqueda por dirección
            Q(cargo__descripcion__icontains=query) |  # Búsqueda por cargo
            Q(departamento__descripcion__icontains=query) |  # Búsqueda por departamento
            Q(tipo_contrato__descripcion__icontains=query) |  # Búsqueda por tipo de contrato
            Q(sexo__icontains=query)              # Búsqueda por sexo 
        ).distinct().order_by('nombre')  # Orden alfabético por nombre
    else:
        empleados = Empleado.objects.all().order_by('nombre')
    
    context = {
        'empleados': empleados,
        'title': 'Listado de empleados',
        'query': query  # Para mantener el término de búsqueda en el template
    }
    return render(request, 'empleado/list.html', context)

def empleado_create(request):
    context={'title':'Ingresar Empleado'}
    print("metodo: ",request.method)
    if request.method == "GET":
        # print("entro por get")
        
        form = EmpleadoForm()# instancia el formulario con los campos vacios
        context['form'] = form
        return render(request, 'empleado/create.html', context)
    else:
        #  print("entro por post")
        form = EmpleadoForm(request.POST) # instancia el formulario con los datos del post
        if form.is_valid():
            form.save()
            # doctor = form.save(commit=False)# lo tiene en memoria
            # doctor.user = request.user
            # doctor.save() # lo guarda en la BD
            return redirect('nomina:empleado_list')
        else:
            context['form'] = form
            return render(request, 'empleado/create.html',context) 
        #return JsonResponse({"message": "voy a crear un doctor"})

def empleado_update(request,id):
    context={'title':'Actualizar Empleado'}
    empleado = Empleado.objects.get(pk=id)
    if request.method == "GET":
        form = EmpleadoForm(instance=empleado)# instancia el formulario con los datos del doctor
        context['form'] = form
        return render(request, 'empleado/create.html', context)
    else:
        form = EmpleadoForm(request.POST,instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('nomina:empleado_list')
        else:
            context['form'] = form
            return render(request, 'empleado/create.html', context)

def empleado_delete(request,id):
    empleado=None
    try:
        empleado = Empleado.objects.get(pk=id)
        if request.method == "GET":
            context = {'title':'Empleado a Eliminar','empleado':empleado,'error':''}
            return render(request, 'empleado/delete.html',context)  
        else: 
            empleado.delete()
            return redirect('nomina:empleado_list')
    except:
        context = {'title':'Datos del Empleado','empleado':empleado,'error':'Error al eliminar al empleado'}
        return render(request, 'empleado/delete.html',context)

def cargo_list(request):
    # doctors = Doctor.objects.all()
    # print("doctors: ",doctors)
    # print("doctores: ",doctors.values())
    # print("metodo: ",request.method)
    # print("valor de get: ",request.GET,request.GET.get('q'))
    # return JsonResponse(list(doctors.values()), safe=False)
    query = request.GET.get('q', None)
    print(query)
    if query:
        cargos = Cargo.objects.filter(descripcion__icontains=query)
    else:
        cargos = Cargo.objects.all()
    context = {'cargos': cargos, 'title': 'Listado de cargos'}
    return render(request, 'cargo/list.html', context)

def cargo_create(request):
    context = {'title': 'Ingresar Cargo'}
    print("metodo: ", request.method)
    if request.method == "GET":
        # print("entro por get")
        
        form = CargoForm()  # instancia el formulario con los campos vacios
        context['form'] = form
        return render(request, 'cargo/create.html', context)
    else:
        # print("entro por post")
        form = CargoForm(request.POST)  # instancia el formulario con los datos del post
        if form.is_valid():
            form.save()
            # doctor = form.save(commit=False)# lo tiene en memoria
            # doctor.user = request.user
            # doctor.save() # lo guarda en la BD
            return redirect('nomina:cargo_list')
        else:
            context['form'] = form
            return render(request, 'cargo/create.html', context)
        #return JsonResponse({"message": "voy a crear un doctor"})

def cargo_update(request, id):
    context = {'title': 'Actualizar Cargo'}
    cargo = Cargo.objects.get(pk=id)
    if request.method == "GET":
        form = CargoForm(instance=cargo)  # instancia el formulario con los datos del cargo
        context['form'] = form
        return render(request, 'cargo/create.html', context)
    else:
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            return redirect('nomina:cargo_list')
        else:
            context['form'] = form
            return render(request, 'cargo/create.html', context)

def cargo_delete(request, id):
    cargo = None
    try:
        cargo = Cargo.objects.get(pk=id)
        if request.method == "GET":
            context = {'title': 'Cargo a Eliminar', 'cargo': cargo, 'error': ''}
            return render(request, 'cargo/delete.html', context)
        else:
            cargo.delete()
            return redirect('nomina:cargo_list')
    except:
        context = {'title': 'Datos del Cargo', 'cargo': cargo, 'error': 'Error al eliminar el cargo'}
        return render(request, 'cargo/delete.html', context)

def departamento_list(request):
    # doctors = Doctor.objects.all()
    # print("doctors: ",doctors)
    # print("doctores: ",doctors.values())
    # print("metodo: ",request.method)
    # print("valor de get: ",request.GET,request.GET.get('q'))
    # return JsonResponse(list(doctors.values()), safe=False)
    query = request.GET.get('q', None)
    print(query)
    if query:
        departamentos = Departamento.objects.filter(descripcion__icontains=query)
    else:
        departamentos = Departamento.objects.all()
    context = {'departamentos': departamentos, 'title': 'Listado de departamentos'}
    return render(request, 'departamento/list.html', context)

def departamento_create(request):
    context = {'title': 'Ingresar Departamento'}
    print("metodo: ", request.method)
    if request.method == "GET":
        # print("entro por get")
        
        form = DepartamentoForm()  # instancia el formulario con los campos vacios
        context['form'] = form
        return render(request, 'departamento/create.html', context)
    else:
        # print("entro por post")
        form = DepartamentoForm(request.POST)  # instancia el formulario con los datos del post
        if form.is_valid():
            form.save()
            # doctor = form.save(commit=False)# lo tiene en memoria
            # doctor.user = request.user
            # doctor.save() # lo guarda en la BD
            return redirect('nomina:departamento_list')
        else:
            context['form'] = form
            return render(request, 'departamento/create.html', context)
        #return JsonResponse({"message": "voy a crear un doctor"})

def departamento_update(request, id):
    context = {'title': 'Actualizar Departamento'}
    departamento = Departamento.objects.get(pk=id)
    if request.method == "GET":
        form = DepartamentoForm(instance=departamento)  # instancia el formulario con los datos del departamento
        context['form'] = form
        return render(request, 'departamento/create.html', context)
    else:
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            return redirect('nomina:departamento_list')
        else:
            context['form'] = form
            return render(request, 'departamento/create.html', context)

def departamento_delete(request, id):
    departamento = None
    try:
        departamento = Departamento.objects.get(pk=id)
        if request.method == "GET":
            context = {'title': 'Departamento a Eliminar', 'departamento': departamento, 'error': ''}
            return render(request, 'departamento/delete.html', context)
        else:
            departamento.delete()
            return redirect('nomina:departamento_list')
    except:
        context = {'title': 'Datos del Departamento', 'departamento': departamento, 'error': 'Error al eliminar el departamento'}
        return render(request, 'departamento/delete.html', context)

def tipocontrato_list(request):
    # doctors = Doctor.objects.all()
    # print("doctors: ",doctors)
    # print("doctores: ",doctors.values())
    # print("metodo: ",request.method)
    # print("valor de get: ",request.GET,request.GET.get('q'))
    # return JsonResponse(list(doctors.values()), safe=False)
    query = request.GET.get('q', None)
    print(query)
    if query:
        tipos_contrato = TipoContrato.objects.filter(descripcion__icontains=query)
    else:
        tipos_contrato = TipoContrato.objects.all()
    context = {'tipos_contrato': tipos_contrato, 'title': 'Listado de tipos de contrato'}
    return render(request, 'tipocontrato/list.html', context)

def tipocontrato_create(request):
    context = {'title': 'Ingresar Tipo de Contrato'}
    print("metodo: ", request.method)
    if request.method == "GET":
        # print("entro por get")
        
        form = TipoContratoForm()  # instancia el formulario con los campos vacios
        context['form'] = form
        return render(request, 'tipocontrato/create.html', context)
    else:
        # print("entro por post")
        form = TipoContratoForm(request.POST)  # instancia el formulario con los datos del post
        if form.is_valid():
            form.save()
            # doctor = form.save(commit=False)# lo tiene en memoria
            # doctor.user = request.user
            # doctor.save() # lo guarda en la BD
            return redirect('nomina:tipocontrato_list')
        else:
            context['form'] = form
            return render(request, 'tipocontrato/create.html', context)
        #return JsonResponse({"message": "voy a crear un doctor"})

def tipocontrato_update(request, id):
    context = {'title': 'Actualizar Tipo de Contrato'}
    tipo_contrato = TipoContrato.objects.get(pk=id)
    if request.method == "GET":
        form = TipoContratoForm(instance=tipo_contrato)  # instancia el formulario con los datos del tipo de contrato
        context['form'] = form
        return render(request, 'tipocontrato/create.html', context)
    else:
        form = TipoContratoForm(request.POST, instance=tipo_contrato)
        if form.is_valid():
            form.save()
            return redirect('nomina:tipocontrato_list')
        else:
            context['form'] = form
            return render(request, 'tipo_contrato/create.html', context)

def tipocontrato_delete(request, id):
    tipo_contrato = None
    try:
        tipo_contrato = TipoContrato.objects.get(pk=id)
        if request.method == "GET":
            context = {'title': 'Tipo de Contrato a Eliminar', 'tipo_contrato': tipo_contrato, 'error': ''}
            return render(request, 'tipocontrato/delete.html', context)
        else:
            tipo_contrato.delete()
            return redirect('nomina:tipocontrato_list')
    except:
        context = {'title': 'Datos del Tipo de Contrato', 'tipo_contrato': tipo_contrato, 'error': 'Error al eliminar el tipo de contrato'}
        return render(request, 'tipocontrato/delete.html', context)

def rolpago_list(request):
    query = request.GET.get('q', None)
    
    if query:
        roles = Rol.objects.filter(
            Q(empleado__nombre__icontains=query) |    # Búsqueda por nombre de empleado
            Q(empleado__cedula__icontains=query) |    # Búsqueda por cédula de empleado
            Q(aniomes__icontains=query) |             # Búsqueda por periodo (formato YYYY-MM)
            Q(sueldo__icontains=query) |              # Búsqueda por monto de sueldo
            Q(horas_extra__icontains=query) |         # Búsqueda por horas extra
            Q(bono__icontains=query) |                # Búsqueda por bono
            Q(neto__icontains=query) |                # Búsqueda por neto
            Q(empleado__cargo__descripcion__icontains=query) |  # Búsqueda por cargo del empleado
            Q(empleado__departamento__descripcion__icontains=query)  # Búsqueda por departamento
        ).distinct().order_by('-aniomes', 'empleado__nombre')  # Orden por fecha descendente y nombre
    else:
        roles = Rol.objects.all().order_by('-aniomes', 'empleado__nombre')
    
    context = {
        'roles': roles,
        'title': 'Listado de roles de pago',
        'query': query  # Para mantener el término de búsqueda en el template
    }
    return render(request, 'rolpago/list.html', context)

def rolpago_create(request):
    if request.method == "POST":
        form = RolForm(request.POST)
        if form.is_valid():
            try:
                rol = form.save()
                print(f"Rol guardado - ID: {rol.id}")  # Debug
                return redirect('nomina:rolpago_list')
            except Exception as e:
                print(f"Error al guardar: {str(e)}")  # Debug
        else:
            print("Formulario inválido:", form.errors)  # Debug
    else:
        form = RolForm()
    
    return render(request, 'rolpago/create.html', {'form': form, 'title': 'Ingresar Rol de Pago'})

def rolpago_update(request, id):
    context = {'title': 'Actualizar Rol de Pago'}
    rol_pago = Rol.objects.get(pk=id)
    if request.method == "GET":
        form = RolForm(instance=rol_pago)  # instancia el formulario con los datos del rol de pago
        context['form'] = form
        return render(request, 'rolpago/create.html', context)
    else:
        form = RolForm(request.POST, instance=rol_pago)
        if form.is_valid():
            form.save()
            return redirect('nomina:rolpago_list')
        else:
            context['form'] = form
            return render(request, 'rol_pago/create.html', context)

def rolpago_delete(request, id):
    rol_pago = None
    try:
        rol_pago = Rol.objects.get(pk=id)
        if request.method == "GET":
            context = {'title': 'Rol de Pago a Eliminar', 'rol_pago': rol_pago, 'error': ''}
            return render(request, 'rolpago/delete.html', context)
        else:
            rol_pago.delete()
            return redirect('nomina:rolpago_list')
    except:
        context = {'title': 'Datos del Rol de Pago', 'rol_pago': rol_pago, 'error': 'Error al eliminar el rol de pago'}
        return render(request, 'rolpago/delete.html', context)
    

