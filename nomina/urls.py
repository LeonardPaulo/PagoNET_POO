from django.urls import path
from nomina.views import empleado_create, empleado_list, empleado_update, empleado_delete, cargo_list, cargo_create, cargo_update, cargo_delete, departamento_list, departamento_create, departamento_update, departamento_delete, rolpago_list, rolpago_create, rolpago_update, rolpago_delete, tipocontrato_list, tipocontrato_create, tipocontrato_update, tipocontrato_delete
app_name = 'nomina'  # Nombre de la aplicación para el espacio de nombres
urlpatterns = [
    path('empleado_list/',empleado_list, name='empleado_list'),  # URL para la vista home
    path('empleado_create/',empleado_create, name='empleado_create'),  # URL para la vista home
    path('empleado_update/<int:id>/',empleado_update, name='empleado_update'),
    path('empleado_delete/<int:id>/',empleado_delete, name='empleado_delete'),
    path('cargo_list/',cargo_list, name='cargo_list'),  # URL para la vista home
    path('cargo_create/',cargo_create, name='cargo_create'),  # URL para la vista home
    path('cargo_update/<int:id>/',cargo_update, name='cargo_update'),
    path('cargo_delete/<int:id>/',cargo_delete, name='cargo_delete'),
    path('departamento_list/',departamento_list, name='departamento_list'),  # URL para la vista home
    path('departamento_create/',departamento_create, name='departamento_create'),  # URL para la vista home
    path('departamento_update/<int:id>/',departamento_update, name='departamento_update'),
    path('departamento_delete/<int:id>/',departamento_delete, name='departamento_delete'),
    path('company/rolpago_list/',rolpago_list, name='rolpago_list'),  # URL para la vista home
    path('company/rolpago_create/',rolpago_create, name='rolpago_create'),  # URL para la vista home
    path('rolpago_update/<int:id>/',rolpago_update, name='rolpago_update'),
    path('rolpago_delete/<int:id>/',rolpago_delete, name='rolpago_delete'),
    path('tipocontrato_list/',tipocontrato_list, name='tipocontrato_list'),  # URL para la vista home
    path('tipocontrato_create/',tipocontrato_create, name='tipocontrato_create'),  # URL para la vista home
    path('tipocontrato_update/<int:id>/',tipocontrato_update, name='tipocontrato_update'),
    path('tipocontrato_delete/<int:id>/',tipocontrato_delete, name='tipocontrato_delete'),
]

