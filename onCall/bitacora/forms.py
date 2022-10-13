
from django import forms
from .models import Incidencia, Elemento, IncideciaHijo
from ckeditor.widgets import CKEditorWidget



class IncidenciaForm(forms.ModelForm):
    #inicio_afectacion = forms.SplitDateTimeField(widget=forms.SplitDateTimeWidget(date_attrs={'class': 'form-control', 'required': 'True', 'type':'date'}, time_attrs={'class': 'form-control', 'required': 'True', 'type':'time'}))
    class Meta:
        model = Incidencia
        fields = ['folio','estado','msr','noti','description','nemonico','region','inicio_afectacion','ultima_actualizacion','proxima_actualizacion','calendarizacion', 'elemento']
        widgets = {
            'folio': forms.TextInput(attrs={'class': 'form-control', 'required': 'True', 'placeholder':'Ticket...'}),
            'estado': forms.Select(attrs={'class': 'form-control', 'required': 'True', }),
            'msr': forms.Select(attrs={'class': 'form-control', 'required': 'True', }),
            'noti': forms.Select(attrs={'class': 'form-control', 'required': 'True', }),

            'description': forms.Textarea(attrs={'class': 'form-control', 'required': 'True','rows':2 }),

            'nemonico': forms.TextInput(attrs={'class': 'form-control', 'required': 'True', 'placeholder':'Nemónico...'}),
            'region': forms.Select(attrs={'class': 'form-control', 'required': 'True'}),


            'inicio_afectacion': forms.TextInput(attrs={'class': 'form-control', 'required': 'True', 'type':'datetime-local'}),
            'ultima_actualizacion': forms.TextInput(attrs={'class': 'form-control', 'type':'datetime-local'}),
            'proxima_actualizacion': forms.TextInput(
                attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'calendarizacion': forms.TextInput(
                attrs={'class': 'form-control',  'type': 'datetime-local'}),
            'elemento': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

        labels = {
            'folio': 'Ticket',


        }

        def clean_folio(self):
            folio = self.cleaned_data['folio']

            if Incidencia.objects.filter(folio=folio).exists():
                raise ValidationError("Este folio ya existe...")
            return folio



class ElementoForm(forms.ModelForm):
    class Meta:
        model = Elemento
        fields = ['nombre','description','nemonico']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'True', 'placeholder':'Nombre del Elemento...'}),


            'description': forms.Textarea(attrs={'class': 'form-control', 'required': 'True','rows':2 , 'placeholder':'Descripción del Elemento...'}),

            'nemonico': forms.TextInput(attrs={'class': 'form-control', 'required': 'True', 'placeholder':'Nemónico...'}),
        }


class IncidenciaHijoForm(forms.ModelForm):

    class Meta:
        model = IncideciaHijo
        fields = ['folio','estado','msr','description','padre','nemonico']
        widgets = {
            'folio': forms.TextInput(attrs={'class': 'form-control', 'required': 'True', 'placeholder':'Ticket...'}),
            'estado': forms.Select(attrs={'class': 'form-control', 'required': 'True', }),
            'msr': forms.Select(attrs={'class': 'form-control', 'required': 'True', }),


            'description': forms.Textarea(attrs={'class': 'form-control', 'required': 'True','rows':2 }),
            'padre': forms.Select(attrs={'hidden': 'True'}),
            'nemonico': forms.TextInput(attrs={'class': 'form-control', 'required': 'True', 'placeholder':'Nemónico...'}),

        }