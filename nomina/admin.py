from django.contrib import admin
from .models import Cargo, Departamento, TipoContrato, Empleado, Rol
from django.utils.html import format_html

class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'sueldo_formateado', 'cargo', 'departamento', 'tipo_contrato')
    list_filter = ('cargo', 'departamento', 'tipo_contrato', 'sexo')
    search_fields = ('nombre', 'cedula')
    list_per_page = 20
    
    def sueldo_formateado(self, obj):
        return f"${obj.sueldo:,.2f}"
    sueldo_formateado.short_description = 'Sueldo'

class RolAdmin(admin.ModelAdmin):
    list_display = ('empleado', 'aniomes', 'sueldo_formateado', 'horas_extra', 'bono', 'neto_formateado')
    list_filter = ('aniomes', 'empleado__departamento')
    search_fields = ('empleado__nombre', 'empleado__cedula')
    date_hierarchy = 'aniomes'
    list_per_page = 20
    
    fieldsets = (
        (None, {
            'fields': ('empleado', 'aniomes')
        }),
        ('Ingresos', {
            'fields': ('sueldo', 'horas_extra', 'bono')
        }),
        ('Cálculos Automáticos (No editable)', {
            'fields': ('iess', 'tot_ing', 'tot_des', 'neto'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('iess', 'tot_ing', 'tot_des', 'neto')
    
    def sueldo_formateado(self, obj):
        return f"${obj.sueldo:,.2f}"
    sueldo_formateado.short_description = 'Sueldo'
    
    def neto_formateado(self, obj):
        return f"${obj.neto:,.2f}"
    neto_formateado.short_description = 'Neto a Pagar'



# Registro de modelos
admin.site.register(Cargo)
admin.site.register(Departamento)
admin.site.register(TipoContrato)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Rol, RolAdmin)