from datetime import datetime

from django import forms
from django.forms import ModelForm
from django.forms.models import ModelChoiceField
from core.erp.models import Category, Compras, FinancieroPagos, Product, Client,Transfer,Impuesto, Operaciones, Purchase,PurchaseOrder, Sale, Vendor, Gastos, Measures, CreditCard, PlanCuentas, RecepcionCompra, Secuences, Facturacion, Serie, PriceList, Sucursal, Provider, Grouprov, Scrap, Tariff, Timelimit, Payment


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
        #fields = 'name', 'cat', 'image', 'stock', 'pvp', 'standardcost'

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                    'class': 'form-control',

                }
            ),
            'cat': forms.Select(attrs={
                'class': 'form-control',
            }),
            #'cat': forms.Select(
            #    attrs={
            #    'class': 'custom-select select2',
            #        'style': 'width: 100%'
            #    }
            #),
             'datasheet': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese ficha técnica del producto',
                    'rows': 3,
                    'cols': 3,
                    'class': 'form-control',

                }
            ),
             'detail': forms.Textarea(
                attrs={
                    'placeholder': 'Ingrese detalle del producto',
                    'rows': 3,
                    'cols': 3,
                    'class': 'form-control',

                }
            ),
            'stock': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'maxstock': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'minstock': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'pvp': forms.TextInput(attrs={
                'readonly': True,
                #'id':'id_pvp',

                'class': 'form-control',
            }),
            'standardcost': forms.TextInput(attrs={
                'class': 'form-control',
                #'id':'id_standardcost',
            }),
          
            'suc': forms.Select(attrs={
                'class': 'form-control',
            }),
            'medidas': forms.Select(attrs={
                'class': 'form-control',
            }),
            #'image': forms.FileInput(attrs={
            #    'onchange': 'getImagePreview(event)',
            #}),
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
        self.fields['plazo'].queryset = PriceList.objects.all()

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
            #'plazo': forms.Select(attrs={
            #    'class': 'form-control',
            #    #'class': 'custom-select select2',

            #    # 'style': 'width: 100%'
            #'plazo': ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
            #    'class': 'form-control',
            'plazo': forms.Select(attrs={
                'class':'form-control',
            
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                #'id':'tipo',

                #'class': 'custom-select select2',

                # 'style': 'width: 100%'
            }),
            'tax': forms.Select(attrs={
                'class': 'form-control',
                #'id':'tipo',

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
            #'sucursal': forms.Select(attrs={
            #    'class': 'form-control',
            #}),
            'sucursal': forms.Select(attrs={
                'class': 'form-control',
            }),
            'vendedor': forms.Select(attrs={
                'class': 'form-control',
            }),

            'femmision': forms.Select(attrs={
                'class': 'form-control',
            }),
            'entrada': forms.TextInput(attrs={
                'readonly': False,
                'class': 'form-control',
            }),
           'estado': forms.Select(attrs={
                'readonly': True,

                'class': 'form-control',
                #'id':'tipo',

                #'class': 'custom-select select2',

                # 'style': 'width: 100%'
            }),
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
        self.fields['cli'].queryset = Provider.objects.none()

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
            'baseiva': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'estado': forms.Select(),
            'tax': forms.Select(attrs={
                'class': 'form-control',
                #"onChange":'selfuncion()',
                'id':'tax',
                # 'style': 'width: 100%'
            }),
            'tipo_pagos': forms.Select(attrs={
                'class': 'form-control',
                # 'style': 'width: 100%'
            }),
            'sucursal': forms.Select(attrs={
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
class PurchaseOrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cli'].queryset = Provider.objects.none()

    class Meta:
        model = PurchaseOrder
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
            'referencia': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'baseiva': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'estado': forms.Select(),
            'tax': forms.Select(attrs={
                'class': 'form-control',
                #"onChange":'selfuncion()',
                'id':'tax',
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
            'concepto': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Concepto de Transferencia',
                }
            ),
            'observacion': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese observación',
                }
            ),
            'referencia': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese referencia',
                }
            ),
            'sucdestino': forms.Select(
                attrs={
                    'class': 'form-control',
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
            'name': forms.TextInput(attrs={
                'class': 'form-control',

            }),

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

class GrouprovForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Grouprov
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre del Grupo',
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

class ScrapForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Scrap
        fields = '__all__'
        widgets = {
            'name': forms.Select(attrs={
                'class': 'form-control',

            }),
            'sucursal': forms.Select(attrs={
                'class': 'form-control',

            }),
            'desc': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un motivo',

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


class TariffForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['titulo'].widget.attrs['autofocus'] = True

    class Meta:
        model = Tariff
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
            'descuento': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese descuento',
                    
                }
            ),
            'tipo': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un tipo de tiempo',
                }
            ),
        }


class PriceListForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = PriceList
        fields = '__all__'
        widgets = {

            'desc': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un motivo',

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

class SerieForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['prod'].widget.attrs['autofocus'] = True

    class Meta:
        model = Serie
        fields = '__all__'
        widgets = {
            'ref': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese una referencia',
                }
            ),
            'prod': forms.Select(attrs={
                'class': 'form-control',

            }),
            'fecha': forms.DateInput(
                attrs={
                        'class': 'form-control',
                        'type':'date'
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


class VendorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Vendor
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
            'suc': forms.Select(attrs={
                'class': 'form-control',

            }),
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


class FacturacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['serie'].widget.attrs['autofocus'] = True

    class Meta:
        model = Facturacion
        fields = '__all__'
        widgets = {
            'serie': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese una serie',
                }
            ),
            'concepto': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un concepto',

                }
            ),
            'cedula': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese número de cédula',

                }
            ),
            'codigo': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un código',

                }
            ),
            'fechaemision': forms.DateInput(
                attrs={
                        'class': 'form-control',
                        'type':'date'
                }
            ),
            'fechavencimiento': forms.DateInput(
                attrs={
                        'class': 'form-control',
                        'type':'date'

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

class SecuencesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Secuences
        fields = '__all__'
        widgets = {
            'numero': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'suc': forms.Select(attrs={
                'class': 'form-control',

            }),
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

class MeasuresForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Measures
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese nombre',
                }
            ),
            'type': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese tipo',

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

class CreditCardForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['description'].widget.attrs['autofocus'] = True

    class Meta:
        model = CreditCard
        fields = '__all__'
        widgets = {
            'description': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
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


class PlanCuentasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['codigocontable'].widget.attrs['autofocus'] = True

    class Meta:
        model = PlanCuentas
        fields = '__all__'
        widgets = {
            'codigocontable': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese código contable',
                }
            ),
            'descripcion': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese una descripción',

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



class RecepcionCompraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nrecepcion'].widget.attrs['autofocus'] = True


    class Meta:
        model = RecepcionCompra
        fields = '__all__'
        widgets = {
            'nrecepcion': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un Número de Recepción',
                }
            ),
            'concepto': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un concepto',
                }
            ),
            'fecha': forms.DateInput(
                attrs={
                        'class': 'form-control',
                        'type':'date'
                }
            ),
            'codigo': forms.TextInput(
                attrs={
                    'placeholder': 'Ingrese un concepto',

                }
            ),
            'proveedor': forms.Select(attrs={
                'class': 'form-control',

            }),
            'almacen': forms.Select(attrs={
                'class': 'form-control',

            }),
            'costos': forms.Select(attrs={
                'class': 'form-control',

            }),
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


class GastosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['cuenta'].widget.attrs['autofocus'] = True

    class Meta:
        model = Gastos
        fields = '__all__'
        widgets = {
            'cuenta': forms.Select(attrs={
                'class': 'form-control',

            }),
            'retenciones': forms.Select(attrs={
                'class': 'form-control',

            }),
            'iva': forms.Select(attrs={
                'class': 'form-control',

            }),
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


class ComprasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cli'].queryset = Provider.objects.none()

    class Meta:
        model = Compras
        fields = '__all__'
        widgets = {
            'cli': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
            }),
            'femision': forms.DateInput(
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
            'baseiva': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
            }),
            'estado': forms.Select(),
            'tax': forms.Select(attrs={
                'class': 'form-control',
                #"onChange":'selfuncion()',
                'id':'tax',
                # 'style': 'width: 100%'
            }),
            'tipo_pagos': forms.Select(attrs={
                'class': 'form-control',
                # 'style': 'width: 100%'
            }),
            'sucursal': forms.Select(attrs={
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

class FinancieroPagosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for form in self.visible_fields():
        #     form.field.widget.attrs['class'] = 'form-control'
        #     form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['cli'].widget.attrs['autofocus'] = True

    class Meta:
        model = FinancieroPagos
        fields = '__all__'
        widgets = {
            'cli': forms.Select(attrs={
                'class': 'form-control',
                # 'style': 'width: 100%'
            }), 
            'concepto': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'codigoPago': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'femision': forms.DateInput(
                attrs={
                        'class': 'form-control',
                        'type':'date'


                }
            ),
            'fvencimiento': forms.DateInput(
                attrs={
                        'class': 'form-control',
                        'type':'date'


                }
            ),
            'concepto': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'movimiento': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'valorDeuda': forms.TextInput(attrs={
                'class': 'form-control',
            }),
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