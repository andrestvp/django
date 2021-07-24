from datetime import datetime

from django import forms
from django.forms import ModelForm

from core.erp.models import Category, Product, Client,Transfer,Impuesto, Operaciones, Purchase, Sale, Sucursal, Provider, Timelimit, Payment


class CategoryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'desc': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ProductForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Product
        fields = '__all__'
        #fields = 'name', 'cat', 'image', 'stock', 'pvp', 'costo'

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    'class': 'form-control',

                }
            ),
            
            'cat': forms.Select(
                attrs={
                'class': 'custom-select select2',
                    'style': 'width: 100%'
                }
            ),
            'stock': forms.TextInput(attrs={
                'readonly': False,
                'class': 'form-control',
            })
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'surnames': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su cédula',
                }
            ),
            'date_birthday': forms.DateInput(format='%Y-%m-%d',
                                       attrs={
                                           'value': datetime.now().strftime('%Y-%m-%d'),
                                       }
                                       ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': forms.Select()
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['name']) <= 50:
    #         raise forms.ValidationError('Validacion xxx')
    #         # self.add_error('name', 'Le faltan caracteres')
    #     return cleaned



class TimelimitForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['titulo'].widget.attrs['autofocus'] = True

    class Meta:
        model = Timelimit
        fields = '__all__'
        widgets = {
            'titulo': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese título',
                }
            ),
            'dias': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un días',
                    
                }
            ),
            'tipo': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un tipo de tiempo',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data



class ProviderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Provider
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'surnames': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su cédula',
                }
            ),
            'email': forms.DateInput(format='%Y-%m-%d',
                                       attrs={
                                          'placeholder': 'Ingrese su correo',
                                       }
                                       ),
            'address': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese su dirección',
                }
            ),
            'gender': forms.Select()
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data



class TestForm(forms.Form):
    categories = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    products = forms.ModelChoiceField(queryset=Product.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese una descripción'
    # }))

    search = forms.ModelChoiceField(queryset=Product.objects.none(), widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cli'].queryset = Client.objects.none()
        #self.fields['plazo'].queryset = Timelimit.objects.none()

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'date_joined': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'plazo': forms.Select(attrs={
                'class': 'form-control',
                #'class': 'custom-select select2',

                # 'style': 'width: 100%'
            }),
            'iva': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
             'totalpagar': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',      
            }),
            'entrada': forms.TextInput(attrs={
                'readonly': False,
                'class': 'form-control',
            })
        }




class SucursalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Sucursal
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'ubic': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data



class PurchaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cli'].queryset = Client.objects.none()
        #self.fields['plazo'].queryset = Timelimit.objects.none()

    class Meta:
        model = Purchase
        fields = '__all__'
        widgets = {
            'cli': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'date_joined': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'date_joined',
                    'data-target': '#date_joined',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'descuento': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'estado': forms.Select(),
            'tax': forms.Select(attrs={
                'class': 'form-control',
                # 'style': 'width: 100%'
            }),
            'tipo_pagos': forms.Select(attrs={
                'class': 'form-control',
                # 'style': 'width: 100%'
            }),

                        
            'total': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'plazo': forms.Select(attrs={
                'class': 'form-control',
                # 'style': 'width: 100%'
            })
            
        }
class TransferForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['Contacto'].widget.attrs['autofocus'] = True

    class Meta:
        model = Transfer
        fields = '__all__'
        widgets = {
            'Contacto': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Encargado de Transferencia',
                }
            ),
            'Operacion': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
             'sucorigen': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'fechaSalida': forms.DateInput(
                attrs={
                        'class': 'form-control',
                        'type':'date'


                }
            ),
            'fechaPrevista': forms.DateInput(
                attrs={
                        'class': 'form-control',
                        'type':'date'


                }
            ),
            'sucorigin': forms.Select(
                attrs={
                    'class': 'form-control',

                    
                }
            )
            
        }


        

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
        
            
class OperacionesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Operaciones
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese Nombre de Operacion',
                }
            ),
            'desc': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese Descripcion',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class PaymentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Payment
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un Plazo de Pago',
                }
            ),
            'desc': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese una descripción',
                    'rows': 3,
                    'cols': 3
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data



class ImpuestoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Impuesto
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese Título',
                }
            ),
            'valor': forms.TextInput(
                attrs={
                     'placeholder': 'Ingrese Valor',
                }
            ),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
