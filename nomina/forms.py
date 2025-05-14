from django.forms import ModelForm, TextInput, EmailInput, NumberInput, Select, DateInput, Textarea
from django import forms
from .models import Cargo, Departamento, TipoContrato, Empleado, Rol

class CargoForm(forms.ModelForm):
    descripcion = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el cargo',
            'autocomplete': 'off'
        }),
        label='Descripción del Cargo'
    )
    
    class Meta:
        model = Cargo
        fields = ['descripcion']
        widgets = {
            'descripcion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el cargo',
                'autocomplete': 'off'
            })
        }

class DepartamentoForm(forms.ModelForm):
    descripcion = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el departamento',
            'autocomplete': 'off'
        }),
        label='Descripción del Departamento'
    )
    
    class Meta:
        model = Departamento
        fields = ['descripcion']
        widgets = {
            'descripcion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el departamento',
                'autocomplete': 'off'
            })
        }

class TipoContratoForm(forms.ModelForm):
    descripcion = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el tipo de contrato',
            'autocomplete': 'off'
        }),
        label='Tipo de Contrato'
    )
    
    class Meta:
        model = TipoContrato
        fields = ['descripcion']
        widgets = {
            'descripcion': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el tipo de contrato',
                'autocomplete': 'off'
            })
        }

class EmpleadoForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre completo',
            'autocomplete': 'off'
        }),
        label='Nombre Completo'
    )
    cedula = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese la cédula sin guiones',
            'autocomplete': 'off'
        }),
        label='Cédula',
        help_text='Ingrese cédula sin guiones'
    )
    direccion = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ingrese la dirección completa'
        }),
        label='Dirección'
    )
    sexo = forms.ChoiceField(
        choices=Empleado.SEXO_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    sueldo = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': 'Ingrese el sueldo base'
        }),
        label='Sueldo Base',
        min_value=0
    )
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Cargo'
    )
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Departamento'
    )
    tipo_contrato = forms.ModelChoiceField(
        queryset=TipoContrato.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Tipo de Contrato'
    )

    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if not cedula.isdigit():
            raise forms.ValidationError('La cédula debe contener solo números')
        if len(cedula) != 10:
            raise forms.ValidationError('La cédula debe tener 10 dígitos')
        return cedula

    def clean_sueldo(self):
        sueldo = self.cleaned_data['sueldo']
        if sueldo <= 0:
            raise forms.ValidationError('El sueldo debe ser mayor a 0')
        return sueldo

    class Meta:
        model = Empleado
        fields = ['nombre', 'cedula', 'direccion', 'sexo', 'sueldo', 'cargo', 'departamento', 'tipo_contrato']
        widgets = {
            'nombre': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre completo',
                'autocomplete': 'off'
            }),
            'cedula': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cédula',
                'autocomplete': 'off'
            }),
            'direccion': Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ingrese la dirección'
            }),
            'sexo': Select(attrs={
                'class': 'form-control'
            }),
            'sueldo': NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'cargo': Select(attrs={
                'class': 'form-control'
            }),
            'departamento': Select(attrs={
                'class': 'form-control'
            }),
            'tipo_contrato': Select(attrs={
                'class': 'form-control'
            })
        }

class RolForm(forms.ModelForm):
    empleado = forms.ModelChoiceField(
        queryset=Empleado.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'empleado_select'
        }),
        label='Empleado'
    )
    aniomes = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'style': 'height: 70px;'
        },
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d']
    )
    sueldo = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'readonly': 'readonly'
        }),
        label='Sueldo Base'
    )
    horas_extra = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Ingrese las horas extra'
        }),
        label='Horas Extra',
        initial=0
    )
    bono = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': 'Ingrese el bono'
        }),
        label='Bonificación',
        initial=0
    )
    iess = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'readonly': 'readonly'
        }),
        label='Aporte IESS'
    )
    tot_ing = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        label='Total Ingresos'
    )
    tot_des = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        label='Total Descuentos'
    )
    neto = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        label='Valor Neto'
    )

    class Meta:
        model = Rol
        fields = '__all__'
        widgets = {
            'empleado': Select(attrs={
                'class': 'form-control'
            }),
            'aniomes': forms.DateInput(attrs={
                'type': 'date'
            }, format='%Y-%m-%d'),
            'sueldo': NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Ingrese el sueldo base',
                'readonly': 'readonly'
            }),
            'horas_extra': NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Ingrese las horas extra'
            }),
            'bono': NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Ingrese el bono'
            }),
            'iess': NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'readonly': 'readonly'
            }),
            'tot_ing': NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'tot_des': NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            }),
            'neto': NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly'
            })
        }