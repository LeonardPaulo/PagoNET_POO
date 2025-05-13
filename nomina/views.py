from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Empleado, Cargo, Departamento, TipoContrato, Rol
from .forms import EmpleadoForm, CargoForm, DepartamentoForm, TipoContratoForm, RolForm
from django.db.models import Q
from django.core.paginator import Paginator

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

def empleado_list(request):
    query = request.GET.get('q', None)
    order_by = request.GET.get('order_by', 'nombre')
    direction = request.GET.get('direction', 'asc')
    
    if query:
        empleados_list = Empleado.objects.filter(
            Q(nombre__icontains=query) |
            Q(cedula__icontains=query) |
            Q(direccion__icontains=query) |
            Q(cargo__descripcion__icontains=query) |
            Q(departamento__descripcion__icontains=query) |
            Q(tipo_contrato__descripcion__icontains=query) |
            Q(sexo__icontains=query)
        ).distinct()
    else:
        empleados_list = Empleado.objects.all()
    
    # Aplicar ordenamiento
    if direction == 'desc':
        order_by = f'-{order_by}'
    
    empleados_list = empleados_list.order_by(order_by)
    
    paginator = Paginator(empleados_list, 4)
    page_number = request.GET.get('page')
    empleados = paginator.get_page(page_number)
    
    context = {
        'empleados': empleados,
        'title': 'Listado de empleados',
        'query': query,
        'order_by': order_by.replace('-', '') if '-' in order_by else order_by,
        'direction': direction
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
    query = request.GET.get('q', None)
    order_by = request.GET.get('order_by', 'id')
    direction = request.GET.get('direction', 'asc')  # Valor por defecto: ascendente
    print(query)
    
    if query:
        cargos_list = Cargo.objects.filter(descripcion__icontains=query)
    else:
        cargos_list = Cargo.objects.all()
    
    # Aplicar ordenamiento
    if order_by == 'nombre':
        field = 'descripcion'
    else:
        field = 'id'
    
    if direction == 'desc':
        field = f'-{field}'
    
    cargos_list = cargos_list.order_by(field)
    
    paginator = Paginator(cargos_list, 4)
    page_number = request.GET.get('page')
    cargos = paginator.get_page(page_number)
    
    context = {
        'cargos': cargos,
        'title': 'Listado de cargos',
        'query': query,
        'order_by': order_by,
        'direction': direction
    }
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
    query = request.GET.get('q', None)
    order_by = request.GET.get('order_by', 'id')
    direction = request.GET.get('direction', 'asc')
    
    if query:
        departamentos_list = Departamento.objects.filter(descripcion__icontains=query)
    else:
        departamentos_list = Departamento.objects.all()
    
    # Aplicar ordenamiento
    if direction == 'desc':
        order_by = f'-{order_by}'
    
    departamentos_list = departamentos_list.order_by(order_by)
    
    paginator = Paginator(departamentos_list, 4)
    page_number = request.GET.get('page')
    departamentos = paginator.get_page(page_number)
    
    context = {
        'departamentos': departamentos,
        'title': 'Listado de departamentos',
        'query': query,
        'order_by': order_by.replace('-', '') if '-' in order_by else order_by,
        'direction': direction
    }
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
    query = request.GET.get('q', None)
    order_by = request.GET.get('order_by', 'id')
    direction = request.GET.get('direction', 'asc')
    
    if query:
        tipos_contrato_list = TipoContrato.objects.filter(descripcion__icontains=query)
    else:
        tipos_contrato_list = TipoContrato.objects.all()
    
    # Aplicar ordenamiento
    if direction == 'desc':
        order_by = f'-{order_by}'
    
    tipos_contrato_list = tipos_contrato_list.order_by(order_by)
    
    paginator = Paginator(tipos_contrato_list, 4)
    page_number = request.GET.get('page')
    tipos_contrato = paginator.get_page(page_number)
    
    context = {
        'tipos_contrato': tipos_contrato,
        'title': 'Listado de tipos de contrato',
        'query': query,
        'order_by': order_by.replace('-', '') if '-' in order_by else order_by,
        'direction': direction
    }
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
    order_by = request.GET.get('order_by', '-aniomes')
    direction = request.GET.get('direction', 'asc')
    
    if query:
        roles_list = Rol.objects.filter(
            Q(empleado__nombre__icontains=query) |
            Q(empleado__cedula__icontains=query) |
            Q(aniomes__icontains=query) |
            Q(sueldo__icontains=query) |
            Q(horas_extra__icontains=query) |
            Q(bono__icontains=query) |
            Q(neto__icontains=query) |
            Q(empleado__cargo__descripcion__icontains=query) |
            Q(empleado__departamento__descripcion__icontains=query)
        ).distinct()
    else:
        roles_list = Rol.objects.all()
    
    # Aplicar ordenamiento
    if direction == 'desc':
        order_by = f'-{order_by}'
    
    roles_list = roles_list.order_by(order_by)
    
    paginator = Paginator(roles_list, 4)
    page_number = request.GET.get('page')
    roles = paginator.get_page(page_number)
    
    context = {
        'roles': roles,
        'title': 'Listado de roles de pago',
        'query': query,
        'order_by': order_by.replace('-', '') if '-' in order_by else order_by,
        'direction': direction
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
    

