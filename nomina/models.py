from django.db import models
from decimal import Decimal

# Create your models here.
class Cargo(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

class Departamento(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

class TipoContrato(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion
    
class Empleado(models.Model):
    SEXO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Femenino'),
    ]

    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    direccion = models.TextField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento,
    on_delete=models.CASCADE)
    tipo_contrato = models.ForeignKey(TipoContrato,
    on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"

class Rol(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    aniomes = models.DateField()
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    horas_extra = models.DecimalField(max_digits=10, decimal_places=2)
    bono = models.DecimalField(max_digits=10, decimal_places=2)
    iess = models.DecimalField(max_digits=10, decimal_places=2)


    tot_ing = models.DecimalField(max_digits=10, decimal_places=2)
    tot_des = models.DecimalField(max_digits=10, decimal_places=2)
    neto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Rol de {self.empleado.nombre} - {self.aniomes.strftime('%Y-%m')}"
    

    def save(self, *args, **kwargs):
            # Calcular campos automáticos
            self.iess = self.sueldo * Decimal('0.0945')  # 9.45%
            self.tot_ing = self.sueldo + self.horas_extra + self.bono
            self.tot_des = self.iess
            self.neto = self.tot_ing - self.tot_des
            super().save(*args, **kwargs)

